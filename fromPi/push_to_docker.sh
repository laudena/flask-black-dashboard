sudo docker cp clock_hand.py AnalogClockStepper_appseed-app_1:/app/backend/clock_hand.py
sudo docker cp clock_model.py AnalogClockStepper_appseed-app_1:/app/backend/clock_model.py
sudo docker cp ui-configure.html AnalogClockStepper_appseed-app_1:/app/home/templates/ui-configure.html
sudo docker cp I2C_LCD_driver.py AnalogClockStepper_appseed-app_1:/app/backend/I2C_LCD_driver.py
sudo docker cp lcd_display.py AnalogClockStepper_appseed-app_1:/app/backend/lcd_display.py
echo "done"

