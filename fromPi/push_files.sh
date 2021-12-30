
echo 'push files to pi'

ssh pi@raspberryclock "bash -s" < ./clear_files.sh

scp clock_hand.py pi@raspberryclock:/home/pi/clock_hand.py
scp ui-configure.html pi@raspberryclock:/home/pi/ui-configure.html
scp clock_model.py pi@raspberryclock:/home/pi/clock_model.py
scp I2C_LCD_driver.py pi@raspberryclock:/home/pi/I2C_LCD_driver.py
scp lcd_display.py pi@raspberryclock:/home/pi/lcd_display.py

ssh pi@raspberryclock "bash -s" < ./push_to_docker.sh

