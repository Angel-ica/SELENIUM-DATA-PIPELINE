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
        self.driver=webdriver.Chrome()

    def get_page(self):
        self.driver.get('https://coinmarketcap.com/')
        self.driver.implicitly_wait(10)
        
    def accept_cookies(self):
        time.sleep(3)
        self.driver.find_element(By.TAG_NAME,'body').click()
        self.driver.find_element(by=By.XPATH, value="//div[@class='cmc-cookie-policy-banner__close']").click()
        
    def choose_currency(self):
        time.sleep(3)
        change_currency=self.driver.find_element(by=By.XPATH, value="//div[@class='sc-8580441d-1 klKJWV']//button[@class='sc-476bb07-0 sc-8580441d-7 FerZc']")
        change_currency.click()
        input_preferred_currency=self.driver.find_element(by=By.XPATH, value='//div[@class="sc-785445d2-4 kzsuLu"]//input')
        input_preferred_currency.send_keys('Pound Sterling')
        time.sleep(3)
        preferred_currrency=self.driver.find_element(by=By.XPATH, value='//div[@class="sc-8580441d-3 sc-8580441d-5 hFFJRw"]//div[@class="cmc-currency-picker--icon"]')
        ActionChains(self.driver).move_to_element(preferred_currrency).click().perform()

    def scroll(self):
        total_height = int(self.driver.execute_script("return document.body.scrollHeight"))
        for i in range(1, total_height, 7):
            self.driver.execute_script("window.scrollTo(0, {});".format(i))

    def get_top_100_coins(self):
            top_100_coins=self.driver.find_elements(by=By.XPATH, value='//div[@class="sc-853bfcae-1 eibzVK"]//tbody//tr')
            self.data_dict={'Rank':[],'Time':[],'Coin':[],'Symbol':[],'Price':[],'Change in last 24h':[],'Total vol(24h)':[]}

            for coins in top_100_coins:
                    rank=coins.find_element(by=By.XPATH, value='.//div[@class="sc-6110f1f2-2 iEQXo"]//div')
                    self.data_dict['Rank'].append(rank.text)
                    scraped_time=time.strftime('%H:%M:%S--%D')
                    self.data_dict['Time'].append(scraped_time)
                    coin=coins.find_element(by=By.XPATH, value='.//td//div[@class="sc-aef7b723-0 LCOyB"]//p[@class="sc-e225a64a-0 ePTNty"]')
                    self.data_dict['Coin'].append(coin.text)
                    symbol=coins.find_element(by=By.XPATH,value= './/td//div[@class="sc-aef7b723-0 LCOyB"]//p[@class="sc-e225a64a-0 dfeAJi coin-item-symbol"]')
                    self.data_dict['Symbol'].append(symbol.text)
                    price=coins.find_element(by=By.XPATH, value='.//td//div[@class="sc-7510a17-0 hEduBL"]//a//span')
                    self.data_dict['Price'].append(price.text)
                    last_24_hours=coins.find_element(by=By.XPATH, value='.//td//span[@class="sc-97d6d2ca-0 bQjSqS"]')
                    #caret_up=coins.find_element(by=By.XPATH, value='.//td//span[@class="sc-97d6d2ca-0 cYiHal"]//span')
                    # caret_down=last_24_hours.find_element(by=By.XPATH, value='.//td//span[@class="sc-97d6d2ca-0 bQjSqS"]//span[@class="icon-Caret-down"]')
                    # if caret_down in last_24_hours:
                    #     last_24h='▼',last_24_hours.text
                    # else:
                    #     last_24h=('▲',last_24_hours.text)
                    self.data_dict['Change in last 24h'].append(last_24_hours.text)
                    #unicode character for the sign is 'U+02D1'
                    volume_24h_GBP=coins.find_element(by=By.XPATH, value='.//td//div[@class="sc-aef7b723-0 sc-ba1a4d26-0 QisKn"]//a//p')
                    #volume_24h_coin=coins.find_element(by=By.XPATH, value='.//td//div[@class="sc-aef7b723-0 sc-ba1a4d26-0 QisKn"]//div//p')
                    self.data_dict['Total vol(24h)'].append(volume_24h_GBP.text)
                    print(self.data_dict)
                # except selenium.common.exceptions.NoSuchElementException:
                #     WebDriverWait(self.driver,20)


    def store_in_csv(self):
        df=pd.DataFrame(self.data_dict)
        df.to_csv("coin_market_cap_data.csv",index=False,header=True)
        print('done')
        time.sleep(2500)
        
def run():
    crawl=WebCrawl()
    crawl.get_page()
    crawl.accept_cookies()
    crawl.choose_currency()
    crawl.scroll()
    crawl.get_top_100_coins()
    crawl.store_in_csv()

if __name__=='__main__':
    run()


