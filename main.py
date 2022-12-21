import json
import warnings
from lxml import html 
import requests
from urllib.parse import urlparse
from pathlib import Path
from copy import deepcopy
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
    # chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=chrome_options)
    resources = []

    driver.get(url)

    for request in driver.requests:
        # if request.response and urlparse(url).netloc not in urlparse(request.url).netloc:
        if 'cfcunderwriting.com' not in urlparse(request.url).netloc:
            resources.append(request.url)

    driver.close()

    return resources


if __name__ == '__main__':

    url = "https://www.cfcunderwriting.com/"

    # TASK 1: Scrape the index webpage hosted at `cfcunderwriting.com`
    tree = get_page_html(url)

    # Task 2: Write a list of *all externally loaded resources* (e.g. images/scripts/fonts not hosted on cfcunderwriting.com) to a JSON output file.
    ext_resources = deepcopy(get_resources(url))
    Path("./output").mkdir(parents=True, exist_ok=True)
    with open('output/ext_resources.json', 'w') as file:
        # for r in ext_resources:
        r = json.dumps(f'ext_resources')
        file.write(f'{r}\n')
    
    # Task 3: 