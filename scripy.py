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
        try:
            result = requests.get(url)
            self.doc = BeautifulSoup(result.text, 'html.parser')
            return True
        except:
            return False

    def loading_page_error_test(self):
        return False
            
    
    def get_data_from_page(self,href):
        url = f"https://www.olx.pl{href}"
        page = requests.get(url)
        return BeautifulSoup(page.text, 'html.parser')


    
    def get_specs_from_data(self):
        text = self.dataf["description"]
        ghz = re.findall("([\.\d]+) *[gG][hH][zZ]|([\,\d]+) *[gG][hH][zZ]", text)
        ssd =  re.findall("\d+ *[gG][bB] *[sS][sS][dD]|[sS][sS][dD] *\d+ *[gG][bB]",text)
        gb = re.findall("\d+ *[gG][bB]",text)
        matrix = re.findall("[0-9]{3,4} *x *[0-9]{3,4}",text)

        ram = re.findall("\s[0-9]{1,2} *[Gg][bB]",text)
        hd = re.findall("[0-9]{3,4} *[Gg][bB]",text)

        
        try:
            for i in ghz[0]:
                if len(i) > 0:
                    ghz = ''.join([i])
                    break
        except IndexError:
            ghz = ""
            pass
        if len(ssd) > 0:
            ssd=''.join(['1'])
        else:
            ssd=''.join(['0'])
        try:
            for i in gb:
                if i == re.findall("\d+ *[gG][bB]",ram[0])[0]:
                    ram=[i]
                elif i == re.findall("\d+ *[gG][bB]",hd[0])[0]:
                    hd=[i]
                else:
                    pass
        except IndexError:
                ram = ''.join([])
                hd = ''.join([])
        
        ram = ''.join(ram)
        hd = ''.join(hd)

        if not matrix:
            matrix = ''
        else:
            matrix = matrix[0]

        specs = {
            "ghz":ghz,
            "ssd":ssd,
            "ram":ram,
            "hd":hd,
            "matrix":matrix
        }
        return specs


    def get_data(self):
        page=1
        flag = False

        while True:
            if flag == True:
                break
            if self.req_url(f"{self.url}&page={page}"):
                pass
            else:
                break
            test = self.doc.find_all(["a"], class_="css-1bbgabe")
            for adver_number in range(len(test)):
                href = test[adver_number]['href']

                flag = check_if_exists([href]) # we check in database if the link is already in the database
                if not flag :
                    doc = self.get_data_from_page(href)
                    for key in self.selector:
                        try:
                            item = doc.find(class_=self.selector[key]).text
                        except :
                            item = " "
                        self.dataf[key]=item

                    add_to_database(href,self.dataf['title'],float(''.join(re.findall("\d+\,[0-9]{1,2}|\d+",self.dataf['price'])).replace(',','.')))
                    specs = self.get_specs_from_data()
                    add_specs_to_database([href],specs["ghz"],specs["ssd"],specs["ram"],specs["hd"],specs["matrix"])
                else:
                    continue
            page+=1
        return 0


x1 = Scrapper("https://www.olx.pl/d/elektronika/komputery/laptopy/malopolskie/q-Laptop-ThinkPad/?search[order]=filter_float_price:desc")

x1.get_data()