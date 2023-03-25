import RPi.GPIO as GPIO
import time

class ServoMotor:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50) # 50 Hz PWM frequency
        self.pwm.start(0)
    
    def set_angle(self, angle):
        duty_cycle = angle / 18.0 + 2.5 # calculate duty cycle from angle
        self.pwm.ChangeDutyCycle(duty_cycle)
    
    def set_position(self, position):
        duty_cycle = position / 100.0 * 10.0 + 2.5 # calculate duty cycle from position
        self.pwm.ChangeDutyCycle(duty_cycle)
    
    def set_speed(self, speed):
        self.pwm.ChangeFrequency(speed) # change PWM frequency to adjust speed
    
    def set_limits(self, min_angle, max_angle):
        self.min_angle = min_angle
        self.max_angle = max_angle
    
    def set_range(self, min_position, max_position):
        self.min_position = min_position
        self.max_position = max_position
    
    def set_relative_angle(self, angle):
        current_duty_cycle = self.pwm.get_duty_cycle()
        current_angle = (current_duty_cycle - 2.5) * 18.0
        new_angle = current_angle + angle
        if new_angle < self.min_angle:
            new_angle = self.min_angle
        elif new_angle > self.max_angle:
            new_angle = self.max_angle
        self.set_angle(new_angle)
    
    def set_relative_position(self, position):
        current_duty_cycle = self.pwm.get_duty_cycle()
        current_position = (current_duty_cycle - 2.5) / 10.0 * 100.0
        new_position = current_position + position
        if new_position < self.min_position:
            new_position = self.min_position
        elif new_position > self.max_position:
            new_position = self.max_position
        self.set_position(new_position)
    
    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()