import unittest
import time 
from scrape import WebCrawl as wb

class TestScrape(unittest.TestCase):

    def setUp(self):
        self.scraper = wb()
        #time.sleep(10)
    
    def test_get_page(self):
        get_page=self.scraper.get_page()
        self.assert_("ocado",get_page)

    def test_accept_cookies(self):
        accept_cookies =self.scraper.accept_cookies()
        self.scraper.driver.implicitly_wait(10)
        self.assert_(accept_cookies)

    def test_redirect_to_vegan_page(self):
        vegan_page = self.scraper.redirect_to_vegan_page()
        time.sleep(3)
        expected_output=self.scraper.driver.get('https://www.ocado.com/search?entry=vegan')
        self.assertEqual(expected_output,vegan_page)
    

if __name__=='__main__':
    unittest.main()