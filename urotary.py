import machine
from utime import sleep
import _thread

class Rotary:
    def __init__(self, latch, count, cb = None):
        self.latch = machine.Pin(latch, machine.Pin.IN, machine.Pin.PULL_UP)
        self.latch.irq(trigger=machine.Pin.IRQ_RISING, handler=self.latch_isr)
        self.count = machine.Pin(count, machine.Pin.IN, machine.Pin.PULL_UP)
        self.count.irq(trigger=machine.Pin.IRQ_RISING, handler=self.count_isr)
        self._counter = 0
        self.value = 0
        self.callback = cb
        self.schedule_cb = False
        self.debouncer = machine.Timer(-1) # use a virtual timer
        _thread.start_new_thread(self.cb_thread, (None,))

    def cb_thread(self, unused):
        while True:
            if (self.schedule_cb and self.callback):
                self.callback(self.value)
                self.schedule_cb = False
            sleep(0.1)

    def debounce_cnt(self, timer):
        state = machine.disable_irq()
        if (self.count.value() == 1):
            self._counter += 1
        machine.enable_irq(state)

    def debounce_latch(self, timer):
        state = machine.disable_irq()
        if (self.latch.value() == 1):
            self.value = self._counter
            self._counter = 0
            self.schedule_cb = True
        machine.enable_irq(state)

    def count_isr(self, pin):
        self.debouncer.init(period=40, mode=machine.Timer.ONE_SHOT, callback=self.debounce_cnt)

    def latch_isr(self, pin):
        self.debouncer.deinit()
        self.debouncer.init(period=10, mode=machine.Timer.ONE_SHOT, callback=self.debounce_latch)


