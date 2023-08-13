import paho.mqtt.client as mqtt
import time
import random
import json


WIDTH, HEIGHT = 128, 160

def generate_line():
    x1, y1 = random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)
    x2, y2 = random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)
    return [[x1, y1], [x2, y2]]


def main():
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)
    while True:
        line = generate_line()
        payload = dict(lines=[line])
        client.publish("draw", json.dumps(payload))
        time.sleep(3)



# main guard
if __name__ == '__main__':
    main()
