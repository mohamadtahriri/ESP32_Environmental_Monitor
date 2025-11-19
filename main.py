from machine import Pin, I2C, ADC
from i2c_lcd import I2cLcd
import utime

# --- تنظیمات I2C LCD ---
DEFAULT_I2C_ADDR = 0x27 
I2C_NUM_ROWS = 2 
I2C_NUM_COLS = 16 

# تعریف I2C و مقداردهی اولیه LCD (پین‌های 21 و 22)
i2c = I2C(1, scl=Pin(22), sda=Pin(21), freq=400000)
devices = i2c.scan()
lcd_addr = devices[0] if devices else DEFAULT_I2C_ADDR
lcd = I2cLcd(i2c, lcd_addr, I2C_NUM_ROWS, I2C_NUM_COLS)

# --- تنظیمات HC-SR04 ---
trigger = Pin(18, Pin.OUT)
echo = Pin(19, Pin.IN, Pin.PULL_DOWN)

# --- تنظیمات LM35DZ ---
temp_sensor = ADC(Pin(34)) # اتصال به GPIO 34 (ADC)
temp_sensor.width(ADC.WIDTH_12BIT)
temp_sensor.atten(ADC.ATTN_11DB)

# --- توابع HC-SR04 ---
def pulse_in(pin, value, timeout_us=50000):
    """تابع سفارشی اندازه‌گیری مدت زمان پالس"""
    start_time = utime.ticks_us()
    while pin.value() != value:
        if utime.ticks_us() - start_time > timeout_us: return 0
    start_time = utime.ticks_us()
    while pin.value() == value:
        if utime.ticks_us() - start_time > timeout_us: return 0
    return utime.ticks_diff(utime.ticks_us(), start_time)

def measure_distance():
    trigger.value(0); utime.sleep_us(2)
    trigger.value(1); utime.sleep_us(10)
    trigger.value(0)
    duration = pulse_in(echo, 1)
    if duration == 0: return -1
    distance_cm = (duration * 0.0343) / 2
    if distance_cm > 400 or distance_cm < 2: return -2
    return distance_cm

# --- تابع LM35DZ ---
def measure_temperature():
    raw_reading = temp_sensor.read()
    voltage = (raw_reading / 4095) * 3.3
    temperature = voltage / 0.01
    return temperature

# --- حلقه اصلی برنامه ---
lcd.clear()
lcd.putstr("Final Project Ready")
utime.sleep(2)

while True:
    temp = measure_temperature()
    dist = measure_distance()
    
    # نمایش بر روی LCD
    lcd.move_to(0, 0)
    temp_str = "Temp: {:.1f} C".format(temp)
    lcd.putstr(temp_str + " " * (16 - len(temp_str)))

    lcd.move_to(0, 1)
    if dist < 0:
        dist_str = "Dist: Out of Range"
    else:
        dist_str = "Dist: {:.2f} cm".format(dist)
        
    lcd.putstr(dist_str + " " * (16 - len(dist_str)))
    utime.sleep_ms(750)