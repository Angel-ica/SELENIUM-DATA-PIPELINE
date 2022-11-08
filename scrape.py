from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import urllib.request

class WebCrawl():
    def __init__(self):
        self.driver=webdriver.Chrome()
        self.start_time = time.strftime("%H:%M:%S%p")
        
    def get_page(self):
        self.initial_time=time.time()
        print(f"starting at {self.start_time}")
        self.driver.get("https://www.ocado.com/browse/value-just-for-you-323660/everyday-savers-323640")
    def accept_cookies(self):
        accept_cookies=self.driver.find_element(by=By.XPATH, value ='.//button[@id="onetrust-accept-btn-handler"]')
        accept_cookies.click()
        # cookie=self.driver.get_cookie
        # print(cookie)
    def redirect_to_vegan_page(self):
        search = self.driver.find_element(by=By.XPATH, value='.//form[@class="hd-search__form hd-searchProminent__form"]')
        search.click()
        search_box=search.find_element(by=By.XPATH, value='//input[@id="search"]')
        search_box.send_keys('vegan')
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)
        #return ('https://www.ocado.com/search?entry=vegan')


    def scroll_down(self):
        x=0
        page = self.driver.find_element(by=By.TAG_NAME, value='body')
        while True:
            page.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
            x+=1
            if x==55:
                print("55 scrolls")
                break
        # self.driver.implicitly_wait(30)
        # time.sleep(20)
        # self.driver.execute_script("window.scrollTo({left: 0, top: document.body.scrollHeight, behavior : 'smooth'});")


    def remove_promo(self):
        promo=self.driver.find_element(by=By.XPATH, value="//span[@id='aq-promo-close']")
        promo.click()
         # if promo:
        #     promo.click()
        # else:
        #     print('id didnt work')
                      
    
    def get_img_logo(self):
            logo=self.driver.find_element(by=By.XPATH, value="//img[@class='hd-header__logoImg']")
            img=logo.get_attribute("src")
            print(img)
            urllib.request.urlretrieve(str(img),"sample_data.jpg")
            #assert "src" in logo
            
    def get_vegan_items(self):
            products=self.driver.find_elements(by=By.XPATH,value= "//ul[@class='fops fops-regular fops-shelf']//li")
            self.data_dict={"all_name":[],"all_price":[],"all_url":[],"all_prod_img":[]}
            for product in products:
                name=product.find_element(by=By.XPATH,value=".//h4[@class='fop-title']/span")
                self.data_dict["all_name"].append(name.text)
                price=product.find_element(By.CLASS_NAME,("fop-price"))
                self.data_dict["all_price"].append(price.text)
                url=product.find_element(by=By.XPATH, value=".//div[@class='fop-contentWrapper']/a")
                product_link=url.get_attribute("href")
                self.data_dict["all_url"].append(product_link)
                img=product.find_element(By.CLASS_NAME,("fop-img"))
                prod_img=img.get_attribute("src")
                self.data_dict["all_prod_img"].append(prod_img)
                return self.data_dict
            self.driver.quit()

    def store_in_csv(self):
        df=pd.DataFrame(self.data_dict)
        df.to_csv("my_file.csv",index=False,header=True)

    def store_in_json(self):
        df=pd.DataFrame(self.data_dict)
        df.to_json("myfile.json",orient='columns')

    def get_scraped_time(self):
        end_time= time.time()
        run_time=(end_time)-(self.initial_time)
        print(f"run time is approx {round((run_time),1)} secs")
    
def run():
    crawl=WebCrawl()
    crawl.get_page()
    crawl.accept_cookies()
    crawl.get_img_logo()
    crawl.redirect_to_vegan_page()
    crawl.scroll_down()
    crawl.get_vegan_items()
    crawl.store_in_csv()
    crawl.store_in_json()
    crawl.get_scraped_time()

if __name__=='__main__':
    run()
