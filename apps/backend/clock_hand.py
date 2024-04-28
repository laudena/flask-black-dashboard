import logging
from datetime import time, datetime
from gpiozero import OutputDevice
import time
import os

POSITION_FILE = "motor-position.txt"
DATETIME_FORMAT_FOR_REPORT = '%H:%M:%S %Z'
logger = logging.getLogger(__name__)

class ClockHand:
    def __init__(self, flask_app, name,
                 _coil_A_1_pin,
                 _coil_A_2_pin,
                 _coil_B_1_pin,
                 _coil_B_2_pin,
                 _steps_per_revolution):
        self.flask_app = flask_app
        self.name = name
        self.refresh_timeout = 0.5

        self.coil_A_1_pin = _coil_A_1_pin
        self.coil_A_2_pin = _coil_A_2_pin
        self.coil_B_1_pin = _coil_B_1_pin
        self.coil_B_2_pin = _coil_B_2_pin

        # steps per revolution
        self.steps_per_revolution = _steps_per_revolution

        # motor position state
        self.motor_position = 4800
        # other globals: motor control and calibration
        self.calibration_steps = 0

        # adjust if different
        self.stepCount = 8
        self.Seq = list(range(0, self.stepCount))
        self.Seq[0] = [1, 0, 0, 0]
        self.Seq[1] = [1, 1, 0, 0]
        self.Seq[2] = [0, 1, 0, 0]
        self.Seq[3] = [0, 1, 1, 0]
        self.Seq[4] = [0, 0, 1, 0]
        self.Seq[5] = [0, 0, 1, 1]
        self.Seq[6] = [0, 0, 0, 1]
        self.Seq[7] = [1, 0, 0, 1]

        self.A_1_pin = OutputDevice(self.coil_A_1_pin)
        self.A_2_pin = OutputDevice(self.coil_A_2_pin)
        self.B_1_pin = OutputDevice(self.coil_B_1_pin)
        self.B_2_pin = OutputDevice(self.coil_B_2_pin)

    def set_step(self, w1, w2, w3, w4):
        self.A_1_pin.on() if w1 == 1 else self.A_1_pin.off()
        self.A_2_pin.on() if w2 == 1 else self.A_2_pin.off()
        self.B_1_pin.on() if w3 == 1 else self.B_1_pin.off()
        self.B_2_pin.on() if w4 == 1 else self.B_2_pin.off()

    def reset_pins(self):
        self.A_1_pin.off()
        self.A_2_pin.off()
        self.B_1_pin.off()
        self.B_2_pin.off()

    def forward(self, delay, steps):
        if steps == 0:
            return
        print("Forward, [", steps, "] from pos [", self.motor_position, "]")
        for i in range(steps):
            for j in range(self.stepCount):
                self.set_step(self.Seq[j][0], self.Seq[j][1], self.Seq[j][2], self.Seq[j][3])
                time.sleep(delay)
            self.motor_position = self.normalize_steps(self.motor_position + 1)
            # print("Forward, [", i, "..", steps, "] to pos [", self.motor_position, "]")
        self.reset_pins()
        self.persist_motor_position()

    def backwards(self, delay, steps):
        if steps == 0:
            return
        print("Backward, [", steps, "] from pos [", self.motor_position, "]")
        for i in range(steps):
            for j in reversed(range(self.stepCount)):
                self.set_step(self.Seq[j][0], self.Seq[j][1], self.Seq[j][2], self.Seq[j][3])
                time.sleep(delay)
            self.motor_position = self.normalize_steps(self.motor_position - 1)
        self.reset_pins()
        self.persist_motor_position()

    def calibrate_handle(self, flag_stop_calibration):
        while 1:
            if flag_stop_calibration:
                break
            delay = 1
            step = 1
            self.forward(int(delay) / 1000.0, int(step))

    def clock_handle(self, flag_stop_clock, flag_refresh_timeout):
        while 1:
            if flag_stop_clock():
                print("Flag STOP raised, in clcok_handle thread")
                break
            time.sleep(flag_refresh_timeout())
            self.read_motor_position()
            current_time = datetime.now().strftime("%H:%M:%S")
            # print("Current Time =", current_time)
            minutes = datetime.now().hour%12 * 60.0 + datetime.now().minute
            # print('timeout:' + str(self.refresh_timeout) + ' mins:' + str(minutes) + ' current:' + str(self.motor_position) + ' needs:' + str(
            #     int(minutes / 60.0 * self.steps_per_revolution)))
            required_motor_position = int(minutes / 60.0 * self.steps_per_revolution)
            self.shortest_path(self.motor_position, required_motor_position, self.steps_per_revolution * 12)


    def normalize_steps(self, steps):
        while steps < 0:
            steps = steps + self.steps_per_revolution * 12.0
        while steps > self.steps_per_revolution * 12.0:
            steps = steps - self.steps_per_revolution * 12.0
        return steps

    def set_motor_position(self, hours, minutes):
        # print("in set_motor_position: ", hours, minutes)
        self.motor_position = int(((hours % 12) + minutes / 60.0) * self.steps_per_revolution)
        self.persist_motor_position()

    def persist_motor_position(self):
        self.write_value_to_file(self.motor_position)

    def read_motor_position(self):
        self.motor_position = self.read_value_from_file()

    def write_value_to_file(self, value):
        with open(POSITION_FILE, 'w') as file:
            file.write(str(value))

    def read_value_from_file(self):
        try:
            with open(POSITION_FILE, 'r') as file:
                value_str = file.read().strip()
            return int(float(value_str))
        except FileNotFoundError:
            print("Error: {POSITION_FILE} not found.")
            return None
        except ValueError:
            print("Error: Data is not a valid integer.", value_str)
            return None

    def set_time_zone(self, time_zone):
        #Australia/Melbourne
        #US/Eastern
        os.environ['TZ'] = time_zone
        time.tzset()

    def shortest_path(self, current_location, required_location, loop_size):
        print('shortest_path:' + str(current_location) +"," + str(required_location)+"," +  str(loop_size))
        # Calculate the forward distance
        if required_location >= current_location:
            forward_distance = required_location - current_location
        else:
            forward_distance = loop_size - current_location + required_location

        # Calculate the backward distance
        backward_distance = loop_size - forward_distance

        # Determine the shorter distance and direction
        if forward_distance <= backward_distance:
            self.forward(1 / 1000.0, forward_distance)
        else:
            self.backwards(1 / 1000.0, backward_distance)





