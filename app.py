from sense_emu import SenseHat
from gpiozero import LED, Buzzer
from time import sleep
from flask import Flask, jsonify, render_template
import csv
import random
import threading
import os

# --------------------------------
# FLASK SETUP
# --------------------------------
app = Flask(__name__)

score = 0
game_over_state = False

SCORE_FILE = "scores.csv"

# Ensure file exists
if not os.path.exists('score.csv'):
    with open('score.csv', "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["score"])


@app.route("/")
def dashboard():
    return render_template("snake.html")


@app.route("/api/scores")
def readings():
    score_list = []

    with open('score.csv', 'r') as csvfile:
        score_reader = csv.reader(csvfile)

        for row in score_reader:
            if row and row[0].isdigit():
                score_list.append(int(row[0]))

    return jsonify({
        "score_list": score_list,
        "latest_score": score_list[-1] if score_list else 0,
        "game_over": game_over_state
    })

# --------------------------------
# SENSE HAT SETUP
# --------------------------------
hat = SenseHat()
hat.clear()

# --------------------------------
# GPIO SETUP
# --------------------------------
red = LED(22)
yellow = LED(27)
green = LED(17)
buzzer = Buzzer(26)

leds = [red, yellow, green]

# --------------------------------
# COLOURS
# --------------------------------
G = (0, 255, 0)
R = (255, 0, 0)
W = (255, 255, 255)

# --------------------------------
# SNAKE SETUP
# --------------------------------
snake = [(4, 4)]
direction = (1, 0)

fruit = (random.randint(0, 7), random.randint(0, 7))

# --------------------------------
# GPIO FUNCTIONS
# --------------------------------
def clear_all():
    for led in leds:
        led.off()
    buzzer.off()


def normal_light():
    clear_all()
    green.on()


def food_light():
    clear_all()
    yellow.on()
    buzzer.on()
    sleep(0.2)
    yellow.off()
    buzzer.off()


def game_over_lights():
    clear_all()
    for _ in range(5):
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

    for part in snake:
        hat.set_pixel(part[0], part[1], G)

    hat.set_pixel(fruit[0], fruit[1], R)


# --------------------------------
# NEW FRUIT
# --------------------------------
def new_fruit():
    while True:
        pos = (random.randint(0, 7), random.randint(0, 7))
        if pos not in snake:
            return pos


# --------------------------------
# SAVE SCORE (APPEND, NOT OVERWRITE)
# --------------------------------
def save_score(final_score):
    with open('score.csv', "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([final_score])


# --------------------------------
# GAME OVER
# --------------------------------
def show_game_over():
    global score

    save_score(score)

    hat.clear(R)
    game_over_lights()

    hat.show_message("Game over",text_colour=W,back_colour=R)


# --------------------------------
# MAIN GAME LOOP
# --------------------------------
def game_loop():
    global direction, fruit, game_over_state, score

    try:
        while not game_over_state:

            normal_light()

            events = hat.stick.get_events()

            for event in events:

                if event.action == "pressed":

                    if event.direction == "up" and direction != (0, 1):
                        direction = (0, -1)

                    elif event.direction == "down" and direction != (0, -1):
                        direction = (0, 1)

                    elif event.direction == "left" and direction != (1, 0):
                        direction = (-1, 0)

                    elif event.direction == "right" and direction != (-1, 0):
                        direction = (1, 0)

            head_x, head_y = snake[0]

            new_head = (
                head_x + direction[0],
                head_y + direction[1]
            )

            # Wall collision
            if new_head[0] < 0 or new_head[0] > 7 or new_head[1] < 0 or new_head[1] > 7:
                game_over_state = True
                break

            # Self collision
            if new_head in snake:
                game_over_state = True
                break

            snake.insert(0, new_head)

            # Eat fruit
            if new_head == fruit:
                score += 1
                food_light()
                fruit = new_fruit()
            else:
                snake.pop()

            draw()
            sleep(0.5)

        show_game_over()

    except KeyboardInterrupt:
        clear_all()
        hat.clear()
        print("Game stopped.")


# --------------------------------
# START EVERYTHING
# --------------------------------
if __name__ == "__main__":

    game_thread = threading.Thread(target=game_loop)
    game_thread.start()

    app.run(host="0.0.0.0", port=5000)