from tkinter import * 
from tkinter import ttk
from tkinter import messagebox
from myclasses import *
import re
import daily_report
import weekly_report
import monthly_report
import yearly_report


def userWin():              # (User window) : Opens on "userButton" click. 
    top = Toplevel()
    top.title("Users")
    top.geometry("400x500")
    top.resizable(False,False)
    top.grab_set()
    top.focus_set()
    
    tree_frame = Frame(top)                 # Create Treeview Frame
    tree_frame.pack(pady=20,padx=10)

    tree_scroll = Scrollbar(tree_frame)     # Treeview Scrollbar
    tree_scroll.pack(side=RIGHT,fill=Y)
                                            # Create Treeview
    my_tree = ttk.Treeview(tree_frame,columns=(1,2,3),show="headings",
                           yscrollcommand=tree_scroll.set)
    my_tree.pack()
    
    tree_scroll.config(command=my_tree.yview)   # Configure the scrollbar
    
    my_tree.column(1,width=80)        # Formate my Columns
    my_tree.column(2,width=140)
    my_tree.column(3,width=140)
    
    my_tree.heading(1,text="ID",anchor=W)           #Create Headings
    my_tree.heading(2,text="Username",anchor=W)
    my_tree.heading(3,text="Password",anchor=W)
    
    def clicker(event):             # Binding function : clicker 
        # Clear entry boxes
        usernameEntry.delete(0,"end")
        passwordEntry.delete(0,"end")
        
        # Grab record number
        selected = my_tree.focus()
        
        # Grab record values
        values = my_tree.item(selected, "values")
        
        # Output to entry boxes
        usernameEntry.insert(0,values[1])
        passwordEntry.insert(0,values[2])
    
    my_tree.bind("<Double-1>", clicker) # Selects row on Double-click
    
    def remove_all():                       # Remove all records from my_tree
        for record in my_tree.get_children():
            my_tree.delete(record)
            
    def update_tree():                      # Update my_tree
        remove_all()
        rows = User.get_all_users()
        for row in rows:
            my_tree.insert(parent='',index='end',values=row)
            
    update_tree()
    
    usernameLabel = Label(top,text="Username",font="Calibri 25",width=10)
    usernameLabel.place(x=20,y=260)
    
    usernameEntry = Entry(top,bd=10,relief="sunken",justify="center",font="Calibri 14")
    usernameEntry.place(x=200,y=260,width=150,height=50)
    usernameEntry.focus_set()
    
    passwordLabel = Label(top,text="Password",font="Calibri 25",width=10)
    passwordLabel.place(x=20,y=320)
    
    passwordEntry = Entry(top,bd=10,relief="sunken",justify="center",show="*",font="Calibri 14")
    passwordEntry.place(x=200,y=320,width=150,height=50)
    
    regex = re.compile(r"[\[@_!#$%^&*()<>?/\|}{~:\]]")     # set of Special Characters.
    
    def add():
        if usernameEntry.get() and passwordEntry.get() != "":
            if(regex.search(passwordEntry.get()) != None):
                userobj = User()
                userobj.set_username(usernameEntry.get())
                userobj.set_password(passwordEntry.get())
                if userobj.select_username(userobj.get_username()) != True:
                    userobj.add_user(userobj.get_username(),userobj.get_password())
                    messagebox.showinfo("Record Info:","New User sucessfully added.")
                else:
                    messagebox.showerror("Error:","Username already exists.Try another one.")
            else:
                messagebox.showerror("Error:","Password must have a special character.")
        else:
            messagebox.showerror("Error:","Username and Password must not be empty.")
        
        usernameEntry.delete(0,"end")
        passwordEntry.delete(0,"end")
        usernameEntry.focus_set() 
        update_tree()
        
    def delete():
        if usernameEntry.get() and passwordEntry.get() != "": 
            userobj = User()
            userobj.set_username(usernameEntry.get())
            userobj.set_password(passwordEntry.get())
            if userobj.select_user(userobj.get_username(),userobj.get_password()):    #Checks if user exists in database.
                userobj.set_userid(userobj.get_username(),userobj.get_password())
                if userobj.get_userid() != 1:
                    userobj.remove_user(userobj.get_username(),userobj.get_password()) 
                    messagebox.showinfo("Record Info:","User deleted successfully.")
                else:
                    messagebox.showerror("Error","Admin user cannot be deleted.")
            else:
                messagebox.showerror("Error:","Invalid username and password.")
        else:
            messagebox.showerror("Error:","Username and Password must not be empty.")
            
        usernameEntry.delete(0,"end")
        passwordEntry.delete(0,"end")
        usernameEntry.focus_set()
        update_tree()
    
    addButton = Button(top,text="ADD",font="Calibri 20",width=10,command=add)
    addButton.place(x=30,y=380)
    
    delButton = Button(top,text="DELETE",font="Calibri 20",width=10,command=delete)
    delButton.place(x=220,y=380)
    
    exitButton = Button(top,text="EXIT",font="Calibri 20",width=10,command=top.destroy)
    exitButton.place(x=130,y=440)

