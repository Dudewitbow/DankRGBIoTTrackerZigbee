#pip3 install phue
from digi.xbee.devices import XBeeDevice
import requests
import json
import re #regex
import time
from phue import Bridge
from math import 

#change port if needed
PORT = devttyUSB2
BAUD_RATE = 9600
b = Bridge('192.168.1.145') #change if needed
red =  {'transitiontime'  1, 'on'  True, 'xy'[0.7006,0.2993]}
green = {'transitiontime'  1, 'on'  True, 'xy'[0.4091, 0.518]}
blue = {'transitiontime'  1, 'on'  True, 'hue'  46920}



# Returns Latitude and Longitude GPS data via IP
def getLocation()
   url = 'httpfreegeoip.netjson'
   result = requests.get(url)
   jsonResult = json.loads(result.text)
   latitude = jsonResult['latitude']
   longitude = jsonResult['longitude']
   return(latitude, longitude)

# Determines Cardinal Direction given Bearing in Degrees
def cardinalDirection(degree)
   if degree  348.75 or degree = 11.25
       return N
   elif degree  11.25 and degree = 33.75
       return NNE
   elif degree  33.75 and degree = 56.25
       return NE
   elif degree  56.25 and degree = 78.75
       return ENE
   elif degree  78.75 and degree = 101.25
       return E
   elif degree  101.25 and degree = 123.75
       return ESE
   elif degree  123.75 and degree = 146.25
       return SSE
   elif degree  146.25 and degree = 191.25
       return S
   elif degree  191.25 and degree = 213.75
       return SSW
   elif degree  213.75 and degree = 236.25
       return SW
   elif degree  236.25 and degree = 258.75
       return WSW
   elif degree  258.75 and degree = 281.25
       return W
   elif degree  281.25 and degree = 303.75
       return WNW
   elif degree  303.75 and degree = 326.25
       return NW
   else
       return NNW

# Calculates Bearing and Distance
def haversine(lat1, lon1, lat2, lon2)
   #convert to radians
   lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
   longi = lon2 - lon1
   lati = lat2 - lat1
   #distance
   inner = sin(lati2)2 + cos(lat1)  cos(lat2)  sin(longi2)2
   outer = 2  asin(sqrt(inner))
   radius = 6371 #6371 radius of earth in kilometers, 3956 for miles
   distance = radius  outer
   #direction
   left = sin(longi)  cos(lat2)
   right = (cos(lat1)  sin(lat2)) - (sin(lat1)  cos(lat2)  cos(longi))
   direction = atan2(left, right)
   direction = degrees(direction)
   direction = (direction + 360) % 360
   card = cardinalDirection(direction)
   print(Distance %.2f KilometersnBearing %.2f� (%s) % (distance, direction, card))

# Main
def main()
   device = XBeeDevice(PORT, BAUD_RATE)
   b.connect()
   b.create_group('RGB', [1,2,3])
   b.set_group(1, green)
   currentTime = time.time()
   targetTime = time.time()

   try
       device.open()
       while(True)
           #light reset
           if targetTime  time.time()
               b.set_group(1, green)
              
           # Receive Data and Parse
           def data_receive_callback(xbee_message)
               address = xbee_message.remote_device.get_64bit_addr()
               message = xbee_message.data.decode()
               print(From %s  %s % (address, message))
               regexQuery = re.compile(r'-d+.d+')
               result = [float(i) for i in regexQuery.findall(message)]
               print (result)
               #lat, lon = getLocation()
               #SJSU Police Department geo location
               lat = 37.3331
               lon = -121.8799
               currentTime = time.time()
               print(Current Time %sn % (currentTime))
               haversine(lat, lon, result[0], result[1])
               b.set_group(1, red)

           device.add_data_received_callback(data_receive_callback)
           #haversine = (lat, lon, result[0], result[1])

           print(Waiting for data...n)
           choice = input(Type x to exit ) # press key to exit
           if choice == 'x'
               break
           if choice == 'h'
               b.set_group(1, blue)
               startTime = time.time()
               targetTime = startTime + 5 #5 second timer


   finally
       if device is not None and device.is_open()
           device.close()


if __name__ == '__main__'
   main()


