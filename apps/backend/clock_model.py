import logging
import threading
import time
import os

from apps.backend.clock_hand import ClockHand

logger = logging.getLogger(__name__)
# globals
flag_stop_clock = False
flag_seconds_refresh_timeout = 1.0
TIME_ZONE = 'Australia/Victoria'

# static variables
TIMEOUT_FOR_CLOCK_HAND_THREADS_TO_DIE = 3.0  # seconds
seconds_coil_A_1_pin = 4
seconds_coil_A_2_pin = 17
seconds_coil_B_1_pin = 27
seconds_coil_B_2_pin = 22
seconds_steps_per_revolution = 615  # previously 63.68395*8


class ClockModel:
    def __init__(self):
        self.seconds_hand = ClockHand("seconds", 0.5,
                                      seconds_coil_A_1_pin,
                                      seconds_coil_A_2_pin,
                                      seconds_coil_B_1_pin,
                                      seconds_coil_B_2_pin,
                                      seconds_steps_per_revolution)

        self.seconds_thread = threading.Thread(target=self.seconds_hand.clock_handle,
                                               args=(lambda: flag_stop_clock, lambda: flag_seconds_refresh_timeout))

    def start(self):
        set_time_zone(TIME_ZONE)
        wait_for_threads_to_die()
        print('seconds thread starting...')
        self.seconds_thread.start()
        self.seconds_thread.join()
        print('seconds thread joined!')

    def get_clock_hand(self):
        return self.seconds_hand


def set_seconds_timeout(timeout):
    global flag_seconds_refresh_timeout
    flag_seconds_refresh_timeout = float(timeout)


def set_time_zone(time_zone):
    if time_zone:
        global TIME_ZONE
        TIME_ZONE = time_zone
    os.environ['TZ'] = TIME_ZONE


def stop_clock():
    global flag_stop_clock
    flag_stop_clock = True


def set_time(time_str):
    visibleTime = time.strptime(time_str, "%H:%M")
    print("in set_time: ", visibleTime)
    print (clock_model.seconds_hand)
    clock_model.get_clock_hand().set_motor_position(visibleTime.tm_hour, visibleTime.tm_min)
    # //(time_str.hour % 12) * 60.0 + time_str.minute


def reset_time_from_web():
    try:
        import ntplib
        client = ntplib.NTPClient()
        response = client.request('pool.ntp.org')
        os.system('date ' + time.strftime('%m%d%H%M%Y.%S', time.localtime(response.tx_time)))
    except:
        print('Could not sync with time server.')


def start_clock():
    print("hello from start_clock")
    global clock_model
    clock_model = ClockModel()
    clock_model.start()


def wait_for_threads_to_die():
    global flag_stop_clock
    flag_stop_clock = True
    time.sleep(TIMEOUT_FOR_CLOCK_HAND_THREADS_TO_DIE)
    flag_stop_clock = False

def calibrate_handle(steps):
    clock_model.get_clock_hand().calibrate_handle(steps)