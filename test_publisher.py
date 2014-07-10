import zmq
import numpy as np
from time import sleep

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")

tvals = np.arange(0,10,0.01)
yvals = np.sin(2*np.pi*tvals) + np.random.normal(scale=0.1, size=len(tvals))*np.cos(40*np.pi*tvals)

for t,y in zip(tvals,yvals):
    socket.send_string("%f %f" % (t,y))
    sleep(0.01)
