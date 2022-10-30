from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector as ms
import time

DB = ms.connect(host = "localhost", user = "root", password = "admin")
cursor = DB.cursor()

#=======Create GUI window========#
window = Tk()
window.geometry("1535x805")
window.title('Passenger List Management')
window.minsize(500,500)
window.maxsize(1600,900)
window.configure(background="#BDB76B")

#========Define variables========#
Ticket = StringVar()
Name = StringVar()
Age = StringVar()
Gender = StringVar()
Contact = StringVar()
Destination = StringVar()
Date_r = StringVar()
Ticket.set("Tx_")
Date_r.set("Enter date like DD/MM/YYYY")

date = time.strftime("%d/%m/%Y")

#================= CREATING DATABASE ==================#
cursor.execute("create database if not exists plm_gui")
cursor.execute("use plm_gui")

#=============Creating Table in Database===============#
sql_command_1 = '''
               create table if not exists record(
               Ticket_ID char(20),
               Name varchar(25),
               Age char(3),
               Gender char(10),
               Contact char(15),
               Destination varchar(30),
               Date_ date)
               '''     
cursor.execute(sql_command_1)

def get_Ticket_number(x):
     c = x[3:]
     d = int(c)
     x = TicketID_generate(d)
     return x

def TicketID_generate(i=0):     
     Ticket_ID = "Tx_"+str(i+1)     
     return Ticket_ID

def checkID():
     global DB,cursor
     cursor.execute("use plm_gui")
     cursor.execute("select * from record")
     data = cursor.fetchall()
     count = cursor.rowcount
     if count == 0:
          a = TicketID_generate()
          return a
     
     else:
          for row in data:
               pass
          b = get_Ticket_number(row[0])
          return b

def empty(e):
     Date_r.set('')

def exit_():
     window.destroy()

def create_date(x):
     c = ''
     for i in range(len(x)):
          b = ord(x[i])
          if b in range(48,58):
               c = c+x[i]
     w = c[4:]+c[2:4]+c[:2]
     return int(w)

def create_frame():
     #============creating frame============#
     frame=Frame(window,relief=RIDGE,borderwidth=5)
     frame.place(x=360,y=150,width=1080,height=600)
      
     Label(frame,text="Today's Date : "+date,font=("Forte",15)).pack(anchor='w')     
     Label(frame,text="Connected to Database",font=('Script MT Bold',55)).pack(pady=10)
     Label(frame,text="'plm_gui'.",font=('Script MT Bold',45),fg='#800000').pack()
     Label(frame,text='Tabel name : ',font=('Calisto MT',20)).pack(anchor='w',pady=40,padx=10)
     Label(frame,text='record',font=('Calisto MT',20),fg='Blue').place(x=180,y=259)
     Label(frame,text='Fields : ',font=('Calisto MT',20)).pack(anchor='w',padx=10,pady=40)
     Label(frame,text='Ticket_ID, Name, Age, Gender, Contact, Destination, Date.',
           font=('Calisto MT',20),fg='Blue').place(x=110,y=377)

def check_info(k,TicketID,name,age,gender,contact,destination,date):
     if k == 1:
          if len(TicketID) <= 3 :
               messagebox.showerror("*ERROR*","Invalid Ticket ID.")
          elif name == '':
               messagebox.showinfo("*Not Found*","Enter name of the passenger.")
               return True
          elif age == '':
               messagebox.showinfo("*Not Found*","Enter age of the passenger.")
               return True
          elif gender == '':
               messagebox.showinfo("*Not Found*","Enter gender of the passenger.")
               return True
          elif contact == '':
               messagebox.showinfo("*Not Found*","Enter contact number of the passenger.")
               return True
          elif len(contact) != 10:
               messagebox.showerror("*ERROR*","Enter correct contact number.")
               return True
          elif destination == '':
               messagebox.showinfo("*Not Found*","Enter destination of the passenger.")
               return True

     elif k == 2:
          if len(TicketID)<=3 and name=='' and age=='' and gender=='' and contact=='' and destination=='' and len(date)==0:
               messagebox.showerror("*Not Found*","Any one field must filled to retrive data.")
               return True
          elif len(contact)>0 and len(contact) != 10:
               messagebox.showerror("*ERROR*","Enter correct contact number.")
               return True
     elif k == 3:
          if len(TicketID)<=3:
               messagebox.showerror("*Not Found*","Enter Ticket ID.")
               return True
          if name=='' and age=='' and gender=='' and contact=='' and destination=='':
               messagebox.showerror("*Not Found*","Enter new data to which old data is to be updated")
               return True
          elif len(contact)>0 and len(contact) != 10:
               messagebox.showerror("*ERROR*","Enter correct contact number.")
               return True
