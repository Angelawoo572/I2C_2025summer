################################################################
# 18-100 F23 Lab07: I2C Lab Starter Code
#
# version log:
# Mar 06, 2022 - initial version - M Nguyen <mnguyen2>
# Mar 25, 2022 - revised style and organization - M Nguyen <mnguyen2> , Tushaar Jain <tushaarj>
# Mar 30, 2023 - updated str.format() to f string - Owen Ball <oball>
# Mon dd, yyyy - student submision - your name <andrewID>
################################################################

################################################################
# CircuitPython module documentation:
# time      https://circuitpython.readthedocs.io/en/latest/shared-bindings/time/index.html
# board     https://circuitpython.readthedocs.io/en/latest/shared-bindings/board/index.html
# busio     https://circuitpython.readthedocs.io/en/latest/shared-bindings/busio/index.html
# digitalio https://circuitpython.readthedocs.io/en/latest/shared-bindings/digitalio/index.html
################################################################

# load standard Python modules
import time

# load the CircuitPython hardware definition module for pin definitions
import board
import busio

# input output packages
import digitalio

# address constants
TMP_ADDR = 0x48
BTN_ADDR = 0x6f
LCD_ADDR = 0x72
RTC_ADDR = 0x68

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

#               scl0(GP5)      sda0(GP4)      100kHz
i2c = busio.I2C(scl=board.GP5, sda=board.GP4, frequency=100000)

# @brief scan the I2C line and return a list of all addresses which respond
# @return list of addresses which respond to I2C prompt
def checkDevices():
    while not i2c.try_lock():
        time.sleep(0.1)
    l = i2c.scan()
    i2c.unlock()
    return l

# @brief    Convert BCD (Binary-Coded Decimal) to decimal (This is a helper function for q3_rtc)
# @return   equivalent decimal integer (0–99)
def bcd_to_decimal(bcd):
    return (bcd >> 4) * 10 + (bcd & 0x0F)

# @brief    read temperature in Celsius as a floating point number
# @return   temperature in Celsius as a floating point number
def readTemp():
    # TODO: implement readTemp
    while not i2c.try_lock():
        time.sleep(0.1)
    # TODO: put your I2C communication here
    i2c.unlock()
    # TODO: write temperature calculation here
    pass

# @brief    read clock as a time.struct_time
# @return   clock information as a time.struct_time
def read_clock():
    while not i2c.try_lock():
        time.sleep(0.1)
    # TODO: Initialize varibales and read from the module
    i2c.unlock()
    # TODO: Write your calculation of time here
    second = 0
    minute = 0
    hour   = 0
    day    = 0
    month  = 0
    year   = 0 # You will need to change these zeros to practical code
    return time.struct_time((year, month, day, hour, minute, second, 0, -1, -1))

# @brief    check if the button has been pressed
# @return   whether or not the button has been pressed
def readBtnStatus():
    # TODO: implement readBtnStatus, remove pass if implemented
    while not i2c.try_lock():
        time.sleep(0.1)
    # TODO: put your I2C communication here
    i2c.unlock()
    pass

# @brief        set the button LED Brightness
# @param[in]    brightness (0-255) desired brightness the button LED
# @param[in]    reg_addr address to write to
def writeBtnLED(brightness, reg_addr):
    # TODO: implement writeBtnLED, remove pass if implemented
    while not i2c.try_lock():
        time.sleep(0.1)
    # TODO: put your I2C communication here
    i2c.unlock()
    pass

# @brief    clear the LCD
def clearLCD():
    # TODO: implement clearLCD, remove pass if implemented
    pass

# @brief        print stuff to the LCD
# @param[in]    pressed - whether the button is pressed or not
# @param[in]    temp - current temperature in Celsius as a floating point number
# @return       whether or not the button has been pressed
def printLCD(pressed, temp):
    # TODO: implement printLCD, remove pass if implemented
    pass

# @brief        clear the LCD
# @param[in]    r (0-255) red color mix
# @param[in]    g (0-255) red color mix
# @param[in]    b (0-255) red color mix
def setBackLight(r, g, b):
    # TODO: BONUS: implement setBackLight remove pass if implemented
    pass

lightCounter = 0
while True:
    # uncomment this to check which devices are connected
    # print([hex(i) for i in checkDevices()])

    # inserts return value of readTemp() into "It's a lovely {} C today!" and prints
    print(f"It's a lovely {readTemp()} C today!")
    led.value = bool(lightCounter % 2)
    lightCounter += 1
    # TODO: you'll want to tune this delay to get more frequent results
    time.sleep(0.5) # loop delay



# technically we need to release the I2C object but for our purposes we never will
i2c.deinit()
