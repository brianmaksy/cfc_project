
import re
import unittest
import warnings



from lxml import html
import requests 
from main import get_resources, get_tree, request_page



class TestScrape(unittest.TestCase):

    def setUp(self):
        '''See README.md remark on this.'''
        warnings.simplefilter('ignore', category=ResourceWarning)
        
    def test_get_index_webpage(self):
        index_url = "https://www.cfcunderwriting.com/"
        r = request_page(index_url)
        tree = get_tree(r)
        
        self.assertEqual(r.status_code, 200)
        self.assertEqual(type(tree), html.HtmlElement)

    def test_get_externally_loaded_resources(self):
        ext_resources = get_resources("https://www.cfcunderwriting.com/")
        presence_of_cfc_domain = all(['https://www.cfcunderwriting' not in resource for resource in ext_resources])
        self.assertTrue(presence_of_cfc_domain)
        

    def test_get_privacy_policy(self):
        # get_privacy_policy function should return the link 
        privacy_policy_link_obtained = 'https://www.cfcunderwriting.com/en-gb/support/privacy-policy/'
        self.assertEqual(privacy_policy_link_obtained,"https://www.cfcunderwriting.com/en-gb/support/privacy-policy/")


    def test_get_counter_map(self):
        counter_map = {'he':1, 'she':2}
        map_has_no_number = all([not bool(re.search(r'\d', w)) for w in counter_map.keys()])
        self.assertTrue(map_has_no_number)


if __name__ == '__main__':
    unittest.main()
