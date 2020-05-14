from tkinter import *
from PIL import ImageTk, Image
import minesweeper


minesweeper_size = "medium"
game = minesweeper.MinesweeperGame(minesweeper_size)

block_size = 30

canvas_width = block_size*game.columns
canvas_height = block_size*game.rows + block_size*1.5
game_start_height = block_size*1.5

button_one_down_location = []
button_three_down_location = []

root = Tk()
canvas = Canvas(root, width= canvas_width, height=canvas_height, borderwidth=0)



def drawBoard(canvas):
    game_height = canvas_height - game_start_height
    for i in range(game.rows):
        row_start = game_height/game.rows*i + game_start_height
        row_end = row_start+block_size
        for j in range(game.columns):
            col_start = canvas_width/game.columns * j
            col_end = col_start+block_size

            canvas.create_rectangle(col_start, row_start, col_end, row_end, fill="#bdbdbd", outline="#7b7b7b")

            #left white line
            canvas.create_line(col_start, row_start, col_start, row_end-1, fill="white")
            canvas.create_line(col_start+1, row_start, col_start+1, row_end-2, fill="white")
            canvas.create_line(col_start+2, row_start, col_start+2, row_end-3, fill="white")
            #top white line
            #if i == 0:
            canvas.create_line(col_start, row_start, col_end-1, row_start, fill="white")
            canvas.create_line(col_start, row_start+1, col_end-2, row_start+1, fill="white")
            canvas.create_line(col_start, row_start+2, col_end-3, row_start+2, fill="white")

            #right dark line (not working)
            canvas.create_line(col_end-1, row_start+1, col_end-1, row_end, fill="#7b7b7b")
            canvas.create_line(col_end-2, row_start+2, col_end-2, row_end, fill="#7b7b7b")
            canvas.create_line(col_end-3, row_start+3, col_end-3, row_end, fill="#7b7b7b")

            #bottom dark line
            canvas.create_line(col_start, row_end, col_end, row_end, fill="#7b7b7b")
            canvas.create_line(col_start+1, row_end-1, col_end, row_end-1, fill="#7b7b7b")
            canvas.create_line(col_start+2, row_end-2, col_end, row_end-2, fill="#7b7b7b")

def buttonOneDownOnBoard(event):
    global button_one_down_location
    if event.y > game_start_height:
        if not game.game_is_over:
            drawShockedSmiley()
            row_clicked, column_clicked = getRowAndColumnClicked(event)
            button_one_down_location=[row_clicked, column_clicked]
    else:
        if event.x > canvas_width/2 - block_size/2 and event.y > game_start_height/2-block_size/2 and event.x <= canvas_width/2 + block_size/2 and event.y <= game_start_height/2+block_size/2:
            game.newGame()
            game.printBoard()
            drawBoard(canvas)

def buttonOneUpOnBoard(event):
    global button_one_down_location
    if not game.game_is_over:
        drawStartingSmiley()
        if event.y > game_start_height:
            row_clicked, column_clicked = getRowAndColumnClicked(event)
            if button_one_down_location == [row_clicked, column_clicked]:
                spaces_to_change = game.clickOnLocation([row_clicked, column_clicked])
                if game.game_is_over:
                    drawDeadSmiley()
                updateBoard(spaces_to_change)
        button_one_down_location = []

def buttonThreeDownOnBoard(event):
    global button_three_down_location
    if not game.game_is_over:
        row_clicked, column_clicked = getRowAndColumnClicked(event)
        if event.y > game_start_height:
            result = game.setFlagOnSpace([row_clicked, column_clicked])
            if result == "add":
                drawFlag([row_clicked, column_clicked])
            elif result == "remove":
                removeFlag([row_clicked, column_clicked])
            button_three_down_location=[row_clicked, column_clicked]