def login():             # This function runs on "loginButton" click.

    regex = re.compile("[@_!#$%^&*()<>?/\|}{~:]")     # set of Special Characters.
    def add():
        if usernameEntry.get() and passwordEntry.get() != "":
            if(regex.search(passwordEntry.get()) != None):
                userobj = User()
                userobj.set_username(usernameEntry.get())
                userobj.set_password(passwordEntry.get())
                userobj.add_user(userobj.get_username(),userobj.get_password())
                userobj.set_userid(userobj.get_username(),userobj.get_password())
                messagebox.showinfo("Record Info:","New User sucessfully added as 'Admin' as there are no existing users.")
            else:
                messagebox.showerror("Error:","Password must have a special character.")
        else:
            messagebox.showerror("Error:","Username and Password must not be empty.")
        
        usernameEntry.delete(0,"end")
        passwordEntry.delete(0,"end")
        usernameEntry.focus_set() 
        
    if usernameEntry.get() and passwordEntry.get() != "":
        userobj = User()
        userobj.set_username(usernameEntry.get())
        userobj.set_password(passwordEntry.get())
        if User.user_table_empty():
            add()
            loginButton.config(state="disabled")
            stockButton.config(state="normal")
            reportButton.config(state="normal")
            userButton.config(state="normal")
        elif userobj.select_user(userobj.get_username(),userobj.get_password()):
            userobj.set_userid(userobj.get_username(),userobj.get_password())
            loginButton.config(state="disabled")
            stockButton.config(state="normal")
            reportButton.config(state="normal")
            if userobj.get_userid() == 1:
                userButton.config(state="normal")
            messagebox.showinfo("Record Info:","Login successful.")
        else:
                messagebox.showerror("Error:","Invalid username and password.")
                
        usernameEntry.delete(0,"end")
        passwordEntry.delete(0,"end")
        usernameEntry.focus_force()
    else:
        messagebox.showerror("Error:","Username and Password must not be empty.")

