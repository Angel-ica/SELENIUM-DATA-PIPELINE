from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common.exceptions
import pandas as pd
import time
import urllib.request
import os
import os.path

class WebCrawl():
    def __init__(self):
        print(f"starting at {time.strftime('%H:%M:%S--%D')}")
        self.driver=webdriver.Chrome()

    def get_page(self):
        self.driver.get('https://www.cryptocompare.com')

    def scroll(self):
        total_height = int(self.driver.execute_script("return document.body.scrollHeight"))
        for i in range(1, total_height, 7):
            self.driver.execute_script("window.scrollTo(0, {});".format(i))

    def view_top_coins(self):
        view_more=self.driver.find_element(by=By.XPATH, value='//div[@class="table-coins-footer"]//a')
        ActionChains(self.driver).move_to_element(view_more).click().perform()
    
    def choose_currency(self):
        self.driver.find_element(By.ID, 'single-button').click()
        new_currency=self.driver.find_element(by=By.XPATH, value='//ul[@class="dropdown-menu"]//li[5]//a')
        ActionChains(self.driver).move_to_element(new_currency).click().perform()
        time.sleep(2)

    def get_top_coins(self):
        top_coins=self.driver.find_elements(by=By.XPATH, value='//div[@class="coins-list"]//tbody//tr')
        self.data_dict={'Rank':[],'Time':[],'Coin':[],'Symbol':[],'Price':[],'Change in last 24h':[],'Total vol(24h)':[]}
        #print(top_coins)
        for coin in top_coins:
            scraped_time=time.strftime('%H:%M:%S--%D')
            self.data_dict['Time'].append(scraped_time)
            rank=coin.find_element(by=By.XPATH, value='.//td[1]//div')
            self.data_dict['Rank'].append(rank.text)
            name=coin.find_element(by=By.XPATH, value='.//td[3]//a//h3//span[1]')
            self.data_dict['Coin'].append(name.text)
            symbol=coin.find_element(by=By.XPATH, value='.//td[3]//a//h3//span[2]')
            self.data_dict['Symbol'].append(symbol.text)
            price= coin.find_element(by=By.XPATH, value='.//td[4]//div')
            self.data_dict['Price'].append(price.text)
            last_24_hours=coin.find_element(by=By.XPATH, value='.//td[@class="change"]//div[1]//span')
            self.data_dict['Change in last 24h'].append(last_24_hours.text)
            volume_24h_GBP=coin.find_element(by=By.XPATH, value='.//td[@class="full-volume"]//div')
            self.data_dict['Total vol(24h)'].append(volume_24h_GBP.text)
   

    def store_in_csv(self):
        df=pd.DataFrame(self.data_dict)
        df.to_csv("crypto_compare_data.csv",index=False,header=True)

    def keep_open(self):
        print(f"finished at {time.strftime('%H:%M:%S--%D')}")

        time.sleep(5000)

def run():
    crawl=WebCrawl()
    crawl.get_page()
    crawl.view_top_coins()
    crawl.choose_currency()
    crawl.scroll()
    crawl.get_top_coins()
    crawl.store_in_csv()
    crawl.keep_open()
if __name__=='__main__':
    run()

