from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions
import pandas as pd
import time
import urllib.request
import os.path

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
        load_more = self.driver.find_element(by=By.XPATH, value='.//button[@class="btn-primary show-more"]')
        while True:
            #time.sleep(3)
            page.send_keys(Keys.PAGE_DOWN)
            time.sleep(1) 
            x+=1
            if load_more:
                try:
                    load_more.click()
                    time.sleep(2)
                
                except selenium.common.exceptions.StaleElementReferenceException:pass
                break
            else:
                self.get_vegan_items()
                break


    def remove_promo(self):
        self.driver.find_element(by=By.XPATH, value=("//span[@id='aq-promo-close']/*[name()='svg']/*[name()='rect']")).click()

    def get_img_logo(self):
            logo=self.driver.find_element(by=By.XPATH, value="//img[@class='hd-header__logoImg']")
            img=logo.get_attribute("src")
            print(img)
            urllib.request.urlretrieve(str(img),"sample_data.jpg")
            
    def get_vegan_items(self)-> dict :
            self.products=self.driver.find_elements(by=By.XPATH,value= "//ul[@class='fops fops-regular fops-shelf']//li")
            self.data_dict={"all_name":[],"all_price":[],"all_url":[],"all_prod_img":[]}
            for product in self.products:
                name=product.find_element(by=By.XPATH,value=".//h4[@class='fop-title']/span")
                self.data_dict["all_name"].append(name.text)
                price=product.find_element(By.CLASS_NAME,("fop-price"))
                self.data_dict["all_price"].append(price.text)
                url=product.find_element(by=By.XPATH, value=".//div[@class='fop-contentWrapper']/a")
                product_link=url.get_attribute("href")
                self.data_dict["all_url"].append(product_link)
                img=product.find_element(by=By.XPATH, value=".//div[@class='fop-contentWrapper']//a//img")
                self.prod_img=img.get_attribute("src")
                self.prod_img_link=('https://www.ocado.com'+self.prod_img)
                self.data_dict["all_prod_img"].append(self.prod_img_link)
                
                self.prod_img_path=urllib.request.urlretrieve(self.prod_img_link,f"image_{name}.jpg")
                #print(self.data_dict)

                
            #self.driver.quit()

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
    #crawl.remove_promo()
    crawl.redirect_to_vegan_page()
    crawl.scroll_down()
    crawl.get_vegan_items()
    crawl.store_in_csv()
    crawl.store_in_json()
    crawl.get_scraped_time()

if __name__=='__main__':
    run()
