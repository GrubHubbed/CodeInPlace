from tkinter import *
import random
from threading import *
import sys
import os

"""
menu page
colours, different colour themes, different snake shapes
different gamemodes:
1) after eating food creates block at that position
2) different foods - increase speed, increase length, decrease length, decrease speed, extra life, 
3) snake gets faster the more food it eats
4) different size boards




"""


BOARD_WIDTH = 800
BOARD_HEIGHT = 800
CELL_SIZE = 50
SNAKE_SPEED = 50
SNAKE_PARTS = 3
SNAKE_COLOUR = "green"
FOOD_COLOUR = "red"
BACKGROUND_COLOUR = "black"


class Snake:
    
    def __init__(self):
        # self.body_length = SNAKE_PARTS
        self.coordinates = [] #this contains a list of coordinates of each snake part where the 0th index is the head of the snake
        self.squares = [] #this list contains each canvas square representing each snake part

        for i in range(0, SNAKE_PARTS):
            self.coordinates.append([0, 0])
        
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x+CELL_SIZE, y+CELL_SIZE, fill = SNAKE_COLOUR)
            self.squares.append(square)
            


class Food:

    def __init__(self, snake):
        snake_xpositions = [coordinates[0] for coordinates in snake.coordinates]
        snake_ypositions = [coordinates[1] for coordinates in snake.coordinates]
        self.random_x = random.randint(0, int(BOARD_WIDTH/CELL_SIZE)-1) * CELL_SIZE 
        self.random_y = random.randint(0, int(BOARD_HEIGHT/CELL_SIZE)-1) * CELL_SIZE 
        self.coordinates = [self.random_x, self.random_y]
        
        #ensures that the food item does not spawn in a cell occupied by a snakepart by regenerating random x and y coordinates until it is so.
        while self.random_x in snake_xpositions and self.random_y in snake_ypositions:
            self.random_x = random.randint(0, int(BOARD_WIDTH/CELL_SIZE)-1) * CELL_SIZE 
            self.random_y = random.randint(0, int(BOARD_HEIGHT/CELL_SIZE)-1) * CELL_SIZE 
            self.coordinates = [self.random_x, self.random_y]

    #randomly spawns a food item on the board
    def spawn_food(self):
        canvas.create_oval(self.random_x, self.random_y, CELL_SIZE + self.random_x, CELL_SIZE + self.random_y, fill = FOOD_COLOUR, tag = "food")

def gameplay(snake, food):
    x, y = snake.coordinates[0] #coordinates of the head of the snake

    #These conditions determine how the snake will move depending on the value of the current_direction variable. A new value for x or y is set depending.
    if current_direction == "up":
        y -= CELL_SIZE
    elif current_direction == "down":
        y += CELL_SIZE
    elif current_direction == "left":
        x -= CELL_SIZE  
    elif current_direction == "right":
        x += CELL_SIZE

    snake.coordinates.insert(0, (x,y))

    square = canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill = SNAKE_COLOUR)

    snake.squares.insert(0, square)

    #if a food is eaten the last part of the snake is not deleted. Otherwise the last snakepart is deleted given by the [-1] index.
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        score_label.configure(text = f"Score: {score}")
        canvas.delete("food")
        food = Food(snake)
        food.spawn_food()

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    
    #checks if a collision has occurred. if no collision the next turn function is called again to cause the snake to continue moving.
    if check_crash(snake) == True :
        endgame()

    else:
        game_window.after(SNAKE_SPEED, gameplay, snake, food) #the gameplay() function is only called after SNAKE_SPEED seconds such that this controls the speed of the game through how fast it updates

"""This function controls the direction of the snake which is changed depending on the key pressed. Each direction is binded to a keyboard key. 
A direction change of only 90 degrees is allowed so that the snake does not flip into itself, therefor there is the need for the != conditions
direction is the direction that we want to change to when a certain key is pressed. current_direction is the direction the snake is currently moving in"""
def change_direction(direction): 
    global current_direction

    if direction == "left" and current_direction != "right":
        current_direction = direction
    elif direction == "right" and current_direction != "left":
        current_direction = direction
    elif direction == "up" and current_direction != "down":
        current_direction = direction
    elif direction == "down" and current_direction != "up":
        current_direction = direction

