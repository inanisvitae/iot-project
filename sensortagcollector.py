#!/usr/bin/python3
from bluepy import sensortag
import time
import signal
import sys
import argparse

addr = 'xx'
dev_name = 'ST-XX'

def interruptHandler(signal, frame):
    sys.exit(0)

def setup(addr):
    st = sensortag.SensorTag(addr)
    st.lightmeter.enable()
    st.IRtemperature.enable()
    st.accelerometer.enable()
    st.barometer.enable()
    st.humidity.enable()
    return st

def readLux(st):
    lux=st.lightmeter.read()
    print('{"deviceuid":"'+addr+'","devicename":"'+dev_name+'","lightmeter":'+'%.2f'%(lux)+'}')

def readIRTemp(st):
    temp=st.IRtemperature.read()
    print('{"deviceuid":"'+addr+'","devicename":"'+dev_name+'","IRtemperature":['+'%f,%f'%(temp[0],temp[1])+']}')

def readAcceleration(st):
    acc=st.accelerometer.read()
    print('{"deviceuid":"'+addr+'","devicename":"'+dev_name+'","accelerometer":['+'%f,%f,%f'%(acc[0],acc[1],acc[2])+']}')

def readBarometer(st):
    press=st.barometer.read()
    print('{"deviceuid":"'+addr+'","devicename":"'+dev_name+'","barometer":['+'%f,%f'%(press[0],press[1])+']}')

def readHumidity(st):
    hum=st.humidity.read()
    print('{"deviceuid":"'+addr+'","devicename":"'+dev_name+'","humidity":['+'%f,%f'%(hum[0],hum[1])+']}')

def main():
    signal.signal(signal.SIGINT, interruptHandler)

    st = setup(addr)
    while True:
            readLux(st)
            time.sleep(2)
            readIRTemp(st)
            time.sleep(2)
            readAcceleration(st)
            time.sleep(2)
            readBarometer(st)
            time.sleep(2)
            readHumidity(st)
            time.sleep(2)

if __name__ == '__main__':
    # specify commandline options       
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--only", action="store_true", help='restrict recognized devices to only those specified with -d')
    parser.add_argument("-d", "--device", nargs='*',help="Give device with uid a friendly name, in format: uid=friendlyname e.g. a0:e6:f8:b6:34:83=SHOULDER")

    args = parser.parse_args()

    if not args.device:
        print("No device UID given.")
        sys.exit(0)

    for dev in args.device:
        (uid,devname) = dev.split("=",2)
        if not uid or not devname:
            print ("could not split device",dev)
            burp
        dev_name = devname
        addr=uid
    try:
        main()
    finally:
        print('Program terminated.')
