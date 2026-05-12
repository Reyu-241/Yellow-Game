from sense_emu import SenseHat
from time import sleep
import random

#sensehat object
hat = SenseHat()

new_head = (0)
insert = (0, new_head)
hat.clear()

G =(0,255,0)
R =(255,0,0)
O =(0,0,0)

snake = [(4,4)]

direction = "RIGHT"

food = (random.randint(0,7), random.randint(0,7))

speed =0.3

while True:
    #---- JOYSTICK INPUTS -----
    for event in hat.stick.get_events():
        if event.action == "pressed":
            if event.direction == "up" and direction != "DOWN":
                direction= "UP"
            elif event.direction == "down" and direction !="UP":
                direction= "DOWN"
            elif event.direction == "left" and direction !="RIGHT":
                direction= "LEFT"
            elif event.direction == "right" and direction != "LEFT":
                direction= "RIGHT"

    #---- MOVE SNAKE -----
    head_x= snake[0][0]
    head_y= snake[0][1]
    new_head = snake[0]


    #wall collision
    if x <0 or x >7 or y <0 or y >7:
        break
    #snake collision
    if new_head in snake[:-1]:
        break
    #add new head
    snake.insert(0, new_head)
    #----- FOOD CHECK ------
    if new_head == food:
        #create  new food pos
        while food in snake:
            food = (random.randint(0,7), random.randint(0,7))
    else:
        snake.pop()
    #---- Screen -----
    hat.clear()

    #draw snake
    for segment in snake:
        hat.set_pixel(segment[0],segment[1], G)

    #draw food
    hat.set_pixel(food[0], food[1], R)

sleep(0.5)
#------ GAME OVER ----
hat.show_message("Game Over!")
hat.clear