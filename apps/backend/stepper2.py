# import RPi.GPIO as GPIO
from gpiozero import OutputDevice
import time
import os
import threading
from datetime import datetime

TIME_ZONE = 'Australia/Victoria'


# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
coil_A_1_pin = 4  #
coil_A_2_pin = 17 #
coil_B_1_pin = 27 #
coil_B_2_pin = 22 #

#steps per revolution
steps_per_revolution =64*8# 63.68395*8

#motor position state
motor_position = 0
#other globals: motor control and calibration
calibration_steps = 0
stop_calibration = False
stop_clock = False

# adjust if different
StepCount = 8
Seq = range(0, StepCount)
Seq[0] = [1,0,0,0]
Seq[1] = [1,1,0,0]
Seq[2] = [0,1,0,0]
Seq[3] = [0,1,1,0]
Seq[4] = [0,0,1,0]
Seq[5] = [0,0,1,1]
Seq[6] = [0,0,0,1]
Seq[7] = [1,0,0,1]

# GPIO.setup(coil_A_1_pin, GPIO.OUT)
# GPIO.setup(coil_A_2_pin, GPIO.OUT)
# GPIO.setup(coil_B_1_pin, GPIO.OUT)
# GPIO.setup(coil_B_2_pin, GPIO.OUT)
self.A_1_pin = OutputDevice(coil_A_1_pin)
self.A_2_pin = OutputDevice(coil_A_1_pin)
self.B_1_pin = OutputDevice(coil_A_1_pin)
self.B_2_pin = OutputDevice(coil_A_1_pin)
#GPIO.output(enable_pin, 1)

def setStep(w1, w2, w3, w4):
    self.A_1_pin.on() if w1 == 1 else self.A_1_pin.off()
    self.A_2_pin.on() if w2 == 1 else self.A_2_pin.off()
    self.B_1_pin.on() if w3 == 1 else self.B_1_pin.off()
    self.B_2_pin.on() if w4 == 1 else self.B_2_pin.off()
#     GPIO.output(coil_A_1_pin, w1)
#     GPIO.output(coil_A_2_pin, w2)
#     GPIO.output(coil_B_1_pin, w3)
#     GPIO.output(coil_B_2_pin, w4)

def forward(delay, steps):
    for i in range(steps):
        for j in range(StepCount):
            setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(delay)
        global motor_position
        motor_position = normalizeSteps(motor_position + 1)

def backwards(delay, steps):
    for i in range(steps):
        for j in reversed(range(StepCount)):
            setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(delay)
        global motor_position
        motor_position = normalizeSteps(motor_position - 1)


def calibrate_handle():
    while 1:
	global stop_calibration
        if stop_calibration:
            break
        delay = 1
        step = 1
        forward(int(delay) / 1000.0, int(step))

def clock_handle():
    global stop_clock
    while 1:
	if stop_clock:
	    break;
	time.sleep(0.1)
	print('sec:' + str(datetime.now().second) + ' current:' + str(motor_position) + ' needs:' + str(int(datetime.now().second / 60.0 * steps_per_revolution)))
	required_motor_position=int( datetime.now().second / 60.0 * steps_per_revolution )
	if (motor_position > normalizeSteps(steps_per_revolution/2.0 + required_motor_position)):
		if required_motor_position > motor_position:
			steps_delta = int( required_motor_position -  motor_position )
			forward(1/1000.0, abs(steps_delta))
	    	elif required_motor_position < motor_position:
			steps_delta = int( steps_per_revolution - motor_position + required_motor_position )
			forward(1/1000.0, abs(steps_delta))

	elif motor_position < normalizeSteps(steps_per_revolution/2.0 + required_motor_position):
		if required_motor_position < motor_position:
			steps_delta = int( motor_position - required_motor_position)
			backwards(1/1000.0, int(steps_delta))
	    	elif required_motor_position > motor_position:
			steps_delta = int( required_motor_position - motor_position )
			forward(1/1000.0, abs(steps_delta))

def normalizeSteps(steps):
    while(steps<0):
	steps = steps+steps_per_revolution
    while(steps>steps_per_revolution):
	steps = steps-steps_per_revolution
    return steps



if __name__ == '__main__':

    os.environ['TZ'] = TIME_ZONE
    time.tzset()

    try:
        import ntplib
        client = ntplib.NTPClient()
        response = client.request('pool.ntp.org')
        os.system('date ' + time.strftime('%m%d%H%M%Y.%S', time.localtime(response.tx_time)))
    except:
        print('Could not sync with time server.')


    print('Time sync completed.')
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    while True:
        print('motor position:' + str(motor_position))
	setStep(0,0,0,0)
	command = raw_input("cmd (f)orward (l)oop (r)otate20times (c)alibrate (s)top Clock, or enter to Start Clock ") 
        #delay = raw_input("Time Delay (ms)?")
        #steps = raw_input("How many steps forward? ")
	if (command == "l" or command == "r"):
		steps = steps_per_revolution
		if (command =="r"):
			steps = steps * 20
		delay = 1
		forward(int(delay) / 1000.0, int(steps))
	if (command == "f"):
		steps = 20
		delay =1
		forward (int(delay) / 1000.0, int(steps))
        if (command == "c"):
		stop_calibration = False
                stop_clock = True
		calibrationThread = threading.Thread(target=calibrate_handle)
                calibrationThread.start()
                input = raw_input()
		global stop_calibration
		stop_calibration = True
		calibrationThread.join()
                print('calibrated from position:' + str(motor_position) +' to 0')
                motor_position = 0
        if (command == ""):
		stop_clock = True
		time.sleep(1.0)
		stop_clock = False
		clockThread = threading.Thread(target=clock_handle)
		clockThread.start()
	if (command == "s"):
		stop_clock = True
		clockThread.join()

        print('motor position:' + str(motor_position))
	#raw_input("hit enter")
        #steps = raw_input("How many steps backwards? ")
        #backwards(int(delay) / 1000.0, int(steps))

