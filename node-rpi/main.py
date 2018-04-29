import time
import datetime

import threading
import requests

from picamera.array import PiRGBArray
from picamera import PiCamera

import cv2

from .config import *

class ThreadedRequest(threading.Thread):
    def __init__(self, addr, data, endpoint):
        self.req_host = addr[0]
        self.req_port = addr[1]
        self.req_data = data
        self.req_endpoint = endpoint

        super(ThreadedRequest, self).__init__(self)

    def run(self):
        requests.post("http://{h}:{p}{ep}".format(
            h=self.req_host, p=self.req_port, ep=self.req_endpoint),
                      json=self.req_data)

if __name__ == "__main__":
    camera = PiCamera()
    rawCapture = PiRGBArray(camera)

    #camera warmup
    time.sleep(0.1)

    while True:
        camera.capture(rawCapture, format="bgr")
        img = rawCapture.array

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        cars = car_cascade.detectMultiScale(gray, 1.1, 1)

        req = ThreadedRequest(API_CONN, {
            "id": SELF_NODE_ID,
            "density": len(cars) / kMaxCarCapacity
        }, '/lights/data/cam/')

        time.sleep(kRequestLoopDelay)