def reset():     
     Destination.set("")     
     Contact.set("")
     Gender.set("")
     Age.set("")
     Name.set("")
     Ticket.set("Tx_")
     Date_r.set("Enter date like DD/MM/YYYY")

def delete_data():
     TicketID = Ticket.get()

     message = '''Details of the passenger with ID "%s" will be deleted and cannot be retrive again.
Are you sure that you want to delete the data?'''%(TicketID)
     
     a = messagebox.askyesno("*Warning*",message)
     if a == 1:
          delete_command = "delete from record where Ticket_ID like '%s'"%(TicketID)
          cursor.execute(delete_command)
          DB.commit()
     elif a == 0:
          delete_interface()
     reset()
     
def update_data():     
     TicketID = Ticket.get()
     name = Name.get()
     age = Age.get()
     gender = Gender.get()
     contact = Contact.get()
     destination = Destination.get()

     a = check_info(3,TicketID,name,age,gender,contact,destination,None)
     
     update_command = "update record set "
     i=0
     if a == True:
          interface(3)
     else:
          if len(name) != 0:
               update_command = update_command + 'Name = "%s"'
               update_command = update_command%(name)
               i += 1
               
          if len(age) != 0:
               if i > 0:
                    update_command = update_command + ',Age = "%s"'
               else:
                    update_command = update_command + 'Age = "%s"'
               update_command = update_command%(age)
               i += 1
               
          if len(gender) != 0:
               if i > 0:
                    update_command = update_command + ',Gender = "%s"'
               else:
                    update_command = update_command + 'Gender = "%s"'
               update_command = update_command%(gender)
               i += 1
               
          if len(contact) != 0:
               if i > 0:
                    update_command = update_command + ',Contact = "%s"'
               else:
                    update_command = update_command + 'Contact = "%s"'
               update_command = update_command%(contact)
               i += 1
               
          if len(destination) != 0:
               if i > 0:
                    update_command = update_command + ',Destination = "%s"'
               else:
                    update_command = update_command + 'Destination = "%s"'
               update_command = update_command%(destination)
               i += 1
          update_command = update_command + ' where Ticket_ID = "%s"'%(TicketID)
          
          cursor.execute(update_command)
          DB.commit()
          messagebox.showinfo("Notification","Data Updated!")
          reset()
     
def output_frame(data):
     #========Creating Frame for treeview=========#
     frame=Frame(window,bg='ghost white',relief=RIDGE,borderwidth=5)
     frame.place(x=360,y=150,width=1080,height=600)


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
     tree = ttk.Treeview(frame,columns=('Ticket','Name','Age','Gender','Contact','Destination',
                                        'Date'),yscrollcommand=scroll_y.set)
     
     scroll_y.config(command=tree.yview)
     
     tree.heading("Ticket",text="TicketID")
     tree.heading("Name",text="Name")
     tree.heading("Age",text="Age")
     tree.heading("Gender",text="Gender")
     tree.heading("Contact",text="Contact No.")
     tree.heading("Destination",text="Destination")
     tree.heading("Date",text="Date")

     tree.column('#0', width=0, stretch=NO)
     tree.column('Ticket', width=50, minwidth=50, anchor=CENTER)
     tree.column('Name', width=120,  minwidth=120, anchor=CENTER)
     tree.column('Age', width=50, minwidth=50, anchor=CENTER)
     tree.column('Gender', width=50,  minwidth=50, anchor=CENTER)
     tree.column('Contact', width=100, minwidth=100, anchor=CENTER)
     tree.column('Destination', width=120, minwidth=120, anchor=CENTER)
     tree.column('Date', width=100, minwidth=100,anchor=CENTER)
     
     tree.pack(fill=BOTH,expand=1)

     for row in data:
          date = str(row[6])
          tree.insert('',END,values=[row[0],row[1],row[2],row[3],row[4],row[5],date])
     
