#!/usr/bin/env python3
#############################################################################
# Filename    : Motor.py
# Description : Control Motor with L293D
# Author      : www.freenove.com, Emily Bernier et Sophie Bourgault
# modification: 11 mai 2021
########################################################################
import RPi.GPIO as GPIO
import time
import board
import busio
import adafruit_adxl34x
from ADCDevice import *
#from PCF8574 import PCF8574_GPIO
#from Adafruit_LCD1602 import Adafruit_CharLCD
import os
import signal
import json
import sys
import logging
from gpiozero import Device, LED
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
from uuid import uuid1
import requests
# Initialize GPIO

#Global variables
led_right = 26 # GPIO Pin that LED is connected to
led_left = 16
THING_NAME_FILE = 'thing_name.txt'  # The name of our "thing" is persisted into this file
URL = 'https://dweet.io'            # Dweet.io service API
last_car_state= None# Current state of LED ("on", "off", "blinking")
thing_name= None# Thing name (as persisted in THING_NAME_FILE)
ledR = None
ledL = None
CAR_STATES = ['on', 'reverse', 'right', 'left', 'off']

# Initialize Logging
logging.basicConfig(level=logging.WARNING)  # Global logging configuration
logger = logging.getLogger('main')  # Logger for this module
#logger = logging.getLogger(__name__)# (2)
logger.setLevel(logging.INFO) # Debugging for this file.


Device.pin_factory = PiGPIOFactory()

# define the pins connected to L293D pour les moteurs
motoRPin1 = 27 #gpio23
motoRPin2 = 22 #gpio24
enablePin = 17 #gpio25

motoPin3 = 25 #gpio17
motoPin4 = 23 #gpio27
enablePin2 = 24 #gpio22

#les pins pour les deux LEDs
led1 = 26 #gpio26
led2 = 16 #gpio19

#servo
OFFSE_DUTY = 0.5        #define pulse offset of servo
SERVO_MIN_DUTY = 2.5+OFFSE_DUTY     #define pulse duty cycle for minimum angle of servo
SERVO_MAX_DUTY = 12.5+OFFSE_DUTY    #define pulse duty cycle for maximum angle of servo
servoPin = 4

#joystick
Z_Pin = 20

adc = ADCDevice() # Define an ADCDevice class object

#adc = ADCDevice() # Define an ADCDevice class object

#Pins pour le sonar
trigPin = 7
echoPin = 8
MAX_DISTANCE = 220          # define the maximum measuring distance, unit: cm
timeOut = MAX_DISTANCE*60   # calculate timeout according to the maximum measuring distance

def setup():
    """Create and initialise an LED Object"""
    global ledR
    global ledL
    ledR = LED(led_right)
    ledL = LED(led_left)
    ledR.off()
    ledL.off()
    print("leds initalized")
    #global adc
    #if(adc.detectI2C(0x48)): # Detect the pcf8591.
    #    adc = PCF8591()
    #elif(adc.detectI2C(0x4b)): # Detect the ads7830
    #    adc = ADS7830()
    #else:
    #    print("No correct I2C address found, \n"
    #    "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
    #    "Program Exit. \n");
        
    #    exit(-1)

    #GPIO.setup(Z_Pin,GPIO.IN,GPIO.PUD_UP) # set Z_Pin to pull-up mode

    #moteur 1
    global p2
    #GPIO.setmode(GPIO.BOARD)   
    GPIO.setup(motoRPin1,GPIO.OUT)   # set pins to OUTPUT mode
    GPIO.setup(motoRPin2,GPIO.OUT)
    GPIO.setup(enablePin,GPIO.OUT)
    
    #LEDs
    GPIO.setup(led1, GPIO.OUT) # set the ledPin to OUTPUT mode
    GPIO.output(led1, GPIO.LOW) # make ledPin output LOW level
    GPIO.setup(led2, GPIO.OUT) # set the ledPin to OUTPUT mode
    GPIO.output(led2, GPIO.LOW) # make ledPin output LOW level
        
    p2 = GPIO.PWM(enablePin,1000) # creat PWM and set Frequence to 1KHz
    p2.start(0)
    
    GPIO.setup(Z_Pin,GPIO.IN,GPIO.PUD_UP)   # set Z_Pin to pull-up mode
    
    #moteur 2
    global p3 
    GPIO.setup(motoPin3,GPIO.OUT)   # set pins to OUTPUT mode
    GPIO.setup(motoPin4,GPIO.OUT)
    GPIO.setup(enablePin2,GPIO.OUT)
        
    p3 = GPIO.PWM(enablePin2,1000) # creat PWM and set Frequence to 1KHz
    p3.start(0)
    
    #sonar
    GPIO.setup(trigPin, GPIO.OUT)   # set trigPin to OUTPUT mode
    GPIO.setup(echoPin, GPIO.IN)    # set echoPin to INPUT mode
    
    #servo moteur
    global p
    GPIO.setmode(GPIO.BCM)         # use PHYSICAL GPIO Numbering
    GPIO.setup(servoPin, GPIO.OUT)   # Set servoPin to OUTPUT mode
    GPIO.output(servoPin, GPIO.LOW)  # Make servoPin output LOW level

    p = GPIO.PWM(servoPin, 50)     # set Frequece to 50Hz
    p.start(0)                     # Set initial Duty Cycle to 0
    
