import wiotp.sdk.application
import getopt
import signal
import time
import sys
import json

options = wiotp.sdk.application.parseConfigFile("app.yaml")
client = wiotp.sdk.application.ApplicationClient(options)

collector = {
    'barometer': [],
    'IRtemperature': [],
    'humidity': []
}
countBarometer = 0
countIRtemperature = 0
countAccelerometer = 0
countHumidity = 0
enoughData = False

def interruptHandler(signal, frame):
    client.disconnect()
    sys.exit(0)


def myEventCallback(event):
    global countBarometer
    global countIRtemperature
    global countHumidity
    str = "%s event '%s' received from device [%s]: %s"
    print(str % (event.format, event.eventId, event.device, json.dumps(event.data)))
    # {"d": {"deviceuid": "B0:B4:48:BE:49:84", "devicename": "esit_device_01", "barometer": [32.14, 1006.71]}}
    # {"d": {"deviceuid": "B0:B4:48:BE:49:84", "devicename": "esit_device_01", "lightmeter": 90.24}}
    # {"d": {"deviceuid": "B0:B4:48:BE:49:84", "devicename": "esit_device_01", "IRtemperature": [31.34375, 23.6875]}}
    # {"d": {"deviceuid": "B0:B4:48:BE:49:84", "devicename": "esit_device_01", "accelerometer": [0.012207, 0.120361, 0.995605]}}
    # {"d": {"deviceuid": "B0:B4:48:BE:49:84", "devicename": "esit_device_01", "humidity": [0.012207, 0.120361]}}
    # data: {'deviceuid': 'B0:B4:48:BE:49:84', 'devicename': 'esit_device_01', 'humidity': [31.0495, 56.347656]}
    # {'deviceuid': 'B0:B4:48:BE:49:84', 'devicename': 'esit_device_01', 'lightmeter': 44.86}
    # {'deviceuid': 'B0:B4:48:BE:49:84', 'devicename': 'esit_device_01', 'barometer': [31.77, 1002.5]}
    # {'deviceuid': 'B0:B4:48:BE:49:84', 'devicename': 'esit_device_01', 'accelerometer': [0.006836, 0.018311, -1.023193]}
    #{'deviceuid': 'B0:B4:48:BE:49:84', 'devicename': 'esit_device_01', 'IRtemperature': [31.0625, 23.59375]}
    data = event.data['d']
    print(data)
    print(countBarometer)
    print(countIRtemperature)
    print(countHumidity)
    if 'barometer' in data and countBarometer < 30:
        value = data['barometer'][1]
        collector['barometer'].append(value)
        countBarometer += 1
    if 'IRtemperature' in data and countIRtemperature < 30:
        value = data['IRtemperature'][1] * 9/5 + 32
        collector['IRtemperature'].append(value)
        countIRtemperature += 1
    if 'humidity' in data and countHumidity < 30:
        value = data['humidity'][1]
        collector['humidity'].append(value)
        countHumidity += 1

signal.signal(signal.SIGINT, interruptHandler)
client.connect()
client.deviceEventCallback = myEventCallback
client.subscribeToDeviceEvents()
while min(countBarometer, countIRtemperature, countHumidity) is not 30:
    time.sleep(1)


f = open('barometer_data.txt', 'a')
for i in range(len(collector['barometer'])):
    f.write(str(collector['barometer'][i]) + '\n')
f.close()
f = open('humidity_data.txt', 'a')
for i in range(len(collector['barometer'])):
    f.write(str(collector['humidity'][i]) + '\n')
f.close()
f = open('fahrenheit_data.txt', 'a')
for i in range(len(collector['barometer'])):
    f.write(str(collector['IRtemperature'][i]) + '\n')
f.close()