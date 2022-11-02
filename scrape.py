from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class WebCrawl():
    def __init__(self):
        self.driver=webdriver.Chrome()

    def get_page(self):
        self.driver.get("https://www.ocado.com/browse/value-just-for-you-323660/everyday-savers-323640")
        accept_cookies=self.driver.find_element(by=By.XPATH, value ='.//button[@id="onetrust-accept-btn-handler"]')
        accept_cookies.click()
        # assert "ocado" in self.driver.title
        # assert "No results found." not in self.driver.page_source

    def redirect_to_vegan_page(self):
        search = self.driver.find_element(by=By.XPATH, value='.//form[@class="hd-search__form hd-searchProminent__form"]')
        search.click()
        search_box=search.find_element(by=By.XPATH, value='//input[@id="search"]')
        search_box.send_keys('vegan')
        search_box.send_keys(Keys.RETURN)

    def scroll_down(self):
        # x=0
        # page = self.driver.find_element(by=By.TAG_NAME, value='body')
        # while True:
        #     page.send_keys(Keys.PAGE_DOWN)
        #     time.sleep(1)
        #     x+=1
        #     if x==55:
        #         print("55 scrolls")
        #         break
        self.driver.execute_script("window.scrollTo({left: 0, top: document.body.scrollHeight, behavior : 'smooth'});")
            # if EC.presence_of_element_located((By.CLASS_NAME, "btn-primary show-more")):
            #     WebDriverWait(self.driver,60)  
            #     break

    # def remove_promo(self):
    #     promo=self.driver.find_element(by=By.XPATH, value="//span[@id='aq-promo-close']")
    #     promo.click()
                      
    def get_vegan_items(self):
        # promo=self.driver.find_element(By.ID, "aq-promo-close")
        # promo=self.driver.find_element(By.XPATH, "//span[@id='aq-promo-close']")

        # #promo.click()
        # if promo:
        #     promo.click()
        # else:
        #     print('id didnt work')
        products=self.driver.find_elements(by=By.XPATH,value= "//ul[@class='fops fops-regular fops-shelf']//li")
        for product in products:
            name=product.find_element(by=By.XPATH,value=".//h4[@class='fop-title']/span")
            print(name.text)
            price=product.find_element(By.CLASS_NAME,("fop-price"))
            print(price.text)
            url=product.find_element(by=By.XPATH, value=".//div[@class='fop-contentWrapper']/a")
            product_link=url.get_attribute("href")
            print(product_link)

        self.driver.quit()
    
def run():
    crawl=WebCrawl()
    crawl.get_page()
    crawl.redirect_to_vegan_page()
    crawl.remove_promo()
    crawl.scroll_down()
    crawl.get_vegan_items()
run()

