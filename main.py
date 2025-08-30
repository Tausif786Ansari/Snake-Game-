from tkinter import *
from tkinter import font
import random
import os
# Constants
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPACE_SIZE = 30
BODY_PARTS = 2
SNAKE_COLOR = "#F80404"
FOOD_COLOR = "#F8F8F8"
BACKGROUND_COLOR = "#000000"

# Speed (mutable so it can be changed later)
speed = 150

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        # Start in the center
        start_x = GAME_WIDTH // 2
        start_y = GAME_HEIGHT // 2

        for i in range(self.body_size):
            x = start_x
            y = start_y - i * SPACE_SIZE
            self.coordinates.append((x, y))

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                                             fill=SNAKE_COLOR, tags="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = (x, y)
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                           fill=FOOD_COLOR, outline='red', tags='food')

def FetchScore(score):
    try:
        with open('HighScore.txt','r') as f:
            high=f.read()
            high=int(high) if high else 0
    except FileNotFoundError:
        high=0
    if high<score:
        with open('HighScore.txt','w') as f:
            f.write(str(score))
    else:
        return high

def next_turn(snake, food):
    global speed, direction, score,high_score

    x, y = snake.coordinates[0]

    # Move head
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # Wrap around
    x %= GAME_WIDTH
    y %= GAME_HEIGHT

    new_head = (x, y)

    # Check self-collision
    if new_head in snake.coordinates:
        canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2,text="GAME OVER", font=("Arial", 40), fill="red")
        if high_score<score:
            FetchScore(score)
        return

    # Move snake
    snake.coordinates.insert(0, new_head)
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    #Eatting Food
    fx, fy = food.coordinates
    if abs(x - fx) < SPACE_SIZE and abs(y - fy) < SPACE_SIZE:
        score += 1
        label.config(text=f"Score: {score}")
        canvas.delete("food")
        food = Food()
        if speed >= 70:
            speed -= 1
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        snake.squares.pop()
    
    root.after(speed, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

# Initialize Window
root = Tk()
root.title("Snake Game")
root.resizable(False, False)

# Font
try:
    custom_font = font.Font(family="Digital-7", size=20)
except:
    custom_font = font.Font(family="Arial", size=20)

# Score and Direction
score = 0
high_score=FetchScore(score)
direction = "down"

# Score Label
score_frame = Frame(root)
score_frame.pack(fill='x', padx=10, pady=20)

label = Label(score_frame, text=f"Score: {score}", font=custom_font, fg="#012921", anchor='w')
label.pack(side='left')

label1 = Label(score_frame, text=f"High Score: {high_score}", font=custom_font, fg="#012921", anchor='e')
label1.pack(side='right',padx=10)

# Canvas
canvas = Canvas(root, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Center Window
root.update()
root_width = root.winfo_width()
root_height = root.winfo_height()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width // 2) - (root_width // 2)
y = (screen_height // 2) - (root_height // 2)
root.geometry(f"{root_width}x{root_height}+{x}+{y-40}")

# Keyboard bindings
root.bind('<Left>', lambda event: change_direction('left'))
root.bind('<Right>', lambda event: change_direction('right'))
root.bind('<Up>', lambda event: change_direction('up'))
root.bind('<Down>', lambda event: change_direction('down'))

# Start Game
snake = Snake()
food = Food()
next_turn(snake, food)

# Run
root.mainloop()
