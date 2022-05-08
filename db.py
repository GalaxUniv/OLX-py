import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="testdatabase"
)
mycursor = db.cursor()


#mycursor.execute("CREATE TABLE laptops(laptop_id int AUTO_INCREMENT PRIMARY KEY, href VARCHAR(255),title VARCHAR(255), price smallint)")
#mycursor.execute("CREATE TABLE specs(laptop_id int,ghz VARCHAR(10),sdd VARCHAR(10),ram VARCHAR(10),hd VARCHAR(10),matrix VARCHAR(15),PRIMARY KEY(laptop_id),FOREIGN KEY(laptop_id) REFERENCES Laptops(laptop_id) ON DELETE CASCADE)")

#mycursor.execute("DROP TABLE Specs")
#mycursor.execute("DROP TABLE Laptops")


def check_if_exists(href):
    mycursor.execute("SELECT * FROM laptops WHERE href = %s", (href))
    result = mycursor.fetchall()
    if len(result) == 0:
        return False
    else:
        return True

mycursor.execute("SELECT * FROM laptops")
for x in mycursor:
    print(x)



def add_to_database(href,title,price):
    mycursor.execute("INSERT INTO laptops(href,title,price) VALUES(%s,%s,%s)", (href,title,price))
    db.commit()
    print("Added to database")
    return 0

def add_specs_to_database(href,GHZ,SSD,RAM,HD,Matrix):
    mycursor.execute("SELECT laptop_id FROM laptops WHERE href = %s", (href))
    result = mycursor.fetchall()
    laptop_id = result[0][0]
    mycursor.execute("INSERT INTO specs(GHZ,SSD,GB,Matrix,RAM,HD) VALUES(%s,%s,%s,%s,%s,%s)", (laptop_id,GHZ,SSD,RAM,HD,Matrix))
    db.commit()
    print("Added to specs database")
    return 0