def stockWin():             # (Stock window) : Opens on "stockButton" click.
    top = Toplevel()
    top.title("Stock")
    top.geometry("1200x600") 
    top.resizable(False,False)
    top.grab_set()
    top.focus_set()
    
    tree_frame = Frame(top)         # Create Treeview Frame
    tree_frame.pack(pady=20,padx=10)
    
    tree_scroll = Scrollbar(tree_frame)     #Treeview Scrollbar
    tree_scroll.pack(side=RIGHT,fill=Y)
                                            # Create Treeview
    my_tree = ttk.Treeview(tree_frame,columns=(1,2,3,4,5,6,7,8),show="headings",
                           yscrollcommand=tree_scroll.set,selectmode="browse")
    my_tree.pack()
    
    tree_scroll.config(command=my_tree.yview)   # Configure the scrollbar
    
    my_tree.column(1,width=80)        # Formate my Columns
    my_tree.column(2,width=150)
    my_tree.column(3,width=150)
    my_tree.column(4,width=150)
    my_tree.column(5,width=150)
    my_tree.column(6,width=150)
    my_tree.column(7,width=150)
    my_tree.column(8,width=150)
    
    my_tree.heading(1,text="ID",anchor=W)       # Create Headings
    my_tree.heading(2,text="Name",anchor=W)
    my_tree.heading(3,text="Brand",anchor=W)
    my_tree.heading(4,text="Category",anchor=W)
    my_tree.heading(5,text="Unitcost",anchor=W)
    my_tree.heading(6,text="Quantity",anchor=W)
    my_tree.heading(7,text="Totalcost",anchor=W)
    my_tree.heading(8,text="Date",anchor=W)
    
    
    def clicker(event):             # Binding function : clicker 
        # Clear entry boxes
        identry.delete(0,"end")
        nameentry.delete(0,"end")
        brandentry.delete(0,"end")
        categoryentry.delete(0,"end")
        unitcostentry.delete(0,"end")
        quantityentry.delete(0,"end")
        totalcostentry.delete(0,"end")
        dateentry.delete(0,"end")
        
        # Grab record number
        selected = my_tree.focus()
        
        # Grab record values
        values = my_tree.item(selected, "values")
        
        # Output to entry boxes
        identry.insert(0,values[0])
        nameentry.insert(0,values[1])
        brandentry.insert(0,values[2])
        categoryentry.insert(0,values[3])
        unitcostentry.insert(0,values[4])
        quantityentry.insert(0,values[5])
        totalcostentry.insert(0,values[6])
        dateentry.insert(0,values[7])
    
    my_tree.bind("<Double-1>", clicker) # Selects row on Double-click
    
    def remove_all():               # Remove all records from my_tree
        for record in my_tree.get_children():
            my_tree.delete(record)
            
    def update_tree():              # Update my_tree
        remove_all()
        rows = Stock.getall("Stock")
        for row in rows:
            my_tree.insert(parent="",index="end",values=row)
    
    update_tree()
                              
    def tree_search_update(rows):
        remove_all()
        for i in rows:
            my_tree.insert(parent="",index="end",values=i)
            
    def add():
        if (nameentry.get() and brandentry.get() and categoryentry.get() and unitcostentry.get() and
            quantityentry.get() != ""):
            
            totalcost = int(unitcostentry.get()) * int(quantityentry.get())
            
            Purchase.add("Purchase",nameentry.get(), brandentry.get(), categoryentry.get(), 
                         unitcostentry.get(), quantityentry.get(), totalcost, Purchase.date)
            
            Stock.add("Stock",nameentry.get(), brandentry.get(), categoryentry.get(), 
                         unitcostentry.get(), quantityentry.get(), totalcost, Stock.date)
            
            messagebox.showinfo("Record Info:","New Purchase added to Stock.")
        else:
            messagebox.showerror("Error:","All fields except ID,Totalcost,Date must not be empty.")
            
        clear()
        itementry.focus_set() 
        
    def delete():
        if (identry.get(), nameentry.get(), brandentry.get(), categoryentry.get(), unitcostentry.get(),
            quantityentry.get(), totalcostentry.get(), dateentry.get() != ""):
            
            
            if Stock.exists("Stock",identry.get(), nameentry.get(), brandentry.get(), categoryentry.get(),
                            unitcostentry.get(), quantityentry.get(), totalcostentry.get(), dateentry.get()):
                
                newunitcost = ((40/100) * float(unitcostentry.get())) + float(unitcostentry.get())
                newtotalcost = newunitcost * float(quantityentry.get())
                
                Sale.add("Sale",nameentry.get(), brandentry.get(), categoryentry.get(), 
                         newunitcost, quantityentry.get(), newtotalcost, Sale.date) 
                
                Stock.remove("Stock", identry.get(), nameentry.get(), brandentry.get(), categoryentry.get(),
                             unitcostentry.get(), quantityentry.get(), totalcostentry.get(), dateentry.get())
                
                
                messagebox.showinfo("Record Info:","Item added to Sale and deleted from Stock.")
            else:
                messagebox.showerror("Error:","No Record.")
                
        else:
            messagebox.showerror("Error:","All fields must not be empty.")
            
        clear()
        nameentry.focus_set() 
            
    def update_record():
        if (identry.get(), nameentry.get(), brandentry.get(), categoryentry.get(), unitcostentry.get(),
            quantityentry.get(), totalcostentry.get(), dateentry.get() != ""):
            
            Purchase.update("Purchase", nameentry.get(), brandentry.get(), categoryentry.get(), unitcostentry.get(),
                           quantityentry.get(), totalcostentry.get(), dateentry.get(), identry.get())
            
            Stock.update("Stock", nameentry.get(), brandentry.get(), categoryentry.get(), unitcostentry.get(),
                           quantityentry.get(), totalcostentry.get(), dateentry.get(), identry.get())
            
            messagebox.showinfo("Record Info:","Item updated in Purchase and Stock.")
            clear()
        else:
            messagebox.showerror("Error:","All fields must not be empty.")
            
    def search():
        rows = Stock.search("Stock",identry.get(), nameentry.get(), brandentry.get(), categoryentry.get(),
                            unitcostentry.get(), quantityentry.get(), totalcostentry.get(), dateentry.get())
        tree_search_update(rows)
    
    def clear():
        update_tree()
        identry.delete(0,"end")
        nameentry.delete(0,"end")
        brandentry.delete(0,"end")
        categoryentry.delete(0,"end")
        unitcostentry.delete(0,"end")
        quantityentry.delete(0,"end")
        totalcostentry.delete(0,"end")
        dateentry.delete(0,"end")
        
    idlabel = Label(top,text="ID",font="Calibri 25",width=10)
    idlabel.place(x=20,y=260)
    
    identry = Entry(top,bd=10,relief="sunken",justify="center",font="Calibri 14")
    identry.place(x=200,y=260,width=150,height=50)
    
    namelabel = Label(top,text="Name",font="Calibri 25",width=10)
    namelabel.place(x=20,y=320)
    
    nameentry = Entry(top,bd=10,relief="sunken",justify="center",font="Calibri 14")
    nameentry.place(x=200,y=320,width=150,height=50)
    
    brandlabel = Label(top,text="Brand",font="Calibri 25",width=10)
    brandlabel.place(x=350,y=260)
    
    brandentry = Entry(top,bd=10,relief="sunken",justify="center",font="Calibri 14")
    brandentry.place(x=500,y=260,width=150,height=50)
    
    categorylabel = Label(top,text="Category",font="Calibri 25",width=10)
    categorylabel.place(x=330,y=320)
    
    categoryentry = Entry(top,bd=10,relief="sunken",justify="center",font="Calibri 14")
    categoryentry.place(x=500,y=320,width=150,height=50)
    
    unitcostlabel = Label(top,text="Unitcost",font="Calibri 25")
    unitcostlabel.place(x=360,y=380)
    
    unitcostentry = Entry(top,bd=10,relief="sunken",justify="center",font="Calibri 14")
    unitcostentry.place(x=500,y=380,width=150,height=50)
    
    quantitylabel = Label(top,text="Quantity",font="Calibri 25")
    quantitylabel.place(x=700,y=260)
    
    quantityentry = Entry(top,bd=10,relief="sunken",justify="center",font="Calibri 14")
    quantityentry.place(x=850,y=260,width=150,height=50)
    
    totalcostlabel = Label(top,text="Totalcost",font="Calibri 25")
    totalcostlabel.place(x=700,y=320)
    
    totalcostentry = Entry(top,bd=10,relief="sunken",justify="center",font="Calibri 14")
    totalcostentry.place(x=850,y=320,width=150,height=50)
    
    datelabel = Label(top,text="Date",font="Calibri 25")
    datelabel.place(x=730,y=380) 
    
    dateentry = Entry(top,bd=10,relief="sunken",justify="center",font="Calibri 14")
    dateentry.place(x=850,y=380,width=150,height=50)
    
    
    
    addbtn = Button(top,text="Add",font="Calibri 20",width=10,command=add)
    addbtn.place(x=30,y=400)
    
    delbtn = Button(top,text="Delete",font="Calibri 20",width=10,command=delete)
    delbtn.place(x=190,y=400)
    
    updatebtn = Button(top,text="Update",font="Calibri 20",width=10,command=update_record)
    updatebtn.place(x=30,y=470)
    
    srchbtn = Button(top,text="Search",font="Calibri 20",width=10,command=search)
    srchbtn.place(x=190,y=470)
    
    clrbtn = Button(top,text="Clear",font="Calibri 20",width=10,command=clear)
    clrbtn.place(x=370,y=470)
    
    exitButton = Button(top,text="EXIT",font="Calibri 20",width=10,command=top.destroy)
    exitButton.place(x=530,y=470)
    
    def purchasewin():
        top = Toplevel()
        top.title("Purchase")
        top.geometry("1200x400") 
        top.resizable(False,False)
        top.grab_set()
        top.focus_set()
        
        tree_frame = Frame(top)         # Create Treeview Frame
        tree_frame.pack(pady=20,padx=10)
        
        tree_scroll = Scrollbar(tree_frame)     #Treeview Scrollbar
        tree_scroll.pack(side=RIGHT,fill=Y)
                                                # Create Treeview
        my_tree = ttk.Treeview(tree_frame,columns=(1,2,3,4,5,6,7,8),show="headings",
                               yscrollcommand=tree_scroll.set,selectmode="browse")
        my_tree.pack()
        
        tree_scroll.config(command=my_tree.yview)   # Configure the scrollbar
        
        my_tree.column(1,width=80)        # Formate my Columns
        my_tree.column(2,width=150)
        my_tree.column(3,width=150)
        my_tree.column(4,width=150)
        my_tree.column(5,width=150)
        my_tree.column(6,width=150)
        my_tree.column(7,width=150)
        my_tree.column(8,width=150)
        
        my_tree.heading(1,text="ID",anchor=W)       # Create Headings
        my_tree.heading(2,text="Name",anchor=W)
        my_tree.heading(3,text="Brand",anchor=W)
        my_tree.heading(4,text="Category",anchor=W)
        my_tree.heading(5,text="Unitcost",anchor=W)
        my_tree.heading(6,text="Quantity",anchor=W)
        my_tree.heading(7,text="Totalcost",anchor=W)
        my_tree.heading(8,text="Date",anchor=W)
        
        def remove_all():               # Remove all records from my_tree
            for record in my_tree.get_children():
                my_tree.delete(record)
                
        def update_tree():              # Update my_tree
            remove_all()
            rows = Purchase.getall("Purchase")
            for row in rows:
                my_tree.insert(parent="",index="end",values=row)
        
        update_tree()
        
    def salewin():
        top = Toplevel()
        top.title("Sale")
        top.geometry("1200x400") 
        top.resizable(False,False)
        top.grab_set()
        top.focus_set()
        
        tree_frame = Frame(top)         # Create Treeview Frame
        tree_frame.pack(pady=20,padx=10)
        
        tree_scroll = Scrollbar(tree_frame)     #Treeview Scrollbar
        tree_scroll.pack(side=RIGHT,fill=Y)
                                                # Create Treeview
        my_tree = ttk.Treeview(tree_frame,columns=(1,2,3,4,5,6,7,8),show="headings",
                               yscrollcommand=tree_scroll.set,selectmode="browse")
        my_tree.pack()
        
        tree_scroll.config(command=my_tree.yview)   # Configure the scrollbar
        
        my_tree.column(1,width=80)        # Formate my Columns
        my_tree.column(2,width=150)
        my_tree.column(3,width=150)
        my_tree.column(4,width=150)
        my_tree.column(5,width=150)
        my_tree.column(6,width=150)
        my_tree.column(7,width=150)
        my_tree.column(8,width=150)
        
        my_tree.heading(1,text="ID",anchor=W)       # Create Headings
        my_tree.heading(2,text="Name",anchor=W)
        my_tree.heading(3,text="Brand",anchor=W)
        my_tree.heading(4,text="Category",anchor=W)
        my_tree.heading(5,text="Unitcost",anchor=W)
        my_tree.heading(6,text="Quantity",anchor=W)
        my_tree.heading(7,text="Totalcost",anchor=W)
        my_tree.heading(8,text="Date",anchor=W)
        
        def remove_all():               # Remove all records from my_tree
            for record in my_tree.get_children():
                my_tree.delete(record)
                
        def update_tree():              # Update my_tree
            remove_all()
            rows = Sale.getall("Sale")
            for row in rows:
                my_tree.insert(parent="",index="end",values=row)
        
        update_tree()
    
    purchasetable = Button(top,text="View Purchases",font="Calibri 20",width=15,command=purchasewin)
    purchasetable.place(x=730,y=470)
    
    saletable = Button(top,text="View Sales",font="Calibri 20",width=10,command=salewin)
    saletable.place(x=960,y=470) 
    
