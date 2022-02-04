import cgi
from html.parser import HTMLParser
import csv
import xml.etree.cElementTree as ET
import json
import email
import binascii
import numpy as np 
import yara


# Main imports
import os, sys, types, hashlib, urllib, time, struct, datetime
import gzip, re, tempfile
from optparse import OptionParser
import core.engine
import utils.const

VERSION = '0.01'
RELEASE_DATE = 'Feb 03 2022'


if (os.name == 'nt'):
    import ctypes.wintypes
    from ctypes import windll, cdll, Structure, c_short, c_ushort, byref

    print(windll.kernel32)
    print(cdll.msvcrt) 
    SHORT = c_short 
    WORD = c_ushort 