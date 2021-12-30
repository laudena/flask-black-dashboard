echo 'set up your router to point raspberryclock to your RaspberryPi, or change below raspberryclock to your router IP Address'
ssh pi@raspberryclock "bash -s" < ./extract_from_docker.sh

echo 'now copy from pi'
scp pi@raspberryclock:/home/pi/clock_hand.py .
scp pi@raspberryclock:/home/pi/ui-configure.html .
scp pi@raspberryclock:/home/pi/clock_model.py .
scp pi@raspberryclock:/home/pi/I2C_LCD_driver.py
scp pi@raspberryclock:/home/pi/lcd_display.py