def reset():                     # This function runs on "resetButton" click.
    usernameEntry.delete(0,"end")
    passwordEntry.delete(0,"end")
    usernameEntry.focus_force()
    
    stockButton.config(state="disabled")
    reportButton.config(state="disabled")
    userButton.config(state="disabled")
    loginButton.config(state="normal")
    
    messagebox.showinfo("Record Info:","Logout successful.")
    
def reportWin():            # (Report window) : Opens on "reportButton" click. 
    top = Toplevel()
    top.title("Reports")
    top.geometry("450x300")
    top.resizable(False,False)
    top.grab_set()
    top.focus_set()
    
    def gen_daily():
        daily_report.generate()
    
    def gen_weekly():
        weekly_report.generate()
        
    def gen_monthly():
        monthly_report.generate()
        
    def gen_yearly():
        yearly_report.generate()
    
    daily = Button(top,text="Daily Report",font="Calibri 20",width=12,command=gen_daily)
    daily.place(x=10,y=30)
    
    weekly = Button(top,text="Weekly Report",font="Calibri 20",width=12,command=gen_weekly)
    weekly.place(x=250,y=30)
    
    monthly = Button(top,text="Monthly Report",font="Calibri 20",width=13,command=gen_monthly)
    monthly.place(x=10,y=130)
    
    yearly = Button(top,text="Yearly Report",font="Calibri 20",width=12,command=gen_yearly)
    yearly.place(x=250,y=130)
    
    exitButton = Button(top,text="Exit",font="Calibri 20",width=12,command=top.destroy)
    exitButton.place(x=130,y=220)
    

        

