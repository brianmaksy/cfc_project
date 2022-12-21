import json
import re
from typing import Tuple
from lxml import html 
import requests
from urllib.parse import urlparse
from pathlib import Path
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options


def request_page(url: str) -> requests.models.Response: 
    return requests.get(url)


def get_tree(r: requests.models.Response) -> html.HtmlElement:
    tree = html.fromstring(r.content)

    return tree 


def get_page_html(url: str) -> html.HtmlElement: 
    '''Returns the html tree of a given url, making use of the lxml module.'''
    r = request_page(url)
    tree = get_tree(r)

    return tree 


def get_resources(url: str) -> list:
    '''
    This function makes use of the selenium wire module (https://pypi.org/project/selenium-wire/).
    The module extends Selenium's Python bindings to grant access to underlying requests made by the browser.
    The function is largely an adapation of an answer from this page: https://stackoverflow.com/questions/69582773/get-all-loaded-website-resources-with-selenium
    '''
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    resources = []

    driver.get(url)

    for request in driver.requests:
        if 'cfcunderwriting.com' not in urlparse(request.url).netloc:
            resources.append(request.url)

    driver.close()

    return resources


def get_text_from_xml_element(e: html.HtmlElement) -> str:
    text_array = e.xpath('.//text()')
    text = ''
    if text_array: 
        text = text_array[0]
    return text 


def get_hyperlinks_and_identify_privacy_policy_location(tree: html.HtmlElement) -> Tuple[list, str]:
    '''
    Gets and writes elements with hyperlinks, then picks up the element with the text 'Privacy policy' and returns that link.
    '''
    link_elements = tree.xpath('.//a[@href]')
    privacy_policy_link = ''
    links = []
    for e in link_elements:
        link = e.xpath('.//@href')[0]
        links.append(link)
        text = get_text_from_xml_element(e)
        if text == 'Privacy policy':
            privacy_policy_link = link
     
    return links, privacy_policy_link


def re_trim_word(word: str) -> str:
    '''Trim word to only contain letters, except latinised ones like 'i.e.'.'''
    new_word = ''
    pattern = '[a-z.]+'
    m = re.search(pattern,word)
    if m: 
        new_word = m.group(0).strip()
        if new_word[-1] == '.' : new_word = new_word[:-1] 

    return new_word  


def word_frequency_count_from_page(tree: html.HtmlElement) -> dict:
    '''Returns word frequency counter/map for Task 4.'''
    text = get_visible_text(tree)
    counter_map = dict()
    for word in text.split():
        w = re_trim_word(word.lower())
        if w == '': continue 
        if w.lower() in counter_map:
            counter_map[w] += 1
        else: 
            counter_map[w] = 1 

    return counter_map

     
def get_visible_text(tree: html.HtmlElement) -> str:
    '''Obtain visible text from the privacy policy page for Task 4'''
    tree_body = tree.xpath('.//main[@class="individual-content"]/div')[0]
    headings = tree_body.xpath('.//h2')
    lines = tree_body.xpath('.//p')
    text_elements = headings + lines
    text = ''
    for elem in text_elements:
        # avoid getting text in href doubly 
        if elem in tree.xpath('.//a[@href]'): continue

        elem_text = elem.xpath('.//text()')
        elem_text = "".join(elem_text)
        
        if elem_text:
            t = elem_text.replace(u'\xa0', u' ').strip()
            if t: text += f'{t} '

    return text


if __name__ == '__main__':

    url = "https://www.cfcunderwriting.com"

    # TASK 1: Scrape the index webpage hosted at `cfcunderwriting.com`
    tree = get_page_html(url)

    # TASK 2: Write a list of *all externally loaded resources* (e.g. images/scripts/fonts not hosted on cfcunderwriting.com) to a JSON output file.
    ext_resources = get_resources(url)
    Path("./output").mkdir(parents=True, exist_ok=True)
    with open('output/ext_resources.json', 'w') as file:
        r = json.dumps(f'ext_resources')
        file.write(f'{r}\n')
    
    # TASK 3: Enumerates the page's hyperlinks and identifies the location of the "Privacy Policy" page
    links, privacy_policy_rel_link = get_hyperlinks_and_identify_privacy_policy_location(tree) # Tree from task 1
    with open('output/hyperlinks.txt', 'w') as file: 
        for i, link in enumerate(links): 
            file.write(f'{i} {link}\n')
    privacy_policy_link = url + privacy_policy_rel_link
    print(privacy_policy_link)

    # TASK 4: Use the privacy policy URL identified in step 3 and scrape the pages content. 
    # Produce a case-insensitive word frequency count for all of the visible text on the page.
    # Your frequency count should also be written to a JSON output file..
    tree = get_page_html(privacy_policy_link)
    word_counter_map = word_frequency_count_from_page(tree)
    with open('output/word_count.json', 'w') as file:
        file.write(json.dumps(word_counter_map))