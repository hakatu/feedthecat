import RPi.GPIO as GPIO
import time

servoPIN = 18  # GPIO pin number
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50)  # GPIO 1 for PWM with 50Hz
p.start(2.5)  # Initialization, duty cycle (2.5 means the servo is at 0 degrees)

try:
    while True:
        # 180 degrees
        p.ChangeDutyCycle(12.5)
        time.sleep(0.5)
        # 0 degrees
        p.ChangeDutyCycle(2.5)
        time.sleep(0.5)
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