def retrive_all():     
     retrive_command = 'select * from record'
     cursor.execute(retrive_command)
     data = cursor.fetchall()
     count = cursor.rowcount
     if count == 0:
          messagebox.showinfo("*Result*","No data found from the table.")
     elif count > 0:
          output_frame(data)     
     reset()

def retrive_data():     
     TicketID = Ticket.get()
     name = Name.get()
     age = Age.get()
     gender = Gender.get()
     contact = Contact.get()
     destination = Destination.get()
     date = Date_r.get()
     if date == 'Enter date like DD/MM/YYYY':
          date = ''
     
     a = check_info(2,TicketID,name,age,gender,contact,destination,date)
     
     retrive_command = "select * from record where "
     i = 0
          
     if a == True:
          interface(2)
     else:
          if len(TicketID) != 3:
               retrive_command = retrive_command + 'Ticket_ID like "%s"'
               retrive_command = retrive_command%(TicketID)
               i = i + 1
          if len(destination) != 0:
               if i > 0:
                    retrive_command = retrive_command + ' and Destination like "%s"' 
               else:
                    retrive_command = retrive_command + 'Destination like "%s"'
               retrive_command = retrive_command%(destination)
               i = i + 1
          if len(age) != 0:
               if i > 0:
                    retrive_command = retrive_command + ' and Age like "%s"'
               else:
                    retrive_command = retrive_command + 'Age like "%s"'
               retrive_command = retrive_command%(age)
               i = i + 1
          if len(gender) != 0:
               if i > 0:
                    retrive_command = retrive_command + ' and Gender like "%s"'
               else:
                    retrive_command = retrive_command + 'Gender like "%s"'
               retrive_command = retrive_command%(gender+'%')
               i = i + 1
          if len(contact) != 0:
               if i > 0:
                    retrive_command = retrive_command + ' and Contact like "%s"'
               else:
                    retrive_command = retrive_command + 'Contact like "%s"'
               retrive_command = retrive_command%(contact)
               i = i + 1
          if len(name) != 0:
               if i > 0:
                    retrive_command = retrive_command + ' and Name like "{}"'
               else:
                    retrive_command = retrive_command + 'Name like "{}"'
               retrive_command = retrive_command.format('%'+name+'%')
               i = i + 1
          if len(date) != 0:
               d = create_date(date)
               if i > 0:
                    retrive_command = retrive_command + ' and Date_=%d'
               else:
                    retrive_command = retrive_command + 'Date_=%d'
               retrive_command = retrive_command%(d)
               i = i + 1
               
          cursor.execute(retrive_command)
          data = cursor.fetchall()
          count = cursor.rowcount
          if count == 0:
               messagebox.showinfo("*Result*","No data found with provided values.")
          elif count > 0:
               output_frame(data)          
          reset()

def insert_data():
     
     date = time.strftime("%Y%m%d")     
     TicketID = checkID()
     name = Name.get()
     age = Age.get()
     gender = Gender.get()
     contact = Contact.get()
     destination = Destination.get()

     a = check_info(1,TicketID,name,age,gender,contact,destination,0)
     if a == True:
          interface(1)
     else:          
          insert_command_1 = "insert into record values('%s','%s','%s','%s','%s','%s','%s')"          
          insert_command_2 = insert_command_1%(TicketID,name,age,gender,contact,destination,date)                 
          cursor.execute(insert_command_2)                 
          DB.commit()

          reset()
          messagebox.showinfo("Notification","  Data Saved!  ")
          interface(1)
     
