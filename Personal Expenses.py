from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector as ms
import time

window = Tk()
window.title("Personal Expenses")
window.geometry("700x500+350+100")


DB = ms.connect(host = "localhost", user = "root", password = "admin")
cursor = DB.cursor()

# Creating Database
cursor.execute("create database if not exists expenses")
cursor.execute("use expenses")

# Creating Table in Database
sql_command_1 = '''
               create table if not exists record(
               Item char(20),
               Price float,
               Paid float,
               Debt float,
               Message varchar(50),
               Date_ date,
               Total float,
               Total_debt float
               )
               '''     
cursor.execute(sql_command_1)

#Creating Variables for tkinter
itemName = StringVar()
price = StringVar()
paid = StringVar()
debt = StringVar()
message = StringVar()
date = StringVar()
total = StringVar()

# Setting some default values
debt.set("0")
message.set("-")

def reset_entry_vars():     
     itemName.set("")     
     price.set("")
     paid.set("")
     debt.set("0")
     message.set("-")
     date.set("")

def show_data():
    cursor.execute('select * from record')
    data = cursor.fetchall()
    count = cursor.rowcount

    window.geometry("900x600+350+100")

    #========Creating Frame for treeview=========#
    frame=Frame(window,bg='ghost white',relief=RIDGE,borderwidth=5)
    frame.place(x=0,y=0,width=900,height=600)

    Button(frame, text='Back', width=140, font=("",12), bg='black', fg='white', command=lambda: frame.destroy()).pack()

    # Theme and Fonts for table
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview.Heading",font=('Arial',15))
    style.configure("Treeview",background='#D3D3D3',foreground='black',fieldbackground='silver',
                   rowheight=25, font=('arial',12))
     
    #==========Scrollbar for treeview============#
    scroll_y=ttk.Scrollbar(frame,orient=VERTICAL)
    scroll_y.pack(side=RIGHT,fill=Y)
    
    #==========Treeview==========#
    tree = ttk.Treeview(frame,columns=('Item_Name','Price','Paid','Debt','Message','Date',
                                       'Total','Total_Debt'),yscrollcommand=scroll_y.set)
     
    scroll_y.config(command=tree.yview)
    
    tree.heading("Item_Name",text="Item_Name")
    tree.heading("Price",text="Price")
    tree.heading("Paid",text="Paid")
    tree.heading("Debt",text="Debt")
    tree.heading("Message",text="Message")
    tree.heading("Date",text="Date")
    tree.heading("Total",text="Total")
    tree.heading("Total_Debt",text="Total_Debt")

    tree.column('#0', width=0, stretch=NO)
    tree.column('Item_Name', width=70, minwidth=70, anchor=CENTER)
    tree.column('Price', width=50,  minwidth=50, anchor=CENTER)
    tree.column('Paid', width=50, minwidth=50, anchor=CENTER)
    tree.column('Debt', width=50,  minwidth=50, anchor=CENTER)
    tree.column('Message', width=50, minwidth=50, anchor=CENTER)
    tree.column('Date', width=50, minwidth=50, anchor=CENTER)
    tree.column('Total', width=50, minwidth=50,anchor=CENTER)
    tree.column('Total_Debt', width=50, minwidth=50,anchor=CENTER)
     
    tree.pack(fill=BOTH,expand=1)

    for row in data:
         date = str(row[6])
         tree.insert('',END,values=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]])
    
def insert_data(data):

    cursor.execute('select total from record')
    previous_sum = cursor.fetchall()
    count1 = cursor.rowcount

    cursor.execute('select total_debt from record')
    debt = cursor.fetchall()
    #print(debt)
    count2 = cursor.rowcount
    debt_sum = float(debt[count2-1][0]) + float(data[3])

    total = str(float(previous_sum[count1-1][0]) + float(data[2]) + float(data[3]))

    # - data[0] = itemName
    # - data[1] = price
    # - data[2] = paid
    # - data[3] = debt
    # - data[4] = message
    # - data[5] = date
    sql_command=f'''insert into record values('{data[0]}',{data[1]},{data[2]},{data[3]},'{data[4]}',
    {data[5]},{total},{debt_sum})'''
    cursor.execute(sql_command)
    DB.commit()

def extract_data():
    data = [itemName.get(), price.get(), paid.get(), debt.get(), message.get(), date.get()]

    insert_data(data)
    reset_entry_vars()

def structure():

    window.geometry("720x520+350+100")

    #Window Heading 
    heading = Label(window, text="My Personal Expenses", font=('',25))
    heading.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky='ns')

    # Item at
    # row = 1, column = 0,1
    Label(window, text="Item name : ", font=('',20), width=10).grid(row=1, column=0, padx=10, pady=10)
    Entry(window, font=('',20), width=20, textvariable=itemName).grid(row=1, column=1, padx=10, pady=10)

    # Price of item at
    # row = 2, column = 0,1
    Label(window, text="Price : ", font=('',20), width=10).grid(row=2, column=0, padx=10, pady=10)
    Entry(window, font=('',20), width=20, textvariable=price).grid(row=2, column=1, padx=10, pady=10)

    # Paid of item, my contribution
    # row = 3, column = 0,1
    Label(window, text="Paid : ", font=('',20), width=10).grid(row=3, column=0, padx=10, pady=10)
    Entry(window, font=('',20), width=20, textvariable=paid).grid(row=3, column=1, padx=10, pady=10)

    # Debt amount if any at
    # row = 4, column = 0,1
    Label(window, text="Debt : ", font=('',20), width=10).grid(row=4, column=0, padx=10, pady=10)
    Entry(window, font=('',20), width=20, textvariable=debt).grid(row=4, column=1, padx=10, pady=10)

    # Debt to person or message(if any) at
    # row = 5, column = 0,1
    Label(window, text="Message : ", font=('',20), width=10).grid(row=5, column=0, padx=10, pady=10)
    Entry(window, font=('',20), width=20, textvariable=message).grid(row=5, column=1, padx=10, pady=10)

    # Date of expenditure
    # row = 6, column = 0,1
    Label(window, text="Date : ", font=('',20), width=10).grid(row=6, column=0, padx=10, pady=10)
    Entry(window, font=('',20), width=20, textvariable=date).grid(row=6, column=1, padx=10, pady=10)

    # Save and show buttons at
    # row = 7, column = 0,1

    # --- save button calls extract_data() to get data
    save_button = Button(window, text="Save", font=('',20), width=15, command=extract_data)
    save_button.grid(row=7, column=0, padx=40, pady=10)

    show_button = Button(window, text="Show", font=('',20), width=15, command=show_data)
    show_button.grid(row=7, column=1, padx=10, pady=10)

    
structure()

window.mainloop()





































