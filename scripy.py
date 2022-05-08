from enum import Flag
from pickle import TRUE
from bs4 import BeautifulSoup
import requests
from db import check_if_exists, add_to_database, add_specs_to_database
import re


class Scrapper:
    def __init__(self,url):
        self.url= url
        self.data = {
        }
    
    def req_url(self,url=None):
        if url is None:
            url = self.url
        result = requests.get(url)
        self.doc = BeautifulSoup(result.text, 'html.parser')
        return self.doc

    def loading_page_error_test(self):
        return False
            
    
    def get_data_from_page(self,href):
        url = f"https://www.olx.pl{href}"
        page = requests.get(url)
        return BeautifulSoup(page.text, 'html.parser')

    selector = {
        "title":["css-r9zjja-Text eu5v0x0"],
        "price":["css-okktvh-Text eu5v0x0"],
        "negotiable":["css-1897d50-Text eu5v0x0"],
        "date":["css-19yf5ek"],
        "description":["css-g5mtbi-Text"]
    }

    dataf = {
        "title":" ",
        "price":" ",
        "negotiable":" ",
        "date":" ",
        "description":" "
    }
    
    def get_specs_from_data(self):
        text = self.dataf["description"]
        GHZ = re.findall("([\.\d]+) *[gG][hH][zZ]|([\,\d]+) *[gG][hH][zZ]", text)
        SSD =  re.findall("\d+ *[gG][bB] *SSD|SSD *\d+ *[gG][bB]",text)
        GB = re.findall("\d+ *[gG][bB]",text)
        Matrix =''.joint(re.findall("[0-9]{3,4} *x *[0-9]{3,4}",text))
        RAM = re.findall("\s[0-9]{1,2} *[Gg][bB]",text)
        HD = re.findall("[0-9]{3,4} *[Gg][bB]",text)


        #GHZ
        try:
            for i in GHZ[0]:
                if len(i) > 0:
                    GHZ = ''.join([i])
                    break
        except IndexError:
            GHZ = ""
            pass
        if len(SSD) > 0:
            SSD=''.join(['1'])
        else:
            SSD=''.join(['0'])
        try:
            for i in GB:
                if i == re.findall("\d+ *[gG][bB]",RAM[0])[0]:
                    RAM=''.join([i])
                elif i == re.findall("\d+ *[gG][bB]",HD[0])[0]:
                    if len(SSD) > 0 and SSD[0] != i:
                        HD=''.join([i])
                else:
                    pass
        except IndexError:
                RAM = ''.join([])
                HD = ''.join([])
        
        specs = {
            "GHZ":GHZ,
            "SSD":SSD,
            "RAM":RAM,
            "HD":HD,
            "Matrix":Matrix
        }
        self.dataf["specs"] = specs
        return 0

    def get_data(self):
        self.doc = self.req_url()
        test = self.doc.find_all(["a"], class_="css-1bbgabe")
        for adver_number in range(len(test)):
            href = test[adver_number]['href'] # we check in database if the link is already in the database
            flag = check_if_exists([href])
            if flag:
                if len(test[adver_number].find_all(class_="css-1katuj6")) > 0:
                    continue
                else:
                    break
            else :
                doc = self.get_data_from_page(href)
                for key in self.selector:
                    try:
                        item = doc.find(class_=self.selector[key]).text
                    except :
                        item = " "
                    self.dataf[key]=item
                self.get_specs_from_data()
                add_to_database(href,self.dataf['title'],int(re.findall("\d+",self.dataf['price'])[0]))
                add_specs_to_database([href],self.dataf['specs']["GHZ"],self.dataf['specs']["SSD"],self.dataf['specs']["RAM"],self.dataf['specs']["HD"],self.dataf['specs']["Matrix"],)
                # flag = 0



        return test


x1 = Scrapper("https://www.olx.pl/d/elektronika/komputery/malopolskie/q-Laptop-ThinkPad/?search[photos]=1&page=1")

x1.get_data()
z = input()