def delete_interface():
     frame=Frame(window,bg='ghost white',relief=RIDGE,borderwidth=5)
     frame.place(x=360,y=150,width=1080,height=600)
     
     f_l1 = Label(frame,text='DELETE BOX',font=('Cooper Black',30),bg='ghost white')
     f_l1.place(x=355,y=5)
     f_tx = Label(frame,text='Ticket ID  :',font=('Arial Rounded MT Bold',20))
     f_tx.place(x=100,y=200)
     Label(frame,text='Enter Ticket ID of passenger.',font=('Brush Script MT',15),
           bg='ghost white',fg='red').pack(pady=150)
     
     f_tx = Entry(frame,font=('Californian FB',25),fg='blue',textvariable=Ticket,width=30)
     f_tx.place(x=300,y=200)
     
     f_b1 = Button(frame,text='BACK',font=('ROG Fonts',12),fg='red',command=create_frame)
     f_b1.place(x=10,y=10)
     f_b2 = Button(frame,text='DELETE',font=('ROG Fonts',15),fg='red',command=delete_data)
     f_b2.place(x=550,y=300)
     f_b3 = Button(frame,text='RESET',font=('ROG Fonts',15),fg='red',command=reset)
     f_b3.place(x=300,y=300)

def interface(o):
     frame=Frame(window,bg='ghost white',relief=RIDGE,borderwidth=5)
     frame.place(x=360,y=150,width=1080,height=600)
     
     if o == 1:
          
          f_l1 = Label(frame,text='INSERT BOX',font=('Cooper Black',30),bg='ghost white')
          f_l1.place(x=475,y=5)
          
          ticket = checkID()
          
          f_tx = Label(frame,text='Ticket ID  : '+ticket,font=('Arial Rounded MT Bold',20))
          f_tx.place(x=100,y=80)
          
          f_b2 = Button(frame,text='SAVE',font=('ROG Fonts',15),fg='red',command=insert_data)
          f_b2.place(x=550,y=440)
          
          Label(frame,text="*Enter Passenger's data.*",
                font=('Brush Script MT',15),bg='ghost white',fg='red').pack(pady=120)
          
     elif o == 2 or o == 3:
          if o == 2:               
               f_l1 = Label(frame,text='RETRIVE BOX',font=('Cooper Black',30),
                            bg='ghost white')
               f_l1.place(x=355,y=5)
               f_tx = Label(frame,text='Ticket ID  :',font=('Arial Rounded MT Bold',20),
                            bg='ghost white')
               f_tx.place(x=100,y=100)
               f_l7 = Label(frame,text='Date    :',font=('Arial Rounded MT Bold',20),
                            bg='ghost white')
               f_l7.place(x=100,y=400)
               Label(frame,text='Retrive data by',font=('Forte',12),
                     bg='ghost white',fg='red').place(x=50,y=80)
               
               f_e7 = Entry(frame,font=('Californian FB',20),fg='blue',
                            textvariable=Date_r,width=30)
               f_e7.bind("<Button>",empty)
               f_e7.place(x=300,y=400)
               
               f_b2 = Button(frame,text='RETRIVE',font=('ROG Fonts',15),
                             fg='red',command=retrive_data)
               f_b2.place(x=550,y=440)
               f_b3 = Button(frame,text='RETRIVE\n\nALL\n\nDATA',font=('ROG Fonts',15),
                             fg='red',
                             command=retrive_all)
               f_b3.place(x=750,y=170)
               
               i=131
               Label(frame,text='----OR----',font=('Arial',10),bg='ghost white').place(x=115,y=i)
               for thing in range(5):
                    i += 51
                    Label(frame,text='----OR----',font=('Arial',10),bg='ghost white').place(x=115,y=i)
          if o == 3:
               f_l1 = Label(frame,text='UPDATE BOX',font=('Cooper Black',30),bg='ghost white')
               f_l1.place(x=355,y=5)
               f_tx = Label(frame,text='*  '+'Ticket ID  :',font=('Arial Rounded MT Bold',20),
                            bg='ghost white')
               f_tx.place(x=75,y=100)
               Label(frame,text="' * ' indicates that, that field must be filled.",
                     font=('Brush Script MT',15),bg='ghost white',fg='red').place(x=400,y=50)
               
               f_b2 = Button(frame,text='UPDATE',font=('ROG Fonts',15),fg='red',command=update_data)
               f_b2.place(x=550,y=440)
               
               i=182
               Label(frame,text='----OR----',font=('Arial',10),bg='ghost white').place(x=115,y=i)
               for thing in range(3):
                    i += 50
                    Label(frame,text='----OR----',font=('Arial',10),bg='ghost white').place(x=115,y=i)

                         
     
          f_tx = Entry(frame,font=('Californian FB',20),fg='blue',textvariable=Ticket,width=30)
          f_tx.place(x=300,y=100)          

     #Creating common Labels,Enteries and Buttons in Frame     
     #Frame Label     
     f_l2 = Label(frame,text='Name       :',font=('Arial Rounded MT Bold',20),bg='ghost white')
     f_l3 = Label(frame,text='Age        :',font=('Arial Rounded MT Bold',20),bg='ghost white')
     f_l4 = Label(frame,text='Gender     :',font=('Arial Rounded MT Bold',20),bg='ghost white')
     f_l5 = Label(frame,text='Contact    :',font=('Arial Rounded MT Bold',20),bg='ghost white')
     f_l6 = Label(frame,text='Destination:',font=('Arial Rounded MT Bold',20),bg='ghost white')
     f_l2.place(x=100,y=150)
     f_l3.place(x=100,y=200)
     f_l4.place(x=100,y=250)
     f_l5.place(x=100,y=300)
     f_l6.place(x=100,y=350)

     #Frame Entry
     f_e1 = Entry(frame,font=('Californian FB',20),fg='blue',textvariable=Name,width=30)
     f_e2 = Entry(frame,font=('Californian FB',20),fg='blue',textvariable=Age,width=30)
     f_e3 = Entry(frame,font=('Californian FB',20),fg='blue',textvariable=Gender,width=30)
     f_e4 = Entry(frame,font=('Californian FB',20),fg='blue',textvariable=Contact,width=30)
     f_e5 = Entry(frame,font=('Californian FB',20),fg='blue',textvariable=Destination,width=30)
     f_e1.place(x=300,y=150)
     f_e2.place(x=300,y=200)
     f_e3.place(x=300,y=250)
     f_e4.place(x=300,y=300)
     f_e5.place(x=300,y=350)

     #Frame Button
     f_b1 = Button(frame,text='BACK',font=('ROG Fonts',12),fg='red',command=create_frame)
     f_b1.place(x=10,y=10)     
     f_b3 = Button(frame,text='RESET',font=('ROG Fonts',15),fg='red',command=reset)
     f_b3.place(x=300,y=440)


#Creating Labels and Button for main window

l1 = Label(window,text='Passenger List Management',font=("Copperplate Gothic Bold",40),
           bg='#BDB76B')
l1.pack()
b1 = Button(window,text='INSERT ',font=('ROG Fonts',18),width=9,command=lambda:interface(1))
b2 = Button(window,text='RETRIVE',font=('ROG Fonts',18),width=9,command=lambda:interface(2))
b3 = Button(window,text='UPDATE ',font=('ROG Fonts',18),width=9,command=lambda:interface(3))
b4 = Button(window,text='DELETE ',font=('ROG Fonts',18),width=9,command=delete_interface)
b5 = Button(window,text='EXIT   ',font=('ROG Fonts',18),width=9,command=exit)
b1.place(x=50,y=150)
b2.place(x=50,y=250)
b3.place(x=50,y=350)
b4.place(x=50,y=450)
b5.place(x=50,y=550)

create_frame()
