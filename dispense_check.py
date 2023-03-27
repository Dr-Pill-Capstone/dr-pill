import csv
import time
from datetime import datetime, timedelta

import api.motor as motor

def dispense_pill(pill_qty, pill_name):
    print(f"Dispensing {pill_qty} {pill_name} pill(s)...")

while True:
    schedule = []
    with open('dispensing_s(chedule.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            schedule.append(row)
    
    current_time = time.time()
    
    for row in schedule:
        last_administered_time = datetime.strptime(row[4], "%I:%M %p")
        interval = timedelta(hours=int(row[2]))
        motor = int(row[5])
        
        next_dispense_time = last_administered_time + interval
        
        if current_time >= next_dispense_time:
            if motor == 1:
                left_motor = motor.ServoMotor(11)
                left_motor.set_angle(165)
                time.sleep(1)
                left_motor.set_angle(0)
                time.sleep(1)
                left_motor.cleanup()
            else:
                right_motor = motor.ServoMotor(12) # Confirm pin
                right_motor.set_angle(165)
                time.sleep(1)
                right_motor.set_angle(0)
                time.sleep(1)
                right_motor.cleanup()
        
        # TODO: Correct logic to update pill inventory if one is implemented
        # and update csv with next dispense time
        last_administered_time_str = last_administered_time.strftime("%I:%M %p")
        row[4] = last_administered_time_str
        
    time.sleep(60)
                
            
            
            