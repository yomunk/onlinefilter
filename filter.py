import sys
import zmq
import numpy as np
from scipy.signal import iirfilter
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.lines import Line2D

class FilterWindow:
    def __init__(self, ax, b, a):
        self.ax = ax
        self.b = b
        self.a = a

        self.t = []
        self.input = []
        self.output = []

        self.input_buffer=np.zeros(len(a))
        self.output_buffer=np.zeros(len(b))

        self.raw_line = Line2D(self.t, self.input, color='k', alpha=0.5)
        self.filt_line = Line2D(self.t, self.output, color='r', alpha=0.5)

        self.ax.add_line(self.raw_line)
        self.ax.add_line(self.filt_line)

        self.ax.set_ylim(-1,1)
        self.ax.set_xlim(0,10)


    def update(self, data):
        t,y=data
        self.t.append(t)
        self.input.append(y)

        self.input_buffer=np.roll(self.input_buffer, 1)
        self.output_buffer=np.roll(self.output_buffer, 1)

        self.input_buffer[0] = y
        self.output_buffer[0] = np.dot(self.b, self.input_buffer) -\
                np.dot(self.a[1:], self.output_buffer[1:])

        self.output.append(self.output_buffer[0])

        self.raw_line.set_data(self.t, self.input)
        self.filt_line.set_data(self.t, self.output)
        return self.raw_line, self.filt_line,

def zmq_listener():
    context=zmq.Context()
    socket=context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5556")
    socket.setsockopt (zmq.SUBSCRIBE, b"")
    while True:
        string = socket.recv_string()
        t, y = string.split()
        yield t, y


b,a = iirfilter(4, 0.1, btype='lowpass', analog=False, ftype='butter')
fig, ax = plt.subplots()
filtwin = FilterWindow(ax, b, a)

ani = animation.FuncAnimation(fig, filtwin.update, zmq_listener, interval=1,blit=True)

plt.show()




