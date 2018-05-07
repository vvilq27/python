'''
Created on 7 maj 2018

@author: arkadiusz.zelazowski
'''

import matplotlib.pyplot as plt
import numpy as np
import pyaudio
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import struct
from scipy.fftpack import fft
import sys
import time

class Plot2D(object):
    def __init__(self):
        self.traces = dict()
        self.phase =0
        self.t = np.arange(0, 3.0, 0.01)
        pg.setConfigOptions(antialias = True)
        self.app = QtGui.QApplication(sys.argv)
        self.win = pg.GraphicsWindow(title='test qt')
        self.win.resize(1000, 600)
        self.win.setWindowTitle('pyqtgraph example')
        self.canvas = self.win.addPlot(title="pytelemetry")
        
        self.waveform = self.win.addPlot(title='waveform', row=1, col=1)
        self.spectrum = self.win.addPlot(title='spectrum', row=2, col=1)
        
        self.CHUNK = 1024 * 2
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
#         RATE = 20000
        self.pause = False
        
        self.p = pyaudio.PyAudio()

        self.stream =  self.p.open(
            format =  self.FORMAT,
            channels =  self.CHANNELS,
            rate =  self.RATE,
            input = True,
            output = True,
            frames_per_buffer =  self.CHUNK 
        )
         
    def start(self):
        if(sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()
    
       
    def set_plotdata(self, name, data_x, data_y):
        if name in self.traces:
            self.traces[name].setData(data_x, data_y)
        else:
            if name == 'waveform':
                self.traces[name] = self.waveform.plot(pen='', width=3)
                self.waveform.setYRange(0,255, padding = 0)
                self.waveform.setXRange(0, 2 * self.CHUNK, padding = 0.005)
                
            if name == 'spectrum':
                self.traces[name] = self.sectrum.plot(pen='m', width = 3)
                self.spectrum.setLogMode(x=True, y=True)
                self.spectrum.setYRange(-4, 0, padding = 0)
                self.spectrum.setXRange(
                    np.log10(20), np.log10(self.RATE/2), padding = 0.005)
                
            
    def update(self):
            data = self.stream.read(self.CHUNK)
            data_int = np.array(struct.unpack(str(2* self.CHUNK) +'B', data), dtype='b')[::2] + 128
            self.set_plotdata(name = 'waveform', data_x = self.x, data_y=data_int)
            
            sp_data = fft(np.array(data_int, dtype='int8') - 128)
            sp_data = np.abs(sp_data[0: int(self.CHUNK / 2)]) * 2 / (128 * self.CHUNK)
            self.set_plotdata(name='spectrum', data_x = self.f, data_y=sp_data)
    
    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(20)
        self.start()
        
if __name__ == '__main__':
    p = Plot2D()
    p.animation()