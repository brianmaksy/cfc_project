from lxml import html 
import requests

def request_page(url: str) -> requests.models.Response: 
    return requests.get(url)


def get_tree(r: requests.models.Response) -> html.HtmlElement:
    tree = html.fromstring(r.content)

    return tree 


def get_page_html(url: str) -> html.HtmlElement: 
    '''Item 1 in task: get index page'''
    r = request_page(url)
    tree = get_tree(r)

    return tree 

if __name__ == '__main__':
    url = "https://www.cfcunderwriting.com/en-gb/"

    # TASK 1: get index page 
    tree = get_page_html(url)
    
     # Task 2: 