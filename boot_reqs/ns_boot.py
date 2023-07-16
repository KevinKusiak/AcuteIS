FOREGROUND_BLACK = 0x0000
FOREGROUND_BLUE = 0x0001
FOREGROUND_GREEN = 0x0002
FOREGROUND_CYAN = 0x0003
FOREGROUND_RED = 0x0004
FOREGROUND_MAGENTA = 0x0005
FOREGROUND_YELLOW = 0x0006
FOREGROUND_GREY = 0x0007
FOREGROUND_INTENSITY = 0x0008  # intense fg color

from ctypes import *
SHORT = c_short 
WORD = c_ushort

class coordSys(Structure):
    _fields_ = [
            ("X", SHORT),
            ("Y", WORD)]

class smallRect(Structure):
    _fields_ = [
            ("Left", SHORT),
            ("Right", SHORT),
            ("Top", SHORT),
            ("Bottom", SHORT)]

class consoleScreenBuffer(Structure):
    _fields_ = [
            ("dwSize", coordSys),
            ("dwCursorPosition", coordSys),
            ("wAttributes", WORD),
            ("srWindow", smallRect),
            ("dwMaximumWindowSize", coordSys)]

def initialize_nt():
    print("got to the init")
 devices   csbi = consoleScreenBuffer() 