#################################### MAIN APPLICATION WINDOW ####################################
   
  
root = Tk()                        # "root" is the Main window of GUI application.
root.title("Clothes Management System")
root.geometry("600x400")
root.resizable(False,False)
root.focus_force()


cmsLabel = Label(root,text="Clothes  Management  System",bg="skyblue",
                 bd=10,relief="ridge",font="Calibri 30 bold")
cmsLabel.pack(fill=X)

usernameLabel = Label(root,text="Username",fg="blue",font="Calibri 25",width=10)
usernameLabel.place(x=40,y=90)

usernameEntry = Entry(root,bd=10,relief="sunken",bg="yellow",justify="center",font="Calibri 14")
usernameEntry.place(x=300,y=90,width=220,height=50)
usernameEntry.focus_force()

passwordLabel = Label(root,text="Password",font="Calibri 25",width=10)
passwordLabel.place(x=40,y=140)

passwordEntry = Entry(root,bd=10,relief="sunken",justify="center",show="*",font="Calibri 14")
passwordEntry.place(x=300,y=140,width=220,height=50)

loginButton = Button(root,text="Login",font="Calibri 20",width=12,command=login)
loginButton.place(x=50,y=230)

resetButton = Button(root,text="Reset/Logout",font="Calibri 20",width=10,command=reset)
resetButton.place(x=230,y=230)

exitwinButton = Button(root,text="Exit Window",font="Calibri 20",width=10,command=root.destroy)
exitwinButton.place(x=380,y=230)

stockButton = Button(root,text="Clothes Stock",font="Calibri 20",width=12,command=stockWin)
stockButton.place(x=50,y=300)

reportButton = Button(root,text="Reports",font="Calibri 20",width=10,command=reportWin)
reportButton.place(x=230,y=300)

userButton = Button(root,text="Users",font="Calibri 20",width=10,command=userWin)
userButton.place(x=380,y=300)

stockButton.config(state="normal")
reportButton.config(state="normal")       
userButton.config(state="normal")

root.mainloop()