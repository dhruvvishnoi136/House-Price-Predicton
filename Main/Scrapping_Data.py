from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
import io
from os import fsync
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
class web_scarping:
    def __init__(self , driver , Scrapped_data , soup):  
        self.driver = driver
        self.Scrapped_data = Scrapped_data
        self.soup = soup

    def get_pages(self ,xpath):
        self.driver.get("https://www.99acres.com/")
        sleep(1.5)
        self.driver.find_element_by_xpath('//*[@id="keyword"]').send_keys("bang")
        sleep(1)
        self.driver.find_element_by_xpath(str(xpath)).click()
        sleep(0.5) 
        self.driver.find_element_by_xpath('//*[@id="submit_query"]').click()
        sleep(1.5)
        page_count = int(((self.driver.find_element_by_css_selector("""#app > div > div > div.r_srp__mainWrapper > 
        div.r_srp__rightSection > div.Pagination__srpPagination > div.caption_strong_large""").text).split(" "))[-1])
        sleep(0.5)
        return page_count 
        

            
    def Scrapping_tables(self ,page_count):
        self.driver.maximize_window()
        sleep(1)
        self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
        sleep(4)
        try:
            if ((self.driver.find_element_by_xpath('//*[@id="__ss_notif_frame_0"]')).is_displayed()) == True:
                self.driver.switch_to_frame('__ss_notif_frame_0')
                self.driver.find_element_by_xpath('/html/body/div[1]').click()
        except NoSuchElementException:
            pass
        sleep(1)
        for ranger in range(1 , page_count+1):
            print(ranger)
            sleep(1)
            soup_source = self.soup(self.driver.page_source, 'html.parser')
            table_tags = soup_source.find_all('table' , class_ = "srpTuple__tupleTable")
            sleep(1.5) 
            for line in table_tags:
                line.find('p').extract()
                self.Scrapped_data.write(str(line) + "\n")
                self.Scrapped_data.flush()
                fsync(Scrapped_data.fileno())
                
            sleep(0.5)
            try:
                Next_button = self.driver.find_element_by_link_text('Next Page >')
                ActionChains(driver=self.driver).move_to_element(Next_button).click().perform()
                sleep(1)
                self.driver.execute_script("arguments[0].click()" , Next_button)
            except NoSuchElementException:
                pass
            sleep(1)




    def main(self):
        xpaths = ['//*[@id="CITY_252, PREFERENCE_S, RESCOM_R"]' 
        , '//*[@id="CITY_22, PREFERENCE_S, RESCOM_R"]' 
        , '//*[@id="CITY_21, PREFERENCE_S, RESCOM_R"]' 
        , '//*[@id="CITY_217, PREFERENCE_S, RESCOM_R"]' 
        , '//*[@id="CITY_23, PREFERENCE_S, RESCOM_R"]' ]
        for xpath in xpaths:
            page_count =  self.get_pages(xpath)
            self.Scrapping_tables(page_count)










if __name__ == "__main__":
    Scrapped_data = io.open("./Main/Scrapped_raw_data.txt" , "w" , encoding="utf-8")
    driver = webdriver.Edge("./Main/msedgedriver 91.0.864.48.exe")
    soup = BeautifulSoup
    try:
        obj = web_scarping(driver , Scrapped_data , soup)
        obj.main()
    finally:
        driver.quit()
        Scrapped_data.close()

