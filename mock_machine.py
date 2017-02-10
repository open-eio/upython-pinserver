DIRECTION_IN = 0
DIRECTION_OUT = 1
 
class Pin(object):
    IN = DIRECTION_IN
    OUT = DIRECTION_OUT
    def __init__(self, i, direction = DIRECTION_OUT):
        self._i = i
        self._direction = direction
        self._value = False
    def __str__(self):
        return str(self._i)
    def value(self, val = None):
        if not val is None:
            self._value = val
        return self._value

if __name__ == "__main__":
    pin = Pin(0)
