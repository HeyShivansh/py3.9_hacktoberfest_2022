from tkinter import *
from tkinter import messagebox
import mysql.connector as ms
import time

#----Connecting to database and creating a database and a table-----
DB = ms.connect(host = "localhost", user = "root", password = "admin")
cursor = DB.cursor()
cursor.execute("create database if not exists ttt")
cursor.execute("use ttt")
table_command = '''
                create table if not exists record(
                Player_Name char(20),
                VS_player char(25),
                Winner char(20),
                Result char(6),
                Score char(10),
                Date_ date)
                '''     
cursor.execute(table_command)

#-----Creating Window-----
window = Tk()
window.title("Tic Tac Toe")
window.geometry("1550x800+0+0")
window.configure(background="crimson")

#----Global Variables-----
round_no = 1
choice = None
player = "X" # --Chosen by the player 
game_is_on = True
winner = None  # --Result of game
list_of_names = []
player_name, vs_player = None, None
date = time.strftime("%Y%m%d")

Name = StringVar()

#------------------------------------------------------< Funs >--------------------------------------------------------

def save_data_inDBMS():

    if (winner == choice):
        print(round_no)
        result = "Win"
        if round_no >= 3:
            score = '+3'
        else:
            score = '+1'
    elif (winner == None and (player=='X' or player=='O')):
        result = "Tie"
        score = "0"
    else:
        result = "Lose"
        score = "0"
        
    
    insert_com = "insert into record values('{}','{}','{}','{}','{}',{})".format(player_name,vs_player,winner,result,score,date)
    cursor.execute(insert_com)
    DB.commit()


def reset():
    global b1,b2,b3,b4,b5,b6,b7,b8,b9,list_of_names,winner,game_is_on,player,round_no
    
    b1['text'],b2['text'],b3['text'],b4['text'],b5['text'],b6['text'],b7['text'],b8['text'],b9['text'] = '','','','','','','','',''   
    player = choice

    if (winner == choice):
        round_no += 1
    else:
        round_no = 1
        
    list_of_names = []
    winner = None
    game_is_on = True    
    
    
def flip_player():

    global player

    if player == "X":
       player = "O"
    elif player == "O":
       player ="X"

def row_win():
    global game_is_on
    
    row_1 = b1["text"] == b2["text"] == b3["text"] !=""
    row_2 = b4["text"] == b5["text"] == b6["text"] !=""
    row_3 = b7["text"] == b8["text"] == b9["text"] !=""

    if row_1 or row_2 or row_3:
        game_is_on = False

    if row_1:
        return b1["text"]
    elif row_2:
        return b4["text"]
    elif row_3:
        return b7["text"]

def column_win():
    global game_is_on
    
    column_1 = b1["text"] == b4["text"] == b7["text"] !=""
    column_2 = b2["text"] == b5["text"] == b8["text"] !=""
    column_3 = b3["text"] == b6["text"] == b9["text"] !=""

    if column_1 or column_2 or column_3:
        game_is_on = False

    if column_1:
        return b1["text"]
    elif column_2:
        return b2["text"]
    elif column_3:
        return b3["text"]

def diagonal_win():
    global game_is_on
    
    digonal_1 = b1["text"] == b5["text"] == b9["text"] !=""
    digonal_2 = b3["text"] == b5["text"] == b7["text"] !=""
    
    if digonal_1 or digonal_2:
        game_is_on = False

    if digonal_1:
        return b1["text"]
    elif digonal_2:
        return b3["text"]
    
def check_win():

    global winner
    
    row_winner = row_win()
    column_winner = column_win()
    diagonal_winner = diagonal_win()

    if row_winner:
        winner = row_winner
    elif column_winner:
        winner = column_winner
    elif diagonal_winner:
        winner = diagonal_winner
    return

def check_tie():

    global winner

    if (b1['text']!="" and b2['text']!="" and b3['text']!="" and b4['text']!="" and b5['text']!="" and b6['text']!="" and b7['text']!="" and b8['text']!="" and b9['text']!=""):
        winner = None
    return


def check_if_game_is_on():
    check_win()
    check_tie()
    return

def display_board():
    window.mainloop()
    

def play_game(button_object, button_name):

    global list_of_names

    if button_name not in list_of_names:
        list_of_names.append(button_name)

        while game_is_on:

            if button_object["text"] == "":

                button_object["text"] = "{}".format(player)     

                flip_player()
                
            check_if_game_is_on()
            
            if winner == "X" or winner == "O":
                
                print("\n-------Player ",winner," won!--------\n")
                messagebox.showinfo("*Result*",'-------Player {} won!--------\n'.format(winner))
                #exit()

    
            elif winner == None and len(list_of_names) == 9:
                messagebox.showinfo("*Result*",'TIE\n')
                print("\n-------Its a Tie.--------\n")
            if not game_is_on:
                    save_data_inDBMS()
            display_board()

        
        

