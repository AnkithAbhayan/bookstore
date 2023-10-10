#import mysql.connector as con
import os
import random

class DataClient:
    def __init__(self):
        """
        self.mycon = con.connect(host='Localhost',user='root',password='HariOm@123',database='12C23')
        self.mycursor = self.mycon.cursor()
        if self.mycon.is_connected():
            print("connected successfully")
        """

    def fetch_titles(self,price=False):
        """
        self.mycursor.execute("select Title,Price from books")
        list1 = [item for item in self.mycursor]
        random.shuffle(list1)
        titles = [item[0] for item in list1]
        price = [item[1] for item in list1]

        if price:
            return titles, price
        return titles
        """
        list1 = [(name[:-4],random.randint(100,200)) for name in os.listdir("images/covers")]
        random.shuffle(list1)
        titles = [item[0] for item in list1]
        prices = [item[1] for item in list1]
        if price:
            return titles, prices
        return titles
        
    def fetch_prices(self,titles):
        prices = [random.randint(100, 1000) for item in titles]
        """
        for item in titles:
            self.mycursor.execute(f"select Price from books where Title={item}")
            prices.append(self.mycursor[0])
        return prices
        """ 