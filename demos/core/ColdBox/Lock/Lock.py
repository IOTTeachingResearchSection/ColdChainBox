import time
import RPi.GPIO as gpio

class Lock:
    def __init__(self) -> None:
        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)
        gpio.setup(14,gpio.OUT)
        gpio.output(14,gpio.LOW)

    def open(sign:bool):
        if sign:
            gpio.output(14,gpio.HIGH)
            time.sleep(0.1)
            gpio.output(14,gpio.LOW)

# if __name__  == '__main__':
#     lock = Lock()
#     lock.open()