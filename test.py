from gpiozero import LED, Buzzer
from time import sleep

# LEDs
red = LED(22)
yellow = LED(27)
green = LED(17)

# Buzzer
buzzer = Buzzer(26)

# Put LEDs into list
leds = [red, yellow, green]

try:
    while True:

        for led in leds:
            led.on()

            # Turn buzzer on
            buzzer.on()

            sleep(0.2)

            # Turn everything off
            led.off()
            buzzer.off()

            sleep(0.1)

except KeyboardInterrupt:
    # Turn everything off safely
    for led in leds:
        led.off()

    buzzer.off()

    print("System stopped.")