"""This function checks if the snake head has collided with the side walls of the board or a part of the snake body itself. It returns True if a collision has occurred"""
def check_crash(snake):
    x, y = snake.coordinates[0]

#if the x coord of the snake head is less than or past the horizontal width of the board, or the y coord of the snake head is beyond the vertical height of the board the function returns True
    if x < 0 or x >= BOARD_WIDTH or y < 0 or y >= BOARD_HEIGHT:
        return True

#This part checks if the head has collided with a body part, by checking if the coordinates of the head is equal to that of any body part by iterating through each part of the list of coordinates after the head(hence [1:])
    for snakepart in snake.coordinates[1:]:
        if x == snakepart[0] and y == snakepart[1]:
            return True

#erases the canvas and prints text when the game is over
def endgame():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/3, text = "You Lost", font = ("Helvetica", 50), fill = "red")
    canvas.create_text(canvas.winfo_width()/2, (canvas.winfo_height()/2) , text = "Exit To Menu : <Esc>", font = ("Helvetica", 25), fill = "red")
    canvas.create_text(canvas.winfo_width()/2, (canvas.winfo_height()/2) + 65, text = "New Game : <Enter>", font = ("Helvetica", 25), fill = "red")

#starts a new game
def restart(event):
    python = sys.executable
    os.execl(python, python, * sys.argv)

def close_game(event):
    game_window.quit()

#returns to the main menu

# class gamescreen:

#     def __init__(self, root):
#         self.root = root
#         self.secondary_window = None
#         self.start_button = Button(master = self.root, text = "Start Game", command = self.start)
#         self.start_button.pack()

#     def start(self):
#         if not self.secondary_window:
#             self.secondary_window = Toplevel()
#             self.root.withdraw()
#         else:
#             self.secondary_window.deiconify()
#             self.root.withdraw()

def homescreen(event):
    global newWindow
    game_window.withdraw()
    HomeWindow = Toplevel()
    HomeWindow.configure(bg = "black")
    HomeWindow.geometry("1000x800")
    title = Label(HomeWindow, text="Welcome to Snake Game", font = ("Helvetica", 50))
    title.grid(row = 0, column = 0, sticky = "we")

    gamemode = Frame(HomeWindow)
    gamemode.grid(row = 1, column = 0)

    choose_mode = Label(gamemode, text = "Select Mode: ", font = ("Helvetica", 30), fill = "red")
    choose_mode.grid(row = 1, column = 0, sticky = "w")

    homebutton = Button(HomeWindow, text="Start", padx=50, pady=50, command=show, fg="red", bg="white")
    homebutton.grid(row = 2, column = 0, sticky = "nsew")

      

def show():
    game_window.update()
    game_window.deiconify()
    newWindow.destroy()


game_window = Tk()
game_window.title("Snake Game")
game_window.resizable(True, True)
game_window.geometry("1000x1000")

game_window.bind("<w>", lambda x: change_direction("up"))
game_window.bind("<a>", lambda x: change_direction("left"))
game_window.bind("<s>", lambda x: change_direction("down"))
game_window.bind("<d>", lambda x: change_direction("right"))
game_window.bind("<Return>", restart)
game_window.bind("<Escape>", close_game)
score = 0
current_direction = "down"

score_label = Label(master = game_window, text = f"Score: {score}", font = ("Helvetica", 50))
score_label.grid(row = 0, column = 0, sticky = "nsew")

canvas = Canvas(game_window, bg = BACKGROUND_COLOUR, height = BOARD_HEIGHT, width = BOARD_WIDTH)
canvas.grid(row = 1, column = 0, sticky = "nsew")

game_window.update()

snake = Snake()
food = Food(snake)
food.spawn_food()
gameplay(snake, food)


game_window.mainloop()