def destroysave(frame_object):
    global player_name
    player_name = Name.get()
    
    #--- Destroying Frame Window
    frame_object.destroy()
    hiding_frame.destroy()


def assign_player(sign, frame_object):
    global player, hiding_frame, vs_player, choice

    if sign == "O":
        player = sign
        choice = sign
        vs_player = 'Player_X'
    elif sign == "X":
        player = sign
        choice = sign
        vs_player = 'Player_O'

    #--- Creating Invisible Frame (not really)
    Frame2 = Frame(frame_object)
    Frame2.place(x=50, y=400, width=876, height=286)

    Name.set("Player_{}".format(sign))

    #-- Label
    ask_text = Label(Frame2, text='Enter Name   : ',font=('Arial Rounded MT Bold',15))
    ask_text.place(x=225, y=110)
    #-- Entry
    ask_entry = Entry(Frame2, textvariable=Name, font=('Californian FB',15))
    ask_entry.place(x=400, y=110)
    #-- Button
    save_but = Button(Frame2, text='Save', font=('Maiandra GD',20), command=lambda:destroysave(frame_object))
    save_but.place(x=350, y=220)
 
    
def choose_player_window():
    Frame1 = Frame(main_frame)
    Frame1.place(x=0, y=0, width=976, height=736)

    frame_heading = Label(Frame1, text="Choose Player 1", font=("Cooper Black",35))
    frame_heading.pack(pady=10)

    frame_button1 = Button(Frame1, text="X", font=("Cooper Black",45),width=10, command=lambda:assign_player("X",Frame1))
    frame_button2 = Button(Frame1, text="O", font=("Cooper Black",45),width=10, command=lambda:assign_player("O",Frame1))
    frame_button1.place(x=30, y=200)
    frame_button2.place(x=530, y=200)

    new_game_button = Button(menu_frame, text='New Game', font=("Maiandra GD",30), command=reset)
    new_game_button.place(x=75, y=100)

#-------------------------------------------------->< __main__ ><---------------------------------------------------------
    
#--- Creating Menu Frame and its buttons 
menu_frame = Frame(window, relief=RIDGE, borderwidth=7, bg="#CE0000")
menu_frame.place(x=25, y=25, width=425, height=750)

menu_label = Label(menu_frame, text='Menu', font=('cooper black',35), bg='#CE0000').pack()

play_game_button = Button(menu_frame, text='Play Game', font=("Maiandra GD",30), command=choose_player_window)
play_game_button.place(x=75, y=100)

exit_button = Button(menu_frame, text='Exit Game',width=10, font=("Maiandra GD",30), command=lambda:window.destroy())
exit_button.place(x=75, y=340)

score_button = Button(menu_frame, text='Scorecard', font=('Maiandra GD',32))
score_button.place(x=75, y=220)


#--- Creating Main Screen Frame
main_frame = Frame(window, relief=RIDGE, borderwidth=7, bg='orange')
main_frame.place(x=465, y=25, width=990, height=750)


#--- Creating Game Frame and its components
game_frame = Frame(main_frame, relief=RIDGE, borderwidth=7, bg='black')
game_frame.place(x=160, y=42, width=668, height=657)

b1 = Button(game_frame, text="", width=8, height=4, font=("Cooper Black", 29), command=lambda:play_game(b1,'b1'))
b2 = Button(game_frame, text="", width=8, height=4, font=("Cooper Black", 29), command=lambda:play_game(b2,'b2'))
b3 = Button(game_frame, text="", width=8, height=4, font=("Cooper Black", 29), command=lambda:play_game(b3,'b3'))
b4 = Button(game_frame, text="", width=8, height=4, font=("Cooper Black", 29), command=lambda:play_game(b4,'b4'))
b5 = Button(game_frame, text="", width=8, height=4, font=("Cooper Black", 29), command=lambda:play_game(b5,'b5'))
b6 = Button(game_frame, text="", width=8, height=4, font=("Cooper Black", 29), command=lambda:play_game(b6,'b6'))
b7 = Button(game_frame, text="", width=8, height=4, font=("Cooper Black", 29), command=lambda:play_game(b7,'b7'))
b8 = Button(game_frame, text="", width=8, height=4, font=("Cooper Black", 29), command=lambda:play_game(b8,'b8'))
b9 = Button(game_frame, text="", width=8, height=4, font=("Cooper Black", 29), command=lambda:play_game(b9,'b9'))

b1.grid(row=0,column=1)
b2.grid(row=0,column=2)
b3.grid(row=0,column=3)
b4.grid(row=1,column=1)
b5.grid(row=1,column=2)
b6.grid(row=1,column=3)
b7.grid(row=2,column=1)
b8.grid(row=2,column=2)
b9.grid(row=2,column=3)

#--- Creating Hiding Frame to hide Game Frame
hiding_frame = Frame(main_frame, bg='crimson')
hiding_frame.place(x=0, y=0, width=976, height=736)

window.mainloop()
