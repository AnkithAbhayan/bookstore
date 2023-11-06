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
            self.mycursor.execute(f"select BookNo, Author,Genre,Pub_dt,Price,description from books where Title='{title}'")
            for x in self.mycursor:
                data["title"] = title
                data["BookNo"] = x[0]
                data["author"] = x[1]
                data["genre"] = x[2]
                data["pub_dt"] = x[3]
                data["price"] = x[4]
                data["description"] = x[5]
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

    def create_account(self,uname,password):
        if self.sql:
            qry = f"insert into userdata values('{uname}','{password}')"
            self.mycursor.execute(qry)
            self.mycon.commit()
 
    def delete_account(self,uname):
        if self.sql:
            qry = f"delete from userdata where username='{uname}'"
            self.mycursor.execute(qry)
            self.mycon.commit()

    def userexists(self,username, password=None):
        if self.sql:
            qry = f"select * from userdata"
            self.mycursor.execute(qry)
            vals = [item for item in self.mycursor]
        else:
            vals = [("Ankith Abhayan","wakapie1234#"),("Karun","helloworld##")]
        if not password:
            for item in vals:
                if item[0] == username:
                    return True
            return False
        
        for item in vals:
            if item[0] == username and item[1]==password:
                return True
        return False

    def add_purchase(self,Username,BookNo,Qty,Price,DateTime):
        if self.sql:   
            qry = f"insert into purchases values('{Username}',{BookNo},{Qty},{Price}'{DateTime}')"
            self.mycursor.execute(qry)
            self.mycon.commit()

    def addtocart(self,Username, BookNo, Qty):
        if self.sql:
            qry = f"insert into cart values('{Username}',{BookNo},{Qty})"
            self.mycursor.execute(qry)
            self.mycon.commit()

    def deletefromcart(self,Username,BookNo):
        if self.sql:
            qry = f"delete from cart where username='{Username}' and BookNo='{BookNo}'"
            self.mycursor.execute(qry)
            self.mycon.commit()

    def fetch_cart(self,Username):
        if self.sql:
            qry = f"select * from cart where username='{Username}'"
            self.mycursor.execute(qry)
            vals = [x for x in self.mycursor]
            return vals
        return []

    def fetch_purchases(self,Username):
        if self.sql:
            qry = f"select * from purchases where username='{Username}'"
            self.mycursor.execute(qry)
            vals = [x for x in self.mycursor]
            return vals
        return []
            
data = DataClient()
