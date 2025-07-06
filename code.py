# Write your code here :-)
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

import adafruit_ds3231

# address constants
TMP_ADDR = 0x48
BTN_ADDR = 0x6f
LCD_ADDR = 0x72

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

#               scl0(GP5)      sda0(GP4)      100kHz
i2c = busio.I2C(scl=board.GP5, sda=board.GP4, frequency=100000)
rtc_i2c = busio.I2C(scl=board.GP3, sda=board.GP2, frequency=100000)
rtc = adafruit_ds3231.DS3231(rtc_i2c)

# @brief scan the I2C line and return a list of all addresses which respond
# @return list of addresses which respond to I2C prompt
def checkDevices():
    while not i2c.try_lock():
        time.sleep(0.1)
    l = i2c.scan()
    i2c.unlock()
    return l

# @brief    read temperature in Celsius as a floating point number
# @return   temperature in Celsius as a floating point number
def readTemp():
    # TODO: implement readTemp
    while not i2c.try_lock():
        time.sleep(0.1)
    # TODO: put your I2C communication here
    data = bytearray(2)
    i2c.readfrom_into(TMP_ADDR,data)
    i2c.unlock()
    # TODO: write temperature calculation here
    data = (data[0] << 4) | (data[1] >> 4)
    return data * 0.0625

# @brief    check if the button has been pressed
# @return   whether or not the button has been pressed
def readBtnStatus():
    # TODO: implement readBtnStatus, remove pass if implemented
    while not i2c.try_lock():
        time.sleep(0.1)
    # TODO: put your I2C communication here
    output = bytearray([0x03])
    input = bytearray(1)
    i2c.writeto(BTN_ADDR,output)
    i2c.readfrom_into(BTN_ADDR,input)
    i2c.unlock()
    return bool(input[0]&0x04)

# @brief        set the button LED Brightness
# @param[in]    brightness (0-255) desired brightness the button LED
# @param[in]    reg_addr address to write to
def writeBtnLED(brightness, reg_addr):
    # TODO: implement writeBtnLED, remove pass if implemented
    while not i2c.try_lock():
        time.sleep(0.1)
    # TODO: put your I2C communication here
    result = bytearray(2)
    result[0] = reg_addr
    result[1] = brightness
    i2c.writeto(BTN_ADDR,result)
    i2c.unlock()

# @brief    clear the LCD
def clearLCD():
    # TODO: implement clearLCD, remove pass if implemented
    while not i2c.try_lock():
        time.sleep(0.1)
    result = bytearray(2)
    result[0] = 0x7C
    result[1] = 0x2D
    i2c.writeto(LCD_ADDR,result)
    i2c.unlock()

# @brief        print stuff to the LCD
# @param[in]    pressed - whether the button is pressed or not
# @param[in]    temp - current temperature in Celsius as a floating point number
# @return       whether or not the button has been pressed
def printLCD(pressed, temp):
    # TODO: implement printLCD, remove pass if implemented
    while not i2c.try_lock():
        time.sleep(0.1)

    now = rtc.datetime
    time_str = f"{now.tm_hour:02}:{now.tm_min:02}:{now.tm_sec:02}"

    if pressed == True:
        msg = f" hello, temp = {temp:.1f}"
    else:
        msg = f"  bye, temp = {temp:.1f}"
    full = f"{time_str}\n{msg}"

    i2c.writeto(LCD_ADDR, full.encode("utf-8"))

    i2c.unlock()
    return pressed


# @brief        clear the LCD
# @param[in]    r (0-255) red color mix
# @param[in]    g (0-255) red color mix
# @param[in]    b (0-255) red color mix
def setBackLight(r, g, b):
    # TODO: BONUS: implement setBackLight remove pass if implemented
    while not i2c.try_lock():
        time.sleep(0.1)
    result = bytearray(5)
    result[0] = 0x7C
    result[1] = 0x2B
    result[2] = r
    result[3] = g
    result[4] = b
    i2c.writeto(LCD_ADDR,result)
    i2c.unlock()


lightCounter = 0
while True:
    # uncomment this to check which devices are connected
    # print([hex(i) for i in checkDevices()])
    now = rtc.datetime
    print(f"Current time: {now.tm_hour:02}:{now.tm_min:02}:{now.tm_sec:02}")

    time.sleep(1)

    # inserts return value of readTemp() into "It's a lovely {} C today!" and prints
    print(f"It's a lovely {readTemp()} C today!")
    led.value = bool(lightCounter % 2)
    lightCounter += 1
    # TODO: you'll want to tune this delay to get more frequent results
    time.sleep(0.5) # loop delay
    if readBtnStatus():
        writeBtnLED(0xFF,0x19)
        setBackLight(200,215,0)
    else:
        writeBtnLED(0x00,0x19)
        setBackLight(0,225,200)

    clearLCD()
    printLCD(readBtnStatus(),readTemp())

# technically we need to release the I2C object but for our purposes we never will
i2c.deinit()
