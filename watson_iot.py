import wiotp.sdk.application
import json

options = wiotp.sdk.application.parseConfigFile("app.yaml")
client = wiotp.sdk.application.ApplicationClient(options)

countBarometer = 0
countIRtemperature = 0
countAccelerometer = 0
enoughData = False

def myEventCallback(event):
    str = "%s event '%s' received from device [%s]: %s"
    print(str % (event.format, event.eventId, event.device, json.dumps(event.data)))
    # {"d": {"deviceuid": "B0:B4:48:BE:49:84", "devicename": "esit_device_01", "barometer": [32.14, 1006.71]}}
    # {"d": {"deviceuid": "B0:B4:48:BE:49:84", "devicename": "esit_device_01", "lightmeter": 90.24}}
    # {"d": {"deviceuid": "B0:B4:48:BE:49:84", "devicename": "esit_device_01", "IRtemperature": [31.34375, 23.6875]}}
    # {"d": {"deviceuid": "B0:B4:48:BE:49:84", "devicename": "esit_device_01", "accelerometer": [0.012207, 0.120361, 0.995605]}}
    # {"d": {"deviceuid": "B0:B4:48:BE:49:84", "devicename": "esit_device_01", "humidity": [0.012207, 0.120361]}}
    data = event.data['d']
    


client.connect()
client.deviceEventCallback = myEventCallback


while not enoughData:
    client.subscribeToDeviceEvents()
