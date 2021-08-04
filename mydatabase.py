import sqlite3

conn = sqlite3.connect("myDB.db")
c = conn.cursor()

"""                                     User Table queries """

def insert_user(username,password):
    with conn:
        c.execute("INSERT INTO User (Username,Password) VALUES (?,?)", [username,password])
    
def delete_user(username,password):
    with conn:
        c.execute("DELETE FROM User WHERE Username=(?) AND Password=(?)",[username,password])
        
def select_user(username,password):
    with conn:
        c.execute("SELECT * FROM User WHERE Username=(?) AND Password=(?)",[username,password])
        if c.fetchall():
            return True
        
def select_username(username):
    with conn:
        c.execute("SELECT * FROM User WHERE Username=(?)",[username])
        if c.fetchall():
            return True
    
def select_all_users():
    with conn:
        c.execute("SELECT * FROM User")
        rows = c.fetchall()
        return rows
    
def user_table_empty():
    with conn:
        c.execute("SELECT COUNT(*) FROM User")
        count = c.fetchall() 
        if count[0][0]==0:
            return True
        
def get_userid_from_user_table(username,password):
    with conn:
        c.execute("SELECT ID FROM User WHERE Username=(?) and Password=(?)",[username,password])
        row = c.fetchall()  
        userid = row[0][0]
        return userid

"""                                 Item queries """

def select_all_items(tablename):
    with conn:
        c.execute(f"SELECT * FROM {tablename}")
        rows = c.fetchall()
        return rows

def get_item(tablename, itemid, name, brand, category, unitcost, quantity,
             totalcost, date):
    with conn:
        c.execute(f"""SELECT * FROM {tablename} WHERE ID=(?) OR Name=(?) OR Brand=(?) OR Category=(?) 
                  OR Unitcost=(?) OR Quantity=(?) OR Totalcost=(?) OR Date=(?)""",
                  [itemid, name, brand, category, unitcost, quantity,
                   totalcost, date])
        rows = c.fetchall()
        return rows

def insert_item(tablename, name, brand, category, unitcost, quantity,
                               totalcost, date):
    with conn:
        c.execute(f"""INSERT INTO {tablename} (Name,Brand,Category,Unitcost,Quantity,Totalcost,Date) 
                  VALUES (?,?,?,?,?,?,?)""", [name, brand, category, unitcost, quantity,
                  totalcost, date])    
                  
def update_item(tablename, name, brand, category, unitcost, quantity,
                totalcost, date, itemid):
    with conn:
        c.execute(f"""UPDATE {tablename} SET Name=(?), Brand=(?), Category=(?), Unitcost=(?), Quantity=(?), 
                  Totalcost=(?), Date=(?) WHERE ID=(?)""",
                  [name, brand, category, unitcost, quantity,
                   totalcost, date, itemid])

def delete_item(tablename, itemid, name, brand, category, unitcost,
                quantity, totalcost, date):
    with conn:
        c.execute(f"""DELETE FROM {tablename} WHERE ID=(?) AND Name=(?) AND Brand=(?) AND Category=(?) 
                  AND Unitcost=(?) AND Quantity=(?) AND Totalcost=(?) AND Date=(?)""",
                  [itemid, name, brand, category, unitcost,
                   quantity, totalcost, date]) 
            
def select_item(tablename, itemid, name, brand, category, unitcost, quantity,
                totalcost, date):
    with conn:
        c.execute(f"""SELECT * FROM {tablename} WHERE ID=(?) AND Name=(?) AND Brand=(?) AND Category=(?) 
                  AND Unitcost=(?) AND Quantity=(?) AND Totalcost=(?) AND Date=(?)""",
                  [itemid, name, brand, category, unitcost, quantity,
                   totalcost, date]) 
        if c.fetchall():
            return True 
 




