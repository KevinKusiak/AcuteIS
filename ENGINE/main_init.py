import cgi
# from distutils.log import set_threshold
# from distutils.util import copydir_run_2to3
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

from core.engine import *
from utils.const import * 
from utils.args import *
from utils.parserHelp import *

VERSION = '0.01'
BUILD_DATE = 'Feb 05 2022'
RELEASE_DATE = 'Feb 05 2022' 

def defineParsing():
    usage = "Usage: %prog path[s] [options]"
    parser = ModifiedOptionParser(add_help_option=False, usage=usage)

    parser.add_option("-f", "--files",
                      action="store_true", dest="opt_files",
                      default=True)
    parser.add_option("-r", "--arc",
                      action="store_true", dest="opt_arc",
                      default=False)
    parser.add_option("-G",
                      action="store_true", dest="opt_log",
                      default=False)
    parser.add_option("", "--log",
                      metavar="FILE", dest="log_filename")
    parser.add_option("-I", "--list",
                      action="store_true", dest="opt_list",
                      default=False)
    parser.add_option("-e", "--app",
                      action="store_true", dest="opt_app",
                      default=False)
    parser.add_option("-F", "--infp",
                      metavar="PATH", dest="infp_path")
    parser.add_option("", "--qname", 
                      action="store_true", dest="opt_qname",
                      default=False)
    parser.add_option("", "--qhash", 
                      action="store_true", dest="opt_qhash",
                      default=False)
    parser.add_option("-R", "--nor",
                      action="store_true", dest="opt_nor",
                      default=False)
    parser.add_option("-V", "--vlist",
                      action="store_true", dest="opt_vlist",
                      default=False)
    parser.add_option("-p", "--prompt",
                      action="store_true", dest="opt_prompt",
                      default=False)
    parser.add_option("-d", "--dis",
                      action="store_true", dest="opt_dis",
                      default=False)
    parser.add_option("-l", "--del",
                      action="store_true", dest="opt_del",
                      default=False)
    parser.add_option("", "--no-color",
                      action="store_true", dest="opt_nocolor",
                      default=False)
    parser.add_option("", "--move",
                      action="store_true", dest="opt_move",
                      default=False)
    parser.add_option("", "--copy",
                      action="store_true", dest="opt_copy",
                      default=False)
    parser.add_option("", "--update",
                      action="store_true", dest="opt_update",
                      default=False)
    parser.add_option("", "--verbose",
                      action="store_true", dest="opt_verbose",
                      default=False)
    parser.add_option("", "--sigtool",
                      action="store_true", dest="opt_sigtool",
                      default=False)
    parser.add_option("", "--debug",
                      action="store_true", dest="opt_debug",
                      default=False)
    parser.add_option("-?", "--help",
                      action="store_true", dest="opt_help",
                      default=False)


    parser.add_option("", "--feature",
                      type="int", dest="opt_feature",
                      default=0xffffffff)

    return parser


def main():
    args = False
    logo()

if __name__ == '__main__':
    main()