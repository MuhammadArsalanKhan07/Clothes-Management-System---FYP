import mydatabase
import datetime

class User:
    def __init__(self,username=None,password=None):
        self.__userid = None
        self.__username = username
        self.__password = password
        
    def get_userid(self):
        return self.__userid
        
    def get_username(self):
        return self.__username
    
    def get_password(self):
        return self.__password
    
    def set_userid(self,username,password):
        self.__userid = mydatabase.get_userid_from_user_table(username,password)
    
    def set_username(self,x):
        self.__username = x
        
    def set_password(self,y):
        self.__password = y
        
    def add_user(self,username,password):
        mydatabase.insert_user(username,password)
    
    def remove_user(self,username,password):
        mydatabase.delete_user(username,password)
        
    def select_user(self,username,password):
        if mydatabase.select_user(username,password):
            return True
        
    def select_username(self,username):
        if mydatabase.select_username(username):
            return True
    
    def get_all_users():
        rows = mydatabase.select_all_users()
        return rows
    
    def user_table_empty():
        if mydatabase.user_table_empty():
            return True
    
class Item:
 
    itemid = None 
    name = None
    brand = None
    category = None
    unitcost = None
    quantity = None 
    totalcost = None 
    date = datetime.date.today()
        
    def getall(tablename):
        """ Returns all rows from a db table """
        rows = mydatabase.select_all_items(tablename)
        return rows
        
    def search(tablename, itemid, name, brand, category, unitcost, quantity,
               totalcost, date):
        """ Returns all matching rows from a db table """
        rows = mydatabase.get_item(tablename, itemid, name, brand, category,
                                   unitcost, quantity, totalcost, date)
        return rows 
         
    def add(tablename, name, brand, category, unitcost, quantity,
            totalcost, date):
        """ Insert record into db table """
        mydatabase.insert_item(tablename, name, brand, category, unitcost, quantity,
                               totalcost, date)
        
    def update(tablename, name, brand, category, unitcost, quantity,
               totalcost, date, itemid):
        """ Updates row in a db table """
        mydatabase.update_item(tablename, name, brand, category, unitcost, quantity,
                               totalcost, date, itemid)
         
    def remove(tablename, itemid, name, brand, category, unitcost, quantity,
               totalcost, date):
        """ Deletes row in a db table"""
        mydatabase.delete_item(tablename, itemid, name, brand, category, unitcost,
                               quantity, totalcost, date) 
        
    def exists(tablename, itemid, name, brand, category, unitcost, quantity,
               totalcost, date):
        """ Returns True if a record exists in db table """
        if mydatabase.select_item(tablename, itemid, name, brand, category, unitcost, quantity,
                                  totalcost, date):
            return True
        
class Purchase(Item):
    pass 

class Stock(Item):
    pass 

class Sale(Item):
    pass 


