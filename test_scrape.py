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
        self.scraper.get_page()
        self.scraper.accept_cookies()

    
    def test_redirect_to_vegan_page(self):
        vegan_page = self.scraper.redirect_to_vegan_page()
        get_url = self.scraper.driver.current_url
        self.assert_(get_url,vegan_page)


    def test_img_logo(self):
        self.assert_(os.path.isfile('./sample_data.jpg')
)  
    def test_vegan_items(self):
        vegan_items={}
        self.assertEqual(type(vegan_items),type(self.scraper.get_vegan_items()))

    def test_to_csv(self):
        self.assert_(os.path.isfile('./my_file.csv'))

    def test_to_json(self):
        self.assert_(os.path.isfile('./myfile.json'))



    
                                                                                                                                                                                                                                                                                                                                                                                                              

    

if __name__=='__main__':
    unittest.main()