from gpiozero import LED, Buzzer
from time import sleep

# LEDs
red = LED(22)
yellow = LED(27)
green = LED(17)

# Buzzer
buzzer = Buzzer(18)

# Put LEDs into list
leds = [red, yellow, green]


# -----------------------------
# CLEAR / RESET
# -----------------------------
def clear_all():
    for led in leds:
        led.off()
    buzzer.off()


# -----------------------------
# LIGHT FUNCTIONS
# -----------------------------
def normal_light():
    """Green light while snake is moving normally"""
    clear_all()
    green.on()


def food_light():
    """Yellow light when snake eats food"""
    clear_all()
    yellow.on()
    sleep(0.3)
    yellow.off()


def game_over():
    """Red light OFF, only buzzer sounds"""
    clear_all()

    for i in range(5):
        buzzer.on()
        sleep(0.2)

        buzzer.off()
        sleep(0.2)


# -----------------------------
# EXAMPLES TO USE IN SNAKE GAME
# -----------------------------

# Snake moving normally
normal_light()

# Snake eats food
food_light()

# Snake dies by wall or itself
game_over()


# -----------------------------
# STOP EVERYTHING WITH CTRL + C
# -----------------------------
try:
    while True:
        normal_light()
        sleep(1)

except KeyboardInterrupt:
    clear_all()
    print("Lights stopped.")