import machine
from utime import sleep
import _thread

class Rotary:
    def __init__(self, latch, count, cb = None):
        self.latch = machine.Pin(latch, machine.Pin.IN, machine.Pin.PULL_UP)
        self.count = machine.Pin(count, machine.Pin.IN, machine.Pin.PULL_UP)
        self._counter = 0
        self.value = 0
        self.callback = cb
        _thread.start_new_thread(self.rot_thread, (None,))

    def rot_thread(self, unused):
        while True:
            while (self.latch.value() == 0):
                if (self.count.value() == 1):
                    self._counter += 1
                    while (self.count.value() == 1):
                        pass # wait for it to go low
            if (self._counter):
                self.value = self._counter
                if (self.callback):
                    self.callback(self.value)
                self._counter = 0
            sleep(0.1)
