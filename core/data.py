#import mysql.connector as con
import os
import random

class DataClient:
    def __init__(self):
        self.sql = False
        if self.sql:
            self.mycon = con.connect(host='Localhost',user='root',password='HariOm@123',database='12C23')
            self.mycursor = self.mycon.cursor()
            if self.mycon.is_connected():
                print("connected successfully")

    def fetch_titles(self,price=False):
        if self.sql:
            self.mycursor.execute("select Title,Price from books")
            list1 = [item for item in self.mycursor]
            random.shuffle(list1)
            titles = [item[0] for item in list1]
            price = [item[1] for item in list1]

            if price:
                return titles, price
            return titles
        else:
            list1 = [(name[:-4],random.randint(100,200)) for name in os.listdir("images/covers")]
            random.shuffle(list1)
            titles = [item[0] for item in list1]
            prices = [item[1] for item in list1]
            if price:
                return titles, prices
            return titles
        
    def fetch_prices(self,titles):
        if self.sql:
            for item in titles:
                self.mycursor.execute(f"select Price from books where Title={item}")
                prices.append(self.mycursor[0])
            return prices
        else:
            return [random.randint(100, 1000) for item in titles]

    def fetch_bookdetails(self,title):
        if self.sql:
            data = {}
            self.mycursor.execute(f"select Author,Genre,Pub_dt,Price from books where Title={title}")
            data["title"] = self.mycursor[0][1]
            data["author"] = self.mycursor[0][2]
            data["genre"] = self.mycursor[0][3]
            data["pub_dt"] = self.mycursor[0][4]
            data["price"] = self.mycursor[0][5]
            return data
        else:
            data = {
                "title":title,
                "author":random.choice(["charles dickens","john steinback","william golding","George Orwell"]),
                "genre":random.choice(["fiction","non-fiction","fantasy","romance"]),
                "pub_dt":f"{random.randint(1900,2000)}-{random.randint(1,12)}-{random.randint(1,30)}",
                "price":random.randint(100,1000)
            }
            return data