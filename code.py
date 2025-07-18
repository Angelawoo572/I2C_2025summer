# Write your code here :-)
################################################################
# 18-100 F25 Lab07: I2C Lab Starter Code
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

# import adafruit_ds3231

# address constants
TMP_ADDR = 0x48
BTN_ADDR = 0x6f
LCD_ADDR = 0x72
RTC_ADDR = 0x68

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

#               scl0(GP5)      sda0(GP4)      100kHz
i2c = busio.I2C(scl=board.GP5, sda=board.GP4, frequency=100000)
# rtc = adafruit_ds3231.DS3231(i2c)

# @brief scan the I2C line and return a list of all addresses which respond
# @return list of addresses which respond to I2C prompt
def checkDevices():
    while not i2c.try_lock():
        time.sleep(0.1)
    l = i2c.scan()
    i2c.unlock()
    return l

# @brief    Convert BCD (Binary-Coded Decimal) to decimal
# @return   equivalent decimal integer (0–99)
def bcd_to_decimal(bcd):
    return (bcd >> 4) * 10 + (bcd & 0x0F)

def readClock():
    while not i2c.try_lock():
        time.sleep(0.1)
    data = bytearray(7)
    buf = bytearray(1)
    buf[0] = 0x00
    i2c.writeto(RTC_ADDR, buf)
    i2c.readfrom_into(RTC_ADDR, data)
    i2c.unlock()

    second = bcd_to_decimal(data[0])
    minute = bcd_to_decimal(data[1])
    hour   = bcd_to_decimal(data[2] & 0x3F)
    day    = bcd_to_decimal(data[4])
    month  = bcd_to_decimal(data[5] & 0x1F)
    year   = bcd_to_decimal(data[6]) + 2000

    return time.struct_time((year, month, day, hour, minute, second, 0, -1, -1))

def decimal_to_bcd(dec):
    return ((dec // 10) << 4) | (dec % 10)

def setClock(year, month, day, hour, minute, second):
    while not i2c.try_lock():
        time.sleep(0.1)

    # DS3231 从 0x00 开始，依次是 sec, min, hr, weekday, date, month, year
    data = bytearray(8)
    data[0] = 0x00  # 起始寄存器地址
    data[1] = decimal_to_bcd(second)
    data[2] = decimal_to_bcd(minute)
    data[3] = decimal_to_bcd(hour)
    data[4] = 1  # weekday 1=Monday，可随便设
    data[5] = decimal_to_bcd(day)
    data[6] = decimal_to_bcd(month)
    data[7] = decimal_to_bcd(year - 2000)  # 只写后两位

    i2c.writeto(RTC_ADDR, data)
    i2c.unlock()


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
# @param[in] now      time.struct_time returned by readClock()
# @return       whether or not the button has been pressed
def printLCD(pressed, temp,now):
    # TODO: implement printLCD, remove pass if implemented
    while not i2c.try_lock():
        time.sleep(0.1)

    if pressed == True:
        msg1 = f"{now.tm_hour:02}:{now.tm_min:02}:{now.tm_sec:02}"
    else:
        msg1 = f"{now.tm_year}-{now.tm_mon:02}-{now.tm_mday:02}"
    msg2 = f"Temp = {temp:.1f}C"
    full = f"{msg1} {msg2}"

    i2c.writeto(LCD_ADDR, full)

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
# setClock(2025, 7, 7, 19, 07, 0)
while True:
    # uncomment this to check which devices are connected
    # print([hex(i) for i in checkDevices()])
    temp = readTemp()
    pressed = readBtnStatus()
    # now = rtc.datetime
    now = readClock()
    print(f"Current time: {now.tm_hour:02}:{now.tm_min:02}:{now.tm_sec:02}")

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
    printLCD(pressed, temp, now)

# technically we need to release the I2C object but for our purposes we never will
i2c.deinit()
