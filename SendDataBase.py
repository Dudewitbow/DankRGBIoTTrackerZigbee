from digi.xbee.devices import XBeeDevice
import requests
import json

PORT = "COM8"
BAUD_RATE = 9600
REMOTE_NODE_ID = "REMOTE"

def getLocation():
   url = 'http://freegeoip.net/json'
   result = requests.get(url)
   jsonResult = json.loads(result.text)
   latitude = jsonResult['latitude']
   longitude = jsonResult['longitude']
   return(latitude, longitude)

def main():
   device = XBeeDevice(PORT, BAUD_RATE)
   try:
       device.open()
       xbee_network = device.get_network()
       remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
       if remote_device is None:
           print("Could not find the remote device")
           exit(1)
       latitude, longitude = getLocation()
       data = "Latitude: " + str(latitude) + " Longitude: " + str(longitude)
       #modify this
       print("Sending data to %s >> %s..." % (remote_device.get_64bit_addr(), data))

       device.send_data(remote_device, data)

   finally:
       if device is not None and device.is_open():
           device.close()


if __name__ == '__main__':
   main()


