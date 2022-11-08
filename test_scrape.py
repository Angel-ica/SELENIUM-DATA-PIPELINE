import unittest
import time
import os.path 
from scrape import WebCrawl as wb
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver



class TestScrape(unittest.TestCase):

    def setUp(self):
        self.scraper = wb()
        self.get_page=self.scraper.get_page()
        

    def test__get_page(self):
        #get_page=self.scraper.get_page()
        page_url=self.scraper.driver.current_url
        self.assert_("ocado",self.get_page)
        self.assert_(page_url,self.get_page)

    def test_accept_cookies(self):
        print('craving cookies')
        accept_cookies=self.scraper.accept_cookies()

        time.sleep(3)
        #assert not self.accept_cookies
        cookies=None
        self.assertEqual(type(accept_cookies),type(cookies))
        print('no more cookies!')

    def test_redirect_to_vegan_page(self):
        self.get_page=self.scraper.get_page()
        self.accept_cookies=self.scraper.accept_cookies()
        vegan_page = self.scraper.redirect_to_vegan_page()
        time.sleep(1)
        get_url = self.scraper.driver.current_url
        self.assert_(get_url,vegan_page)


    def test_img_logo(self):
        time.sleep(2)
        self.assert_(os.path.isfile('./sample_data.jpg')
)  
    def test_vegan_items(self):
        length_vegan_items={}
        self.assertEqual(type(length_vegan_items),type(self.scraper.get_vegan_items()))

    def test_to_csv(self):
        self.assert_(os.path.isfile('./my_file.csv'))

    def test_to_json(self):
        self.assert_(os.path.isfile('./myfile.json'))



    
                                                                                                                                                                                                                                                                                                                                                                                                              

    

if __name__=='__main__':
    unittest.main()