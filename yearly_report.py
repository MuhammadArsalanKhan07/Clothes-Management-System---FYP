from tkinter import *
import datetime
from fpdf import FPDF  # pip install fpdf
import sqlite3

def generate():
    
    conn = sqlite3.connect("myDB.db")
    c = conn.cursor()

    today = datetime.date.today()
    year_ago = today - datetime.timedelta(days=365)

    with conn:
        c.execute("SELECT SUM(Totalcost) FROM Purchase WHERE Date BETWEEN (?) AND (?)",[year_ago,today])
        rows = c.fetchall()
        totalpurprice = rows[0][0]

    with conn:
        c.execute("SELECT SUM(Totalcost) FROM Sale WHERE Date BETWEEN (?) AND (?)",[year_ago,today])
        rows = c.fetchall()
        totalsprice = rows[0][0]
    
    profit = 0.0
    if totalpurprice != None and totalsprice != None:
        profit = totalsprice - totalpurprice
    
    with conn:
        c.execute("SELECT COUNT(*) FROM Purchase WHERE Date BETWEEN (?) AND (?)",[year_ago,today])
        count = c.fetchall()
        totalpurchases = count[0][0]
    
    with conn:
        c.execute("SELECT COUNT(*) FROM Sale WHERE Date BETWEEN (?) AND (?)",[year_ago,today])
        count = c.fetchall()
        totalsales = count[0][0]
    
    with conn:
        c.execute("SELECT COUNT(*) FROM Stock WHERE Date BETWEEN (?) AND (?)",[year_ago,today])
        count = c.fetchall()
        totalstock = count[0][0]
    
        reports = f"""
            \t\t\t\tProfit Report:
                      
            \t\t\t\tTotal Purchase Price = {totalpurprice}
            \t\t\t\tTotal Sale Price     = {totalsprice}
            \t\t\t\tProfit               = {profit}
                      
                           
            \t\t\t\tStock Report:
                      
            \t\t\t\tTotal Purchases = {totalpurchases}
            \t\t\t\tTotal Sales     = {totalsales}
            \t\t\t\tTotal Stock     = {totalstock}
                  """
    
    with conn:
        c.execute("SELECT * FROM Purchase WHERE Date BETWEEN (?) AND (?)",[year_ago,today])
        purchaserows = c.fetchall()
    
    with conn:
        c.execute("SELECT * FROM Sale WHERE Date BETWEEN (?) AND (?)",[year_ago,today])
        salerows = c.fetchall()
    
    with conn:
        c.execute("SELECT * FROM Stock WHERE Date BETWEEN (?) AND (?)",[year_ago,today])
        stockrows = c.fetchall()
    
    # Creating and writing to text file
    f = open(f"yearly-{today}.txt", "w")
    
    f.write(reports)
    
    f.write("\n\t\t\t\tPurchase Records:\n")
    for row in purchaserows:
        r = str(row)
        f.write(f"\t\t{r} \n")
    
    f.write("\n\t\t\t\tSale Records:\n")
    for row in salerows:
        r = str(row)
        f.write(f"\t\t{r} \n")
    
    f.write("\n\t\t\t\tStock Records:\n")
    for row in stockrows:
        r = str(row)
        f.write(f"\t\t{r} \n")
    
    
    #Creating and writing to pdf file
    pdf = FPDF()       # pdf object
    
    # Add a page
    pdf.add_page()
       
    # set style and size of font 
    # that you want in the pdf
    pdf.set_font("Arial", size = 15)
      
    # open the text file in read mode
    f = open(f"yearly-{today}.txt", "r")
      
    # insert the texts in pdf
    for x in f:
        pdf.cell(200, 10, txt = x, ln = 1, align = 'C')
       
    # save the pdf with name .pdf
    pdf.output(f"yearly-{today}.pdf")
    
    
    ##################################################################################
    
    top = Toplevel()
    top.title("Yearly Report")
    top.geometry("800x750")
    top.resizable(False,False)
    top.grab_set()
    top.focus_set()
    
    
    T = Text(top, height = 500, width = 520)
    T.pack(fill="both", expand=TRUE)
     
    f = open(f"yearly-{today}.txt", "r")
    
    T.insert("end", f.read())
    
   
    

