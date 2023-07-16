#!/usr/bin/env python

import sys, os, cgi, json, email
# import yara IDK why this isn't working rip
from pwn import *
from ns_boot import *
from posix_boot import *
context(arch='x86_64', os='linux')

import types, hashlib, urllib, gzip, re, pylzma

VER ='0.1'
DOB = '18-Sep-22'

plugins = []

if os.name == 'nt':
    initialize_nt()
elif os.name == 'posix':
    initialize_posix()
