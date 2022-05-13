import mysql.connector
import pandas as pd

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="testdatabase"
)
mycursor = db.cursor()

#mycursor.execute("DROP TABLE Specs")
#mycursor.execute("DROP TABLE Laptops")
#mycursor.execute("CREATE TABLE laptops(laptop_id int AUTO_INCREMENT PRIMARY KEY, href VARCHAR(255),title VARCHAR(255), price DECIMAL(10,2))")
#mycursor.execute("CREATE TABLE specs(laptop_id int,ghz VARCHAR(10),ssd VARCHAR(10),ram VARCHAR(10),hd VARCHAR(10),matrix VARCHAR(15),PRIMARY KEY(laptop_id),FOREIGN KEY(laptop_id) REFERENCES Laptops(laptop_id) ON DELETE CASCADE)")




def check_if_exists(href):
    mycursor.execute("SELECT * FROM laptops WHERE href = %s", (href))
    result = mycursor.fetchall()
    if len(result) == 0:
        return False
    else:
        return True


mycursor.execute("SELECT * FROM laptops")
#mycursor.execute("SELECT * FROM specs")
result = mycursor.fetchall()
for x in result:
    print(x)

def export_to_xlsx():
    mycursor.execute("SELECT * FROM laptops")
    result = mycursor.fetchall()
    df = pd.DataFrame(result)
    df.columns = ["laptop_id","href","title","price"]
    #df.to_excel("laptops.xlsx",index=False)
    
    mycursor.execute("SELECT * FROM specs")
    result = mycursor.fetchall()
    dxf = pd.DataFrame(result)
    dxf.columns = ["laptop_id","ghz","ssd","ram","hd","matrix"]
    
    df= df.merge(dxf)
    df.to_excel("data_v3.xlsx",index=False)
    #dxf.to_excel("specs.xlsx",index=False)
    return 0




def clean_empty_values():
    mycursor.execute("DELETE FROM specs WHERE ghz = '' OR ram = ''OR hd = '' OR matrix = '' ")
    db.commit()
    mycursor.execute("SELECT laptop_id FROM laptops WHERE laptop_id NOT IN (SELECT laptops.laptop_id FROM laptops RIGHT JOIN specs ON laptops.laptop_id = specs.laptop_id)") # WHERE laptops.laptop_id IS NULL
    result = mycursor.fetchall()
    for x in result:
        mycursor.execute("DELETE FROM laptops WHERE laptop_id = %s", (x))
        print("Deleted laptop from database")
    db.commit()
    return 0



def add_to_database(href,title,price):
    mycursor.execute("INSERT INTO laptops(href,title,price) VALUES(%s,%s,%s)", (href,title,price))
    db.commit()
    print("Added to database")
    return 0

def add_specs_to_database(href,GHZ,SSD,RAM,HD,Matrix):
    mycursor.execute("SELECT laptop_id FROM laptops WHERE href = %s", (href))
    result = mycursor.fetchall()
    laptop_id = result[0][0]
    mycursor.execute("INSERT INTO specs(laptop_id,ghz,ssd,matrix,ram,hd) VALUES(%s,%s,%s,%s,%s,%s)", (laptop_id,GHZ,SSD,Matrix,RAM,HD))
    db.commit()
    print("Added to specs database")
    return 0


#clean_empty_values()
#export_to_xlsx()