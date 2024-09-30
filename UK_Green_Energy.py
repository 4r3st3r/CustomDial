from time import sleep
import network
import urequests
from machine import Pin, PWM, ADC

led = Pin('LED', Pin.OUT)

ssid = 'XXXXX'
password = 'XXXXXXX'

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Setup servo
servoPin = PWM(Pin(15))
servoPin.freq(50)

# Setup temperature
sensor_temp = ADC(4)
conversion_factor = 3.3 / 65535


def servo(degrees):
    """
    Function to move a servo to a specified angle between 0->180 degrees
    :param degrees: the angle for the servo to move to
    :return: Bool
    """
    # limit degrees to between 0 and 180
    if degrees > 180: degrees = 180
    if degrees < 0: degrees = 0

    # set max and min duty
    maxDuty = 8080
    minDuty = 2201

    # new duty is between min and max duty in proportion to its value
    newDuty = minDuty + (maxDuty - minDuty) * (degrees / 180)

    # servo PWM value is set
    servoPin.duty_u16(int(newDuty))
    return True


def convertToDegrees(x, minDeg, maxDeg):
    """
    Convert the input (whatever unit it may be) to an angle
    :param x: the input
    :param minDeg: the lowest value the input could be
    :param maxDeg: the highest value the input could be
    :return:
    """
    percentage = x / (maxDeg - minDeg)
    deg = (1 - percentage) * 180  # reversed because the servo is mounted so that 0 is on the right
    return deg


led.on()

# start up sequence
for d in range(180, 0, -1):
    servo(d)
    sleep(0.01)
for d in range(0, 180, 1):
    servo(d)
    sleep(0.01)

led.off()
sleep(0.1)

while True:
    led.on()

    json = urequests.get('https://api.carbonintensity.org.uk/generation').json()
    mix = json['data']['generationmix']

    greenFuels = ['solar', 'nuclear', 'wind', 'hydro']
    totalGreen = 0

    for item in mix:
        if item['fuel'] in greenFuels:
            totalGreen += item['perc']

    c = convertToDegrees(totalGreen, 0, 110)
    servo(c)

    led.off()
    sleep(300)
