import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.OUT)

servo = GPIO.PWM(11, 50)

servo.start(0)
print("Waiting 1 second")
time.sleep(1)

print("Rotating every 12 seconds")
duty = 2
while duty <= 17:
	servo.ChangeDutyCycle(duty)
	time.sleep(1)
	duty += 1

print("Turning back to original position at 0 degrees")
servo.ChangeDutyCycle(2)
time.sleep(1)
servo.ChangeDutyCycle(0)

# Clean up environment

servo.stop()
GPIO.cleanup()
print("Completed test")