def getRowAndColumnClicked(event):
    row_clicked = int((event.y-game_start_height)//block_size)
    column_clicked = event.x//block_size
    return [row_clicked, column_clicked]

def updateBoard(spaces_to_update):
    colorDict = {'1': "#0100fe", '2':"#017f01", '3':"#fe0000", '4':"#010080", '5':'#810102',
                 '6': "#008081", '7':"#000000" , '8': "#808080", "X": "#000000"}
    game_height = canvas_height - game_start_height
    print(spaces_to_update)
    for space in spaces_to_update:
        i = space[0]
        j = space[1]
        row_start = game_height/game.rows*space[0] + game_start_height
        row_end = row_start+block_size
        col_start = canvas_width/game.columns * space[1]
        col_end = col_start+block_size
        if game.gameboard[i][j][-1] == 'r':
            canvas.create_rectangle(col_start, row_start, col_end, row_end, fill="#bdbdbd", outline="#7b7b7b")
            if game.gameboard[i][j][0] == 'X':
                canvas.create_text((col_end+col_start)/2, (row_end+row_start)/2,
                                font=("", int(block_size*.5)), text=game.gameboard[i][j][0], fill=colorDict[game.gameboard[i][j][0]])
            else:
                if game.gameboard[i][j][0] != '.':
                    canvas.create_text((col_end+col_start)/2, (row_end+row_start)/2,
                                    font=("", int(block_size*.5)), text=game.gameboard[i][j][0], fill=colorDict[game.gameboard[i][j][0]])
        if game.gameboard[i][j][-1] == 'g':
            canvas.create_rectangle(col_start, row_start, col_end, row_end, fill="#ff0004", outline="#7b7b7b")
            canvas.create_text((col_end+col_start)/2, (row_end+row_start)/2,
                            font=("", int(block_size*.5)), text=game.gameboard[i][j][0], fill=colorDict[game.gameboard[i][j][0]])




def drawFlag(position):
    game_height = canvas_height - game_start_height
    row_start = game_height/game.rows*position[0] + game_start_height
    row_end = row_start+block_size
    col_start = canvas_width/game.columns * position[1]
    col_end = col_start+block_size
    #base
    canvas.create_line(col_start+block_size*.2, row_end-block_size*.2,
                       col_start+block_size*.8, row_end-block_size*.2)
    canvas.create_line(col_start+block_size*.2, row_end-block_size*.2-1,
                       col_start+block_size*.8, row_end-block_size*.2-1)
    canvas.create_line(col_start+block_size*.2+1, row_end-block_size*.2-2,
                       col_start+block_size*.8-1, row_end-block_size*.2-2)
    #staff
    canvas.create_line(col_start+block_size*.5, row_start+block_size*.2,
                       col_start+block_size*.5, row_start+block_size*.8)
    canvas.create_line(col_start+block_size*.5-1, row_start+block_size*.2+1,
                       col_start+block_size*.5-1, row_start+block_size*.8+1)
    #flag
    canvas.create_polygon([col_start+block_size*.5, row_start+block_size*.2,
                       col_start+block_size*.25, row_start+block_size*.35,
                       col_start+block_size*.5, row_start+block_size*.5,
                       col_start+block_size*.5, row_start+block_size*.2], fill="#ff0004")

def removeFlag(position):
    game_height = canvas_height - game_start_height
    row_start = game_height/game.rows*position[0] + game_start_height
    row_end = row_start+block_size
    col_start = canvas_width/game.columns * position[1]
    col_end = col_start+block_size
    canvas.create_rectangle(col_start+5, row_start+5, col_end-5, row_end-5, fill="#bdbdbd", outline="")

def drawStartingSmiley():
    #head
    canvas.create_oval(canvas_width/2 - block_size/2, game_start_height/2-block_size/2,
                       canvas_width/2 + block_size/2, game_start_height/2+block_size/2,  fill="#ffff00")
    #eyes
    canvas.create_rectangle(canvas_width/2 - block_size/2 + block_size/4, game_start_height/2-block_size/2+block_size/4,
                            canvas_width/2 - block_size/2 + block_size/4 + block_size/8, game_start_height/2-block_size/2+block_size/4+block_size/8,
                             fill="#000000")
    canvas.create_rectangle(canvas_width/2 + block_size/2 - block_size/4,  game_start_height/2-block_size/2+block_size/4,
                            canvas_width/2 + block_size/2 - block_size/4 - block_size/8, game_start_height/2-block_size/2+block_size/4+block_size/8,
                             fill="#000000")
    #mouth
    canvas.create_line(canvas_width/2 - block_size/2 + block_size/4, game_start_height/2+block_size/8,
                           canvas_width/2 - block_size/2 +block_size/4 + block_size/8 , game_start_height/2+block_size/4,
                             fill="#000000")
    canvas.create_line(canvas_width/2 - block_size/2 + block_size/4 + 1, game_start_height/2+block_size/8,
                        canvas_width/2 - block_size/2 +block_size/4 + block_size/8 + 1 , game_start_height/2+block_size/4,
                          fill="#000000")
    canvas.create_line(canvas_width/2 - block_size/2 +block_size/4 + block_size/8 , game_start_height/2+block_size/4,
                        canvas_width/2 + block_size/2 - block_size/4 - block_size/8 , game_start_height/2+block_size/4, fill="#000000")
    canvas.create_line(canvas_width/2 - block_size/2 +block_size/4 + block_size/8 , game_start_height/2+block_size/4+1,
                        canvas_width/2 + block_size/2 - block_size/4 - block_size/8 , game_start_height/2+block_size/4+1, fill="#000000")
    canvas.create_line(canvas_width/2 + block_size/2 - block_size/4 - block_size/8 , game_start_height/2+block_size/4,
                       canvas_width/2 + block_size/2 - block_size/4 ,game_start_height/2+block_size/8, fill="#000000")
    canvas.create_line(canvas_width/2 + block_size/2 - block_size/4 - block_size/8 , game_start_height/2+block_size/4+1,
                       canvas_width/2 + block_size/2 - block_size/4 ,game_start_height/2+block_size/8+1, fill="#000000")

def drawShockedSmiley():
    #head
    canvas.create_oval(canvas_width/2 - block_size/2, game_start_height/2-block_size/2,
                       canvas_width/2 + block_size/2, game_start_height/2+block_size/2,  fill="#ffff00")
    #eyes
    canvas.create_oval(canvas_width/2 - block_size/2 + block_size/4, game_start_height/2-block_size/2+block_size/4,
                            canvas_width/2 - block_size/2 + block_size/4 + block_size/8, game_start_height/2-block_size/2+block_size/4+block_size/8,
                             fill="#000000")
    canvas.create_oval(canvas_width/2 + block_size/2 - block_size/4,  game_start_height/2-block_size/2+block_size/4,
                            canvas_width/2 + block_size/2 - block_size/4 - block_size/8, game_start_height/2-block_size/2+block_size/4+block_size/8,
                             fill="#000000")
    #mouth
    canvas.create_oval(canvas_width/2 - block_size/2 + block_size*.35, game_start_height/2+block_size/16,
                         canvas_width/2 + block_size/2 - block_size*.35,game_start_height/2+block_size/3)
    canvas.create_oval(canvas_width/2 - block_size/2 + block_size*.35 +1, game_start_height/2+block_size/16,
                      canvas_width/2 + block_size/2 - block_size*.35+1,game_start_height/2+block_size/3)
    canvas.create_oval(canvas_width/2 - block_size/2 + block_size*.35 -1, game_start_height/2+block_size/16,
                      canvas_width/2 + block_size/2 - block_size*.35-1,game_start_height/2+block_size/3)

def drawDeadSmiley():
    #head
    canvas.create_oval(canvas_width/2 - block_size/2, game_start_height/2-block_size/2,
                       canvas_width/2 + block_size/2, game_start_height/2+block_size/2,  fill="#ffff00")
    #eyes
    canvas.create_line(canvas_width/2 - block_size/2 + block_size/4, game_start_height/2-block_size/2+block_size/4,
                            canvas_width/2 - block_size/2 + block_size/4 + block_size/8, game_start_height/2-block_size/2+block_size/4+block_size/8,
                             fill="#000000")
    canvas.create_line(canvas_width/2 - block_size/2 + block_size/4+1, game_start_height/2-block_size/2+block_size/4,
                            canvas_width/2 - block_size/2 + block_size/4 + block_size/8+1, game_start_height/2-block_size/2+block_size/4+block_size/8,
                             fill="#000000")
    canvas.create_line(canvas_width/2 - block_size/2 + block_size/4 + block_size/8, game_start_height/2-block_size/2+block_size/4,
                            canvas_width/2 - block_size/2 + block_size/4 , game_start_height/2-block_size/2+block_size/4+block_size/8, fill="#000000")
    canvas.create_line(canvas_width/2 - block_size/2 + block_size/4 + block_size/8+1, game_start_height/2-block_size/2+block_size/4,
                            canvas_width/2 - block_size/2 + block_size/4+1, game_start_height/2-block_size/2+block_size/4+block_size/8, fill="#000000")

    canvas.create_line(canvas_width/2 + block_size/2 - block_size/4,  game_start_height/2-block_size/2+block_size/4,
                            canvas_width/2 + block_size/2 - block_size/4 - block_size/8, game_start_height/2-block_size/2+block_size/4+block_size/8,
                             fill="#000000")
    canvas.create_line(canvas_width/2 + block_size/2 - block_size/4+1,  game_start_height/2-block_size/2+block_size/4,
                            canvas_width/2 + block_size/2 - block_size/4 - block_size/8+1, game_start_height/2-block_size/2+block_size/4+block_size/8,
                             fill="#000000")
    canvas.create_line(canvas_width/2 + block_size/2 - block_size/4 - block_size/8,  game_start_height/2-block_size/2+block_size/4,
                            canvas_width/2 + block_size/2 - block_size/4 , game_start_height/2-block_size/2+block_size/4+block_size/8,
                             fill="#000000")
    canvas.create_line(canvas_width/2 + block_size/2 - block_size/4 - block_size/8+1,  game_start_height/2-block_size/2+block_size/4,
                            canvas_width/2 + block_size/2 - block_size/4+1 , game_start_height/2-block_size/2+block_size/4+block_size/8,
                             fill="#000000")

    #mouth
    canvas.create_line(canvas_width/2 - block_size/2 + block_size/4 + block_size/8 , game_start_height/2+block_size/8,
                           canvas_width/2 - block_size/2 +block_size/4 , game_start_height/2+block_size/4,
                             fill="#000000")
    canvas.create_line(canvas_width/2 - block_size/2 + block_size/4 + block_size/8  + 1, game_start_height/2+block_size/8,
                        canvas_width/2 - block_size/2 +block_size/4 + 1 , game_start_height/2+block_size/4,
                          fill="#000000")

    canvas.create_line(canvas_width/2 - block_size/2 +block_size/4 + block_size/8 , game_start_height/2+block_size/8,
                        canvas_width/2 + block_size/2 - block_size/4 - block_size/8 , game_start_height/2+block_size/8, fill="#000000")
    canvas.create_line(canvas_width/2 - block_size/2 +block_size/4 + block_size/8 +1, game_start_height/2+block_size/8,
                        canvas_width/2 + block_size/2 - block_size/4 - block_size/8 +1, game_start_height/2+block_size/8, fill="#000000")

    canvas.create_line(canvas_width/2 + block_size/2 - block_size/4 , game_start_height/2+block_size/4,
                       canvas_width/2 + block_size/2 - block_size/4 - block_size/8,game_start_height/2+block_size/8, fill="#000000")
    canvas.create_line(canvas_width/2 + block_size/2 - block_size/4, game_start_height/2+block_size/4-1,
                       canvas_width/2 + block_size/2 - block_size/4 - block_size/8,game_start_height/2+block_size/8-1, fill="#000000")




drawStartingSmiley()
canvas.bind("<Button-1>", buttonOneDownOnBoard)
canvas.bind("<ButtonRelease-1>", buttonOneUpOnBoard)
canvas.bind("<Button-3>", buttonThreeDownOnBoard)
canvas.pack()

drawBoard(canvas)


root.mainloop()
