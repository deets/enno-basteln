from st7735 import TFT
from machine import SPI,Pin
import time
import math
import json
import time
import ubinascii
import machine
import micropython
import network
import esp
import umqtt.simple2 as mq

esp.osdebug(None)
import gc
gc.collect()

ssid = 'ssid'
password = 'password'
mqtt_server = '192.168.1.109'
#mqtt_server = 'clawstrider.local'
KEEPALIVE = 100 # Must be set, otherwise moquitto won't work!

#EXAMPLE IP ADDRESS
#mqtt_server = '192.168.1.144'
client_id = ubinascii.hexlify(machine.unique_id())
TOPIC_SUB = b'draw'
topic_pub = b'hello'

last_message = 0
message_interval = 5
counter = 0

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())


spi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
tft=TFT(spi,16,17,18)
tft.initr()
tft.rgb(True)


tft.fill(TFT.RED)

def update_display(payload):
    for line in payload.get("lines", []):
        from_, to = line
        tft.line(from_, to, TFT.BLUE)


# Complete project details at https://RandomNerdTutorials.com

def sub_cb(topic, msg, retained, duplicated):
    print(topic, msg)
    if topic == b'draw':
        try:
            payload = json.loads(msg)
        except ValueError:
            print("malformed message:", repr(msg))
        else:
            update_display(payload)


def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = mq.MQTTClient(client_id, mqtt_server, keepalive=KEEPALIVE)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(TOPIC_SUB)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, TOPIC_SUB))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()


try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

while True:
  try:
    client.check_msg()
    if (time.time() - last_message) > message_interval:
      msg = b'Hello #%d' % counter
      client.publish(topic_pub, msg)
      last_message = time.time()
      counter += 1
  except OSError as e:
    restart_and_reconnect()
