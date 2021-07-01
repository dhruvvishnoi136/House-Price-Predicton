import csv
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from time import sleep
import re
DRIVER=webdriver.Edge("./Main/msedgedriver 91.0.864.48.exe")
CSVFILE = open("./Main/zipcodes.csv", 'w')
class zipcode:
    def __init__(self )->None:
        pass

    def extracter(self):
        try:
            
            print("Starting Extractor\n")
            writer = csv.DictWriter(CSVFILE, fieldnames=["location" , "zipcode"])
            writer.writeheader()
            print("Extractor Started")
            data = pd.read_csv('./Main/Result.csv')
            unique_loc = list(data["location"].unique())
            DRIVER.get("https://pincodearea.in/search")
            sleep(2)
            for counter ,loc in enumerate(unique_loc , start=0):
                print(counter)
                name = str(loc) +" banglore"
                DRIVER.find_element_by_xpath('//*[@id="ibox"]').send_keys(name)
                DRIVER.find_element_by_xpath('//*[@class="searchbutton"]').click()
                sleep(2)
                soup = BeautifulSoup(DRIVER.page_source  ,'html.parser')
                section = soup.find('section' ,{"class": "left"})
                text = section.text
                lis = re.findall('(?<!\d)\d{6}(?!\d)', text)
                num = self.most_frequent(lis)
                if isinstance(num,str):
                    writer.writerow({"location": str(loc) ,"zipcode": int(num)})
                elif isinstance(num, list):
                    if len(num) != 0:
                        writer.writerow({"location": str(loc) ,"zipcode": int(num[0])})
                    else:
                        pass
                else:
                    pass

        except:
            pass


    def most_frequent(self,List):
        counter = 0
        num = List

        for i in List:
            curr_frequency = List.count(i)
            if (curr_frequency > counter):
                counter = curr_frequency
                num = i
        return num


if __name__ == "__main__":
    try:
        obj = zipcode()
        obj.extracter() 
    finally:
        DRIVER.close()
        CSVFILE.close()