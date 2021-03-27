#!/usr/bin/python3

import argparse
import RPi.GPIO as GPIO
import time

DELAY = 0.2

PIN = 0
NEUTRAL = 1
ON = 2
OFF = 3
SERVO = -1

group_on = [0, 1, 2, 3, 7, 8] # which lights switches are controlled by --on
group_off = [0, 1, 2, 3, 4, 5, 6, 7, 8] # which light switches are controlled by --off
group_test = [0, 1, 2, 3, 4, 5, 6, 7, 8] # which light switches are controlled by --test

# each element in first list is a light switch
# the columns are:
# pin #, neutral position angle, on position angle, off position angle
light_switches = [[ 3, 90, 140, 40],
                  [ 5, 90, 140, 40],
                  [ 7, 90, 140, 40],
                  [11, 90, 140, 40],
                  [29, 90, 140, 40],
                  [31, 90, 140, 40],
                  [33, 90, 140, 40],
                  [35, 90, 140, 40],
                  [37, 90, 140, 40]]

def servo_control(servo, command_angle, neutral_angle):
    servo.ChangeDutyCycle(2+(command_angle/18))
    time.sleep(DELAY)
    servo.ChangeDutyCycle(2+(neutral_angle/18))
    time.sleep(DELAY)
    servo.ChangeDutyCycle(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Raspberry Pi Servo Light Switch Control')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-n','--on',default=False,action='store_true',help='Power on projector.')
    group.add_argument('-f','--off',default=False,action='store_true',help='Power off projector.')
    parser.add_argument('-c','--channel',type=int,help='Individual channel number to control. Must be used in conjuntion with --on or --off')
    parser.add_argument('-t','--test',default=False,action='store_true',help='Run test sequence.')
    args = parser.parse_args()

    if(args.channel != None and (not args.on and not args.off)):
        print("Channel argument must include either the --on or --off argument")
        exit()
    if(args.channel != None):
        if(args.channel < 1 or args.channel > len(light_switches)):
            print("Channel number must be between 1 and " + str(len(light_switches)))
            exit()

    group_initalize = []

    GPIO.setmode(GPIO.BOARD) # sets GPIO number scheme, this is pin number, or ;board numbering'

    for switch in range(0, len(light_switches)):
        group_initalize.append(switch)
        GPIO.setup(light_switches[switch][PIN], GPIO.OUT) # set pin as an output
        light_switches[switch].append(GPIO.PWM(light_switches[switch][PIN], 50)) # append servo to light_switches set as PWM, and pulse 50Hz
        light_switches[switch][SERVO].start(0)

    if(args.test):
        for switch in group_test:
            servo_control(light_switches[switch][SERVO], light_switches[switch][ON], light_switches[switch][NEUTRAL])
        time.sleep(5)
        for switch in group_test:
            servo_control(light_switches[switch][SERVO], light_switches[switch][OFF], light_switches[switch][NEUTRAL])

    if(args.on):
        if(args.channel == None):
            for switch in group_on:
                servo_control(light_switches[switch][SERVO], light_switches[switch][ON], light_switches[switch][NEUTRAL])
        else:
            servo_control(light_switches[args.channel - 1][SERVO], light_switches[args.channel - 1][ON], light_switches[args.channel - 1][NEUTRAL])

    if(args.off):
        if(args.channel == None):
            for switch in group_off:
                servo_control(light_switches[switch][SERVO], light_switches[switch][OFF], light_switches[switch][NEUTRAL])
        else:
            servo_control(light_switches[args.channel - 1][SERVO], light_switches[args.channel - 1][OFF], light_switches[args.channel - 1][NEUTRAL])

    for switch in group_initalize:
        light_switches[switch][SERVO].stop()

    GPIO.cleanup()
    
