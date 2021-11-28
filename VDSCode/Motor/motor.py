import RPi.GPIO as GPIO
import time

pwml=18
pwmr=19

mtren=21

GPIO.setmode(GPIO.BCM)

GPIO.setup(mtren,GPIO.OUT)
GPIO.setup(pwml,GPIO.OUT)
GPIO.setup(pwmr,GPIO.OUT)

GPIO.output(mtren,1)

GPIO.output(pwmr,0)
GPIO.output(pwml,0)
time.sleep(1)

GPIO.output(pwmr,1)
GPIO.output(pwml,1)
time.sleep(1)

GPIO.output(pwmr,0)
GPIO.output(pwml,1)
time.sleep(1)

GPIO.output(pwmr,0)
GPIO.output(pwml,1)
time.sleep(1)