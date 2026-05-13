from sense_emu import SenseHat
from gpiozero import LED, Buzzer
from time import sleep
import random

# --------------------------------
# SENSE HAT SETUP
# --------------------------------
hat = SenseHat()
hat.clear()

# --------------------------------
# GPIO SETUP
# --------------------------------
# LEDs
red = LED(22)
yellow = LED(27)
green = LED(17)

# Buzzer
buzzer = Buzzer(26)

# Put LEDs into list
leds = [red, yellow, green]

# --------------------------------
# COLOURS
# --------------------------------
G = (0, 255, 0)
R = (255, 0, 0)
B = (0, 0, 0)
W = (255, 255, 255)

# --------------------------------
# SNAKE SETUP
# --------------------------------
snake = [(4, 4)]
direction = (1, 0)

# Fruit
fruit = (random.randint(0, 7), random.randint(0, 7))

game_over_state = False


# --------------------------------
# GPIO FUNCTIONS
# --------------------------------
def clear_all():
    for led in leds:
        led.off()
    buzzer.off()


def normal_light():
    """Green light while snake moves"""
    clear_all()
    green.on()


def food_light():
    """Yellow light when snake eats food"""
    clear_all()

    yellow.on()
    buzzer.on()

    sleep(0.2)

    yellow.off()
    buzzer.off()


def game_over_lights():
    """Red flashing + buzzer"""
    clear_all()

    for i in range(5):
        red.on()
        buzzer.on()

        sleep(0.2)

        red.off()
        buzzer.off()

        sleep(0.2)


# --------------------------------
# DRAW GAME
# --------------------------------
def draw():
    hat.clear()

    # Draw snake
    for part in snake:
        hat.set_pixel(part[0], part[1], G)

    # Draw fruit
    hat.set_pixel(fruit[0], fruit[1], R)


# --------------------------------
# NEW FRUIT
# --------------------------------
def new_fruit():
    while True:
        new_pos = (
            random.randint(0, 7),
            random.randint(0, 7)
        )

        if new_pos not in snake:
            return new_pos


# --------------------------------
# SHOW GAME OVER
# --------------------------------
def show_game_over():
    hat.clear(R)

    game_over_lights()

    hat.show_message(
        "Game Over!",
        text_colour=W,
        back_colour=R,
        scroll_speed=0.05
    )


# --------------------------------
# MAIN GAME LOOP
# --------------------------------
try:

    while not game_over_state:

        normal_light()

        # -------------------------
        # JOYSTICK INPUT
        # -------------------------
        events = hat.stick.get_events()

        for event in events:

            if event.action == "pressed":

                # Prevent reversing
                if event.direction == "up" and direction != (0, 1):
                    direction = (0, -1)

                elif event.direction == "down" and direction != (0, -1):
                    direction = (0, 1)

                elif event.direction == "left" and direction != (1, 0):
                    direction = (-1, 0)

                elif event.direction == "right" and direction != (-1, 0):
                    direction = (1, 0)

        # -------------------------
        # MOVE SNAKE
        # -------------------------
        head_x, head_y = snake[0]

        new_head = (
            head_x + direction[0],
            head_y + direction[1]
        )

        # -------------------------
        # WALL COLLISION
        # -------------------------
        if (
            new_head[0] < 0 or
            new_head[0] > 7 or
            new_head[1] < 0 or
            new_head[1] > 7
        ):
            game_over_state = True
            break

        # -------------------------
        # SELF COLLISION
        # -------------------------
        if new_head in snake:
            game_over_state = True
            break

        # Add new head
        snake.insert(0, new_head)

        # -------------------------
        # EAT FRUIT
        # -------------------------
        if new_head == fruit:

            food_light()

            fruit = new_fruit()

        else:
            snake.pop()

        # Draw screen
        draw()

        sleep(0.5)

    # -------------------------
    # GAME OVER
    # -------------------------
    show_game_over()

except KeyboardInterrupt:
    clear_all()
    hat.clear()
    print("Game stopped.")
