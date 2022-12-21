
import re
import unittest
import warnings



from lxml import html
import requests 
from main import get_hyperlinks_and_identify_privacy_policy_location, get_page_html, get_resources, get_tree, request_page



class TestScrape(unittest.TestCase):

    def setUp(self):
        '''See README.md remark on this.'''
        self.index_url = "https://www.cfcunderwriting.com"
        warnings.simplefilter('ignore', category=ResourceWarning)
        
    def test_get_index_webpage(self):
        r = request_page(self.index_url)
        tree = get_tree(r)

        self.assertEqual(r.status_code, 200)
        self.assertEqual(type(tree), html.HtmlElement)

    def test_get_externally_loaded_resources(self):
        ext_resources = get_resources(self.index_url)
        presence_of_cfc_domain = all([self.index_url not in resource for resource in ext_resources])
        self.assertTrue(presence_of_cfc_domain)
        

    def test_get_privacy_policy(self):
        tree = get_page_html(self.index_url)
        _, privacy_policy_rel_link = get_hyperlinks_and_identify_privacy_policy_location(tree) 
        privacy_policy_link_obtained = self.index_url + privacy_policy_rel_link
        self.assertEqual(privacy_policy_link_obtained,"https://www.cfcunderwriting.com/en-gb/support/privacy-policy/")


    def test_get_counter_map(self):
        counter_map = {'he':1, 'she':2}
        map_has_no_number = all([not bool(re.search(r'\d', w)) for w in counter_map.keys()])
        self.assertTrue(map_has_no_number)



if __name__ == '__main__':
    unittest.main()
