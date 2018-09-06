"""
This is my senior project in which I'll be building a mjinlieff game with an AI
 Current flow:
    game->players->board/pieces->rules->check->win
                ↳AI->MCTS->move->wait->check->continue if need

Work this week 8/27/2018 finish basic game.
"""
from socket import *
from tkinter import *
from tkinter import messagebox
HOST = 'localhost'
PORT = 5555
s = socket()

first = True
root = ''
canvas = ''
squares = {}
background = ''
turn = True
last_move = [[0, 0], '']
aiPiece = []

# Creates an instance of the game with their corresponding tags and dropdown menus
def run_game(width=700, height=700):
    global root 
    global canvas
    # init tkinter and a canvas of 700x700
    root = Tk()
    canvas = Canvas(root, width=width, height=height)
    canvas.pack()
    # Create the 3 different menus
    menubar = Menu(root)
    startmenu = Menu(menubar, tearoff=0)
    exitmenu = Menu(menubar, tearoff=0)

    startmenu.add_command(label="Online Reg", command=connect)
    startmenu.add_command(label="AI Reg", command=ai)
    menubar.add_cascade(label="Play", menu=startmenu)

    exitmenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="Exit", menu=exitmenu)
    root.config(menu=menubar)

    board(width, height)  # it breaks if it ain't there

    root.mainloop()
    print("Im done")  # After its done
# Creates the board at the new dimensions
def board(width, height):
    global canvas
    global squares
    global background
    # Create the background at 0,0 and make it grey
    background = canvas.create_rectangle(0, 0, width, height, fill='grey')
    # Label each player
    if first:
        canvas.create_text(350, 30, font="Ariel", text="player1", fill="white")
    else:
        canvas.create_text(350, 30, font="Ariel", text="player2", fill="white")
    width = 60
    height = 60
    squares = {}
    # Displays the board
    for x in range(4, 8):
        for y in range(4, 8):
            x1 = y * width
            y1 = x * height
            x2 = x1 + width
            y2 = y1 + height
            # Creates a grid with the corresponding x and y
            corr = str(x) + " " + str(y)
            # An array of coordinates with their corresponding spaces in the grid
            squares[x, y] = canvas.create_rectangle(x1, y1, x2, y2, fill="white", tag=corr)
# Creates the AI and clicks where the AI decided to do so
def ai():
    global root
    global canvas
    global first
    global turn
    global background
    global aiPiece
    #  ATM don't  know how to pass in images to config canvas so atm its orange need documentation
    canvas.itemconfig(background, fill="orange")
    canvas.bind("<Button-1>", clicked_ai)
# For multiplayer connectivity
def connect():
    global first
    global turn
    # Connect them
    s.connect((HOST, PORT))
    s.settimeout(.25)

    msg = s.recv(1024)
    # Check who's player 1 and then change variables accordingly
    if msg.decode('utf-8') != "Welcome Player 1":
        first = False
        turn = False
    print(msg.decode('utf-8'))
    # Start the game
    play() 
# the play set
def play():
    global root
    global canvas
    global first
    global turn
    global background

    canvas.itemconfig(background, fill="green")
    canvas.bind("Button-1", clicked)

    try:
        data = s.recv(1024)
        corr = data.decode('utf-8')
        print("Received", corr)
        turn = True

        if "lost" in corr:
            received(corr)
            messagebox.showinfo("You lost, sorry buddy")
            canvas.unbind("Button-1")
        else:
            received(corr)
            play()
    except timeout:
        root.after(500, play)
# receiving the play
def received(corr):
    global canvas
    global squares

    square = ''
    corr_split = str.split(corr)
    for x, y in squares:
        tag = str.split(canvas.itemcget(squares[x, y], "fill"))
        if tag[0] == corr_split[0] and tag[1] == corr_split[1]:
            square = squares[x, y]
            break
    if first:
        canvas.itemconfig(square, fill="blue")
    else:
        canvas.itemconfig(square, fill="red") 
# check the click
def clicked(event):
    global canvas
    global first
    global turn

    square = canvas.find_closest(event.x, event.y)
    # Only do something if the square is blank and if its allowed.
    if canvas.itemcget(square, "fill") == "white": 
        # TODO ADD the ALLOWED part also change red/blue to the current piece
        if turn:
            if first:
                canvas.itemconfig(square, fill="red")
            else:
                canvas.itemconfig(square, fill="blue")
            corr = canvas.itemcget(square, "tag")
            print("Sent", corr)

            corr_split = str.split(corr)
            x, y = int(corr_split[0]), int(corr_split[1])

            corr += check_win(x, y)
            s.send(corr.encode('utf-8'))
            if "lost" in corr:
                messagebox.showinfo("You won", "Great job")
                canvas.unbind("<Button-1>")
            turn = False
        else:
            return 0

# TODO check the AI's click, and position
def clicked_ai(event):
    pass
# TODO check if won
def check_win(x, y):
    pass

run_game()
s.close()
