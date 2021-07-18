import RPi.GPIO as GPIO
import board
button_a_pin = 12
button_b_pin = 6
button_c_pin = 5

def buttonPressed(channel):
        if channel==12:
            print("button A")
        elif channel==6:
            print("button B")
        elif channel==5:
            print("button C")

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(button_a_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(button_b_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(button_c_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(button_a_pin,GPIO.RISING, callback=buttonPressed)
    GPIO.add_event_detect(button_b_pin,GPIO.RISING, callback=buttonPressed)
    GPIO.add_event_detect(button_c_pin,GPIO.RISING, callback=buttonPressed)