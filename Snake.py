from sense_emu import SenseHat
from time import sleep
import random
 
hat = SenseHat()
hat.clear()
 
# Colours
G = (0, 255, 0)
R = (255, 0, 0)
B = (0, 0, 0)
W = (255, 255, 255)
 
# Snake startup
snake = [(4, 4)]
direction = (1, 0)
 
# Fruit code
fruit = (random.randint(0, 7), random.randint(0, 7))
 
game_over = False
 
# -----------------from sense_emu import SenseHat
from time import sleep
import random
 
hat = SenseHat()
hat.clear()
 
# Colours
G = (0, 255, 0)
R = (255, 0, 0)
B = (0, 0, 0)
W = (255, 255, 255)
 
# Snake startup
snake = [(4, 4)]
direction = (1, 0)
#-------------------
# Drawing section
# ------------------------------------
def draw():
    hat.clear()
 
    # Draw snake
    for part in snake:
        hat.set_pixel(part[0], part[1], G)
 
    # Draw fruit
    hat.set_pixel(fruit[0], fruit[1], R)
 
 
# -------------------------------------
# Fruit randomised
# -------------------------------------
def new_fruit():
    while True:
        new_pos = (random.randint(0, 7), random.randint(0, 7))
 
        if new_pos not in snake:
            return new_pos
 
 
# -------------------------------------
# Game over
# -------------------------------------
def show_game_over():
 
    hat.clear(R)
 
    sleep(1)
 
    hat.show_message(
        "Game Over!",
        text_colour=W,
        back_colour=R,
        scroll_speed=0.05
    )
 
 
# --------------------------------
# Main game loop
# --------------------------------
while not game_over:
 
    # Joystick inputs
    events = hat.stick.get_events()
 
    for event in events:
 
        if event.action == "pressed":
 
            # Prevent reversing into snake
            if event.direction == "up" and direction != (0, 1):
                direction = (0, -1)
 
            elif event.direction == "down" and direction != (0, -1):
                direction = (0, 1)
 
            elif event.direction == "left" and direction != (1, 0):
                direction = (-1, 0)
 
            elif event.direction == "right" and direction != (-1, 0):
                direction = (1, 0)
 
    # --------------------------------
    # Move snake
    # --------------------------------
    head_x, head_y = snake[0]
 
    new_head = (
        head_x + direction[0],
        head_y + direction[1]
    )
 
    # --------------------------------
    # Wall collision
    # --------------------------------
    if (
        new_head[0] < 0 or
        new_head[0] > 7 or
        new_head[1] < 0 or
        new_head[1] > 7
    ):
        game_over = True
        break
 
    # --------------------------------
    # Self collision
    # --------------------------------
    if new_head in snake:
        game_over = True
        break
 
    # Add new head
    snake.insert(0, new_head)
 
    # --------------------------------
    # Eat fruit
    # --------------------------------
    if new_head == fruit:
        fruit = new_fruit()
 
    else:
        snake.pop()
 
    # Draw the screen
    draw()
 
    sleep(0.5)
 
# Game over
show_game_over()