def resolve_thing_name(thing_file):
    """Get existing, or create a new thing name"""
    if os.path.exists(thing_file):                                                 # (3)
        with open(thing_file, 'r') as file_handle:
            name = file_handle.read()
            logger.info('Thing name ' + name + ' loaded from ' + thing_file)
            return name.strip()
    else:
        name = str(uuid1())[:8]  # UUID object to string.                          # (4)
        logger.info('Created new thing name ' + name)

        with open(thing_file, 'w') as f:                                           # (5)
            f.write(name)

    return name

def get_latest_dweet():
    """Get the last dweet made by our thing."""
    resource = URL + '/get/latest/dweet/for/' + thing_name                         # (6)
    logger.debug('Getting last dweet from url %s', resource)

    r = requests.get(resource)                                                     # (7)

    if r.status_code == 200:                                                       # (8)
        dweet = r.json() # return a Python dict.
        logger.debug('Last dweet for thing was %s', dweet)

        dweet_content = None

        if dweet['this'] == 'succeeded':                                           # (9)
            # We're just interested in the dweet content property.
            dweet_content = dweet['with'][0]['content']                            # (10)
            print(dweet_content)
            return dweet_content

    else:
        logger.error('Getting last dweet failed with http status %s', r.status_code)
        return {}
    
def stream_dweets_forever():
    """Listen for streaming for dweets"""
    URL = 'https://dweet.io'
    resource = URL + '/listen/for/dweets/from/' + thing_name
    logger.info('Streaming dweets from url %s', resource)

    session = requests.Session()
    request = requests.Request("GET", resource).prepare()

    while True: # while True to reconnect on any disconnections.
        try:
            response = session.send(request, stream=True, timeout=1000)

            for line in response.iter_content(chunk_size=None):
                if line:
                    try:
                        json_str = line.splitlines()[1]
                        json_str = json_str.decode('utf-8')
                        dweet = json.loads(eval(json_str)) # json_str is a string in a string.
                        logger.debug('Received a streamed dweet %s', dweet)

                        dweet_content = dweet['content']
                        process_dweet(dweet_content)
                    except Exception as e:
                        logger.error(e, exc_info=True)
                        logger.error('Failed to process and parse dweet json string %s', json_str)

        except requests.exceptions.RequestException as e:
            #Lost connection. The While loop will reconnect.
            #logger.error(e, exc_info=True)
            pass

        except Exception as e:
            logger.error(e, exc_info=True)
            
#iterateur pour acceleration (x1 et x2)
def getAcceleration(i): #calcul acceleration avec 
    i2c = busio.I2C(board.SCL, board.SDA)
    accelerometer = adafruit_adxl34x.ADXL345(i2c)
    
    string = str(accelerometer.acceleration)[1:-1]
    x = string.split(", ")[0]
    listeAccel = [0, 0]
    #i = 0 #iterateur pour acceleration (x1 et x2)
    string = str(accelerometer.acceleration)[1:-1]
    x = string.split(", ")[0]
    if (i % 2 == 0):
        listeAccel[0] = float(x)
        listeAccel[1] = float(x)
    else:
        listeAccel[1] = float(x)
    print(listeAccel)
    acceleration = listeAccel[1] - listeAccel[0]
    print(acceleration)
    
    #print(accelerometer.acceleration)
    time.sleep(1)
    #print(acceleration)
    return acceleration

def pulseIn(pin,level,timeOut): # obtain pulse time of a pin under timeOut
    t0 = time.time()
    while(GPIO.input(pin) != level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    t0 = time.time()
    while(GPIO.input(pin) == level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    pulseTime = (time.time() - t0)*1000000
    return pulseTime

def getSonar():     # get the measurement results of ultrasonic module,with unit: cm
    GPIO.output(trigPin,GPIO.HIGH)      # make trigPin output 10us HIGH level 
    time.sleep(0.00001)     # 10us
    GPIO.output(trigPin,GPIO.LOW) # make trigPin output LOW level 
    pingTime = pulseIn(echoPin,GPIO.HIGH,timeOut)   # read plus time of echoPin
    distance = pingTime * 340.0 / 2.0 / 10000.0     # calculate distance with sound speed 340m/s 
    return distance

# motor function: determine the direction and speed of the motor according to the input ADC value input
def motor(start):
    
    if (start > 0):  # make motor turn forward
        GPIO.output(motoRPin1,GPIO.HIGH)  # motoRPin1 output HIHG level
        GPIO.output(motoRPin2,GPIO.LOW)   # motoRPin2 output LOW level
        GPIO.output(motoPin3,GPIO.LOW)  # motoRPin1 output HIHG level
        GPIO.output(motoPin4,GPIO.HIGH)   # motoRPin2 output LOW level
        #GPIO.output(led1, GPIO.HIGH)
        #GPIO.output(led2, GPIO.HIGH)
        print ('LEDs on + Turn Forward...')
    elif (start < 0): # make motor turn backward
        GPIO.output(motoRPin1,GPIO.LOW)
        GPIO.output(motoRPin2,GPIO.HIGH)
        GPIO.output(motoPin3,GPIO.HIGH)  # motoRPin1 output HIHG level
        GPIO.output(motoPin4,GPIO.LOW)
        print ('Turn Backward...')
    elif (start == 0):
        GPIO.output(motoRPin1,GPIO.LOW)
        GPIO.output(motoRPin2,GPIO.LOW)
        GPIO.output(motoPin3,GPIO.LOW)  # motoRPin1 output HIHG level
        GPIO.output(motoPin4,GPIO.LOW)
        print ('Motor Stop...')
    p2.start(100)
    p3.start(100)
    #print('enablePins on')

def LCD (distance, acceleration):
    distance = str(int(distance))
    acceleration = str(acceleration)
    lcd.message("Raspberry Mobile" + "\n")# display message nom de la voiture
    #setCursor(7, 14)
    lcd.message("Dist:" + distance + "acc: " + acceleration)# display message distance et accélération

def setCursor (x1, x2):
    lcd.setCursor(x1, 0)
    lcd.message( '    ' )
    lcd.setCursor(x2, 0)
    lcd.message( '    ' )
    
def map( value, fromLow, fromHigh, toLow, toHigh):  # map avalue from one range to another range (for servo motor)
    return(toHigh-toLow)*(value-fromLow) / (fromHigh-fromLow) + toLow

def servoWrite(angle): # make the servo rotate to specific angle, 0-180
    if(angle<0):
        angle = 0
    elif(angle > 180):
        angle = 180
    #angle = (angle * 100) /180
    p.ChangeDutyCycle(map(angle,0,180,SERVO_MIN_DUTY,SERVO_MAX_DUTY)) # map the angle to duty
    #p.ChangeDutyCycle(50)

#def loop():
   # while True:
    #    dweet = get_latest_dweet()                                                 # (11)
   #     if dweet is not None:
   #         process_dweet(dweet)
        #val_Y = adc.analogRead(0) # read analog value of axis X and Y
        #val_X = adc.analogRead(1)
        
        #val_X = 0
        
        #mcp.output(3,1) # Allume le backlight du LCD
        #lcd.begin(16,2) # Set le nombre de colonnes et de lignes
        #LCD(distance, acceleration) #Set l'affichage du LCD en temps de vol

        

def process_dweet(dweet):
    i = 0
    while True:                                                # (18)
        
        """Inspect the dweet and set LED state accordingly"""
        global last_car_state

        if not 'state' in dweet:
            return

        car_state = dweet['state']

        #if car_state == last_car_state:                                                # (14)
            #return; # LED is already in requested state.

        if car_state == 'on':
            val_Y = 100# (15)
            ledR.on()
            ledL.on()
            motor(val_Y)
            distance = getSonar() # get distance
            print ("The distance is : %.2f cm"%(distance))
            acceleration = getAcceleration(i)
            i+=1
            time.sleep(1)
            print("Car turned on!")
        #arrêt des moteur si trop près d'un obstacle.
            if (distance < 15):
                val_Y = 0
                print("Arret pour obstacle")
                motor(val_Y)
                time.sleep(1) #attente de quelques seconde après l'arrêt des moteurs
        elif car_state == 'reverse':
            val_Y = -1
            motor(val_Y)
            ledR.blink()
            ledL.blink()
            print("Car reversing!")
        elif car_state == 'right':
            ledL.blink()
            ledR.off()
            time.sleep(3)
            val_X = 255
            X = (val_X * 180)/255
            servoWrite(X) # donne l'angle au servo-moteur
            print("Turning right!")
            time.sleep(2)
        elif car_state == 'left':
            ledR.blink()
            ledL.off()
            val_X = 0
            X = (val_X * 180)/255
            servoWrite(X) # donne l'angle au servo-moteur
            print("Turning left!")
        elif car_state == 'off':
            val_Y = 0
            ledR.off()
            ledL.off()
            motor(val_Y)
            print("Car turned off!")
        else: # Off, including any unhandled state.
            led_state = 'off'
            ledR.off()
            ledL.off()
            print("LED off!")
        if car_state != last_car_state:                                                # (16)
            last_car_state = car_state
            logger.info('Car is ' + car_state)
        dweet = get_latest_dweet()                                            # (11)

def print_instructions():
    """Print instructions to terminal."""
    print("Control URLs - Try them in your web browser:")
    print("  On    : " + URL + "/dweet/for/" + thing_name + "?state=on")
    print("  Reverse   : " + URL + "/dweet/for/" + thing_name + "?state=reverse")
    print("  Right : " + URL + "/dweet/for/" + thing_name + "?state=right\n")
    print("  Left  : " + URL + "/dweet/for/" + thing_name + "?state=left\n")


def signal_handler(sig, frame):
    """Release resources and clean up as needed."""
    print('You pressed Control+C')
    ledR.off()
    ledL.off()
    sys.exit(0)


# Initialise Module
thing_name = resolve_thing_name(THING_NAME_FILE)

def destroy():
    p2.stop()  # stop PWM
    p3.stop()
    #adc.close()
    GPIO.cleanup()
    
PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
# Create PCF8574 GPIO adapter.
#try:
#    mcp = PCF8574_GPIO(PCF8574_address)
#except:
#    try:
#        mcp = PCF8574_GPIO(PCF8574A_address)
#    except:
#        print ('I2C Address Error !')
#        exit(1)
# Create LCD, passing in MCP GPIO adapter.
#lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)
if __name__ == '__main__':  # Program entrance
    print ('Program is starting ... ')
    setup()
    signal.signal(signal.SIGINT, signal_handler)  # Capture CTRL + C
    print_instructions()
    last_dweet = get_latest_dweet()                                                # (18)
    try:
    #    loop()
        if (last_dweet):
            process_dweet(last_dweet)
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        destroy()



