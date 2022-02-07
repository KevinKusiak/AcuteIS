from main_init import *

noColor = False

if (os.name == 'nt'):
    import ctypes.wintypes
    from ctypes import windll, cdll, Structure, c_short, c_ushort, byref

    # print(windll.kernel32)
    # print(cdll.msvcrt) 
    SHORT = c_short 
    WORD = c_ushort 

    FOREGROUND_BLACK = 0x0000
    FOREGROUND_BLUE = 0x0001
    FOREGROUND_GREEN = 0x0002
    FOREGROUND_CYAN = 0x0003
    FOREGROUND_RED = 0x0004
    FOREGROUND_MAGENTA = 0x0005
    FOREGROUND_YELLOW = 0x0006
    FOREGROUND_GREY = 0x0007
    FOREGROUND_INTENSITY = 0x0008  # foreground color is intensified.

    class Coord(Structure):
      _fields_ = [
        ("X", SHORT),
        ("Y", SHORT)]


    class SmallRect(Structure):
        _fields_ = [
            ("Left", SHORT),
            ("Top", SHORT),
            ("Right", SHORT),
            ("Bottom", SHORT)]


    class ConsoleScreenBufferInfo(Structure):
        _fields_ = [
            ("dwSize", Coord),
            ("dwCursorPosition", Coord),
            ("wAttributes", WORD),
            ("srWindow", SmallRect),
            ("dwMaximumWindowSize", Coord)]

    stdoutHandle = windll.kernel32.GetStdHandle(-11)
    SetConsoleTextAttribute = windll.kernel32.SetConsoleTextAttribute
    GetConsoleScreenBufferInfo = windll.kernel32.GetConsoleScreenBufferInfo

    def getFeatures():
        iat = ConsoleScreenBufferInfo()
        GetConsoleScreenBufferInfo(stdoutHandle, byref(iat))
        return iat.wAttributes

    def setFeatures(color):
        SetConsoleTextAttribute(stdoutHandle, color)

    def toprint(msg, color):
        try:
            if not noColor:
                defaultColor = getFeatures()
                default = defaultColor & 0x00F0

                setFeatures(color | default)
                sys.stdout.write(msg)
                setFeatures(defaultColor)
            else:
                sys.stdout.write(msg)
                sys.stdout.flush()
        except IOError:
            pass

def logo():
    logo = '''AcuAngle Security Anti-Virus (for %s) Ver %s (%s)
Copyright (C) 2022-%s Kevin Wesley Kusiak. All rights reserved.
'''

    sout = logo % (sys.platform.upper(), VERSION, BUILD_DATE, RELEASE_DATE)
    toprint(sout, FOREGROUND_GREEN)

def options():
    options = '''Options:
    AIS 0.01 
    Usage: ais [Scan Type(s)] [Options] {target specification}
    '''