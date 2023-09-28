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

    def fetch_titles(self):
        #self.mycursor.execute("select Title from books")
        #list1 = [item[0] for item in self.mycursor]
        list1 = [name[:-4] for name in os.listdir("images\\covers")]
        random.shuffle(list1)
        return list1