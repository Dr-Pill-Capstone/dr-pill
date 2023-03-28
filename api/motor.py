import RPi.GPIO as GPIO

class ServoMotor:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 25) # 50 Hz PWM frequency
        self.pwm.start(0)
    
    def set_angle(self, angle):
        duty_cycle = angle / 18 + 2 # calculate duty cycle from angle
        self.pwm.ChangeDutyCycle(duty_cycle)
    
    def set_position(self, position):
        duty_cycle = position / 100.0 * 10.0 + 2.5 # calculate duty cycle from position
        self.pwm.ChangeDutyCycle(duty_cycle)
    
    def set_speed(self, speed):
        self.pwm.ChangeFrequency(speed) # change PWM frequency to adjust speed
    
    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()