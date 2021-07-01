import re
import io
from bs4 import BeautifulSoup
class Process_to_csv:
    def __init__(self) -> None:
        pass


    def get_file(self , filename , mode): 
        return io.open("./Main/{}".format(filename), mode , encoding="utf-8")

    def cleaning(self):
        file1 = self.get_file("Scrapped_raw_data.txt" , "r")
        read1 = file1.readlines()
        file1.close()
        read2 = []
        for line in read1:
            if re.match("^\w.*/table>$" , line) or re.match("<table" , line):
                read2.append(line)
        line_shift = {}
        for line_no , line in enumerate(read2, start=1):
            if not re.match("^<table" , line):
                line_shift[line_no] = line
        for key , value in line_shift.items():
            prev_loc = int(key) - 2
            new_string = read2[prev_loc].replace("\n" ,"") + str(value)
            read2.insert(prev_loc , new_string)
            read2.pop(key)
        for line in read2:
            if not re.match("^<table.*</table>$" , line):
                read2.remove(line)
        file2 = self.get_file("Scrapped_data.txt" , "w")
        for string in read2:
            file2.write(string)
        print("cleaning Finally Done ")
        file2.close()
    
    def get_no_p_line(self , table_line)->str:
        souppy= BeautifulSoup(table_line, 'html.parser')
        if souppy.p != None:
            souppy.p.decompose()
            return str(souppy).replace("more</span>" ,"</span>") .replace("RESALE" , "").replace("RERA" , "").replace("NEW BOOKING" , "").replace("₹" , " ₹ ").replace("/sq.ft" ,  " sq.ft ").replace("FEATURED", "").replace("NEW LAUNCH", "").replace("Onwards" , "")
        else:
             return str(souppy).replace("more</span>" ,"</span>").replace("RESALE" , "").replace("RERA" , "").replace("NEW BOOKING" , "").replace("₹" , " ₹ ").replace("/sq.ft" ,  " sq.ft ").replace("FEATURED", "").replace("NEW LAUNCH", "").replace("Onwards" , "")


    def writing_data(self):
        file = self.get_file("Scrapped_data.txt" , "r")
        read = file.readlines()
        file.close()
        csv_file = self.get_file("Result.csv" , "w")
        csv_file.write('areatype,availability,location,size,society,sqft,bath,price\n')
        for table_line in read:
            no_p_line = self.get_no_p_line(str(table_line))
            soup = BeautifulSoup(no_p_line, 'html.parser')
            td = soup.find_all('td')
            texts = list(i.text for i in td)
            for star , item in enumerate(texts , start=0 ):
                if star==0:
                    pass
                elif len(item) > 60:
                    texts.remove(item)
                else:
                    pass

            while ("" in texts):
                texts.remove("")

            csv_dict = self.process(texts)
            csv_file.write(f"{csv_dict['areatype']},{csv_dict['avail']},{csv_dict['location']},{csv_dict['size']},{csv_dict['society']},{csv_dict['sqft']},{csv_dict['bath']},{csv_dict['price']}\n")
        
        csv_file.close()
        print("Done ,You can know check Result.csv ")

    def process(self, text_list)-> dict:
        vars = {"areatype" :"",
                "avail" :"UNKNOWN",
                "location" :"",
                "size" :"",
                "society" :"",
                "sqft" :"",
                "bath" :"",
                "price" :""}
        #areatype
        for text in text_list:
            if re.match('^\d.*Area$' , str(text)):
                var1 = str(text).split(')')
                vars['areatype'] = str(var1[-1]).replace("," , "")

        #avail
        if str(text_list[-1]) == 'UNDER CONSTRUCTION' or str(text_list[-1])== 'READY TO MOVE':
            vars['avail'] = str(text_list[-1]).replace("," , "")

        # location
        vars['location'] = ((str(text_list[0]).split(' in '))[-1]).replace("," , "")
        
        # size
        if re.match('^\d' , text_list[0]):
            vars['size'] = (str(text_list[0]).split(" ")[0] + " BHK").replace("," , "")

        elif re.fullmatch('BHK' , text_list[-2]):
            vars['size'] = (str(text_list[-2]).split(" ")[0] + " BHK").replace("," , "")
        
        # Society
        if re.search('^[A-z]', text_list[1]):
            vars['society'] = str(text_list[1]).replace("," , "")

        # sqft
        for text in text_list:
            if re.match('^\d.*Area$' , str(text)):
                var1 = str(text).split('sq.ft.')
                vars['sqft'] = (str(var1[0]) + "sq.ft.").replace("," , "")

        #bath
        if re.search('Baths$' , text_list[-2]):
            temp_lis = str(text_list[-2]).split("BHK")
            vars['bath'] = str((("".join(temp_lis)).split(" "))[-2]).replace("," , "")
        
        #price
        for text in text_list:
            if re.match('^.*₹' , text):
                text = str(text).split('₹')
                vars['price'] = str(text[1]).replace("," , "")
        return vars




if __name__ == "__main__":
    obj1 = Process_to_csv() 
    obj1.cleaning()
    obj1.writing_data()
