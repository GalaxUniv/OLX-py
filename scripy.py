from bs4 import BeautifulSoup
import requests
from db import check_if_exists, add_to_database, add_specs_to_database
import re


class Scrapper:
    def __init__(self,url):
        self.url= url
        self.dataf = {
        "title":" ",
        "price":" ",
        "negotiable":" ",
        "date":" ",
        "description":" "
        }
        self.selector = {
        "title":["css-r9zjja-Text eu5v0x0"],
        "price":["css-okktvh-Text eu5v0x0"],
        "negotiable":["css-1897d50-Text eu5v0x0"],
        "date":["css-19yf5ek"],
        "description":["css-g5mtbi-Text"]
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


    
    def get_specs_from_data(self):
        text = self.dataf["description"]
        GHZ = re.findall("([\.\d]+) *[gG][hH][zZ]|([\,\d]+) *[gG][hH][zZ]", text)
        SSD =  re.findall("\d+ *[gG][bB] *SSD|SSD *\d+ *[gG][bB]",text)
        GB = re.findall("\d+ *[gG][bB]",text)
        Matrix = re.findall("[0-9]{3,4} *x *[0-9]{3,4}",text)
        RAM = re.findall("\s[0-9]{1,2} *[Gg][bB]",text)
        HD = re.findall("[0-9]{3,4} *[Gg][bB]",text)

        
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
                    RAM=[i]
                elif i == re.findall("\d+ *[gG][bB]",HD[0])[0]:
                    HD=[i]
                else:
                    pass
        except IndexError:
                RAM = ''.join([])
                HD = ''.join([])
        
        RAM = ''.join(RAM)
        HD = ''.join(HD)


        specs = {
            "GHZ":GHZ,
            "SSD":SSD,
            "RAM":RAM,
            "HD":HD,
            "Matrix":Matrix
        }
        return specs

    def get_data(self):
        self.doc = self.req_url()
        test = self.doc.find_all(["a"], class_="css-1bbgabe")
        for adver_number in range(len(test)):
            href = test[adver_number]['href']
            
            flag = check_if_exists([href]) # we check in database if the link is already in the database
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

                add_to_database(href,self.dataf['title'],float(''.join(re.findall("\d+\,[0-9]{1,2}|\d+",self.dataf['price'])).replace(',','.')))
                specs = self.get_specs_from_data()
                print(specs)
                add_specs_to_database([href],specs["GHZ"],specs["SSD"],specs["RAM"],specs["HD"],specs["Matrix"])

        return 0


x1 = Scrapper("https://www.olx.pl/d/elektronika/komputery/malopolskie/q-Laptop-ThinkPad/?search[photos]=1&page=1")

x1.get_data()