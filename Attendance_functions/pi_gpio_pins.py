from gpiozero import LED
from gpiozero import Buzzer
from time import sleep

led = LED(17)

led.on()
led.off()



buzzer = Buzzer(17)

while True:
    buzzer.on()
    sleep(1)
    buzzer.off()
    break