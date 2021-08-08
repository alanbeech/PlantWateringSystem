import utime
from machine import I2C
from pico_i2c_lcd import I2cLcd
from machine import ADC

# display stuff
I2C_ADDR = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20
i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# temperature stuff
adc = ADC(machine.Pin(27))
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

while True:

    # read on board temperature sensor
    reading = sensor_temp.read_u16() * conversion_factor

    # adjust it to temperature value
    temperature = 27 - (reading - 0.706) / 0.001721
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("temp: {}".format(temperature))

    # read capacitive moisture sensor value
    mreading = adc.read_u16()
    # output reading
    print(mreading)

    # some better maths will be needed below to trigger based on change boundaries
    if mreading > 30000:
        lcd.move_to(0, 1)
        lcd.putstr("moisture: Dry")
    else:
        lcd.move_to(0, 1)
        lcd.putstr("moisture: Wet")

    # wait 2 seconds and loop again
    utime.sleep(2)



