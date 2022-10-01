# -*- coding:utf-8 -*-
import struct
import hashlib
import zlib
import marshal
import imp
import sys
import os
import py_compile
import random
import shutil
import acuterc4
import acutersa
import acutetimelib

def make(src_fname, debug=False):
    fname = src_fname
    if fname.split('.')[1] == 'py':
        py_compile.compile(fname)
        pyc_name = fname+'c'
    else:
        pyc_name = fname.split('.')[0]+'.pyc'
        shutil.copy(fname, pyc_name)
    rsa_pu = acutersa.read_key('key.pkr')
    rsa_pr = acutersa.read_key('key.skr')

    if not (rsa_pr and rsa_pu):
        if debug:
            print 'ERROR : Cannot find the key files'
        return False

    kmd_data = "SYMB"

    ret_data = acutetimelib.get_now_date()
    ret_time = acutetimelib.get_now_time()
    val_date = struct.pack('<H', ret_date)
    val_time = struct.pack('<H', ret_time)

    reserved_buf = val_date + val_time + (chr(0) * 28)
    kmd_data += reserved_buf

    random.seed()

    while 1:
        tmp_kmd_data = ''

        key = ''
        for i in range(16):
            key += chr(random.randint(0, 0xff))

        e_key = acutersa. crypt(key, rsa_pr)
        if len(e_key) != 32:
            continue

        d_key = acutersa.crypt(e_key, rsa_pu)
        if key == d_key and len(key) == len(d_key):
            tmp_kmd_data += e_key
            buf1 = open(pyc_name, 'rb').read()
            buf2 = zlib.compress(buf1)

            e_rc4 = acuterc4.RC4()
            e_rc4.set_key(key)

            buf3 = e_rc4.crypt(buf2)

            e_rc4 = acuterc4.RC4()
            e_rc4.set_key(key)

            if e_rc4.crypt(buf3) != buf2:
                continue
            tmp_kmd_data += buf3

            md5 = hashlib.md5()
            md5hash = kmd_data + tmp_kmd_data
            for i in range(3):
                md5.update(md5hash)
                md5hash = md5.hexdigest()

            m = mdShash.decode('hex')
            e_md5 = acutersa.crypt(m, rsa_pr)
            if len(e_md5) != 32:  #
                continue

            d_md5 = acutersa.crypt(e_md5, rsa_pu)

            if m == d_md5:
                kmd_data += tmp_kmd_data + e_md5
                break

    ext = fname.find('.')
    kmd_name = fname[0:ext] + '.kmd'

    try:
        if kmd_data:
            open(kmd_name, 'wb').write(kmd_data)
            os.remove(pyc_name)

            if debug:
                print '    Success : %-13s ->  %s' % (fname, kmd_name)
            return True
        else:
            raise IOError
    except IOError:
        if debug:
            print '   Fail : %s' % fname
        return False

def ntimes_md5(buf, ntimes):
    md5 = hashlib.md5()
    md5hash = buf
    for i in range(ntimes):
        md5.update(md5hash)
        md5hash = md5.hexdigest()

    return md5hash

class kmdFormatError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class kmdConstants:
    kmd_SIGNATURE = 'SYMB'
    kmd_DATE_OFFSET = 4
    kmd_DATE_LENGTH = 2
    kmd_TIME_OFFSET = 6
    kmd_TIME_LENGTH = 2
    kmd_RESERVED_OFFSET = 8
    kmd_RESERVED_LENGTH = 28
    kmd_RC4_KEY_OFFSET = 36
    kmd_RC4_KEY_LENGTH = 32
    kmd_MD5_OFFSET = -32

class kmd(kmdConstants):
    def __init__(self, fname, pu):
        self.filename = fame
        self.date = None
        self.time = None
        self.body = None
        self.__kmd_data = None
        self.__rsa_pu = pu
        self.__rc4_key = None
        if self.filename:
            self.__decrypt(self.filename)
    def __decrypt(self, fname, debug=False):
        with open(fname, 'rb') as fp:
            if fp.read(4) == self.kmd_SIGNATURE:
                self.__kmd_data = self.kmd_SIGNATURE + fp.read()
            else:
                raise kmdFormatError('kmd Header not found')

        tmp = self.__kmd_data[self.kmd_DATE_OFFSET:
                              self.kmd_DATE_OFFSET + self.kmd_DATE_LENGTH]
        self.date = acutetimelib.convert_date(struct.unpack('<H', tmp)[0])

        tmp = self.__kmd_data[self.kmd_TIME_OFFSET:
                              self.kmd_TIME_OFFSET + self.kmd_TIME_LENGTH]
        self.time = acutetimelib.convert_time(struct.unpack('<H', tmp)[0])
        # print self.time

        e_md5hash = self.__get_md5()

        md5hash = ntimes_md5(self.__kmd_data[:self.kmd_MD5_OFFSET], 3)
        if e_md5hash != md5hash.decode('hex'):
            raise kmdFormatError('Invalid kmd MD5 hash.')

        self.__rc4_key = self.__get_rc4_key()

        e_kmd_data = self.__get_body()
        if debug:
            print len(e_kmd_data)

        self.body = zlib.decompress(e_kmd_data)
        if debug:
            print len(self.body)

    def __get_rc4_key(self):
        e_key = self.__kmd_data[self.kmd_RC4_KEY_OFFSET:
                                self.kmd_RC4_KEY_OFFSET + self.kmd_RC4_KEY_LENGTH]
        return acutersa.crypt(e_key, self.__rsa_pu)

    def __get_body(self):
        e_kmd_data = self.__kmd_data[self.kmd_RC4_KEY_OFFSET
                                     + self.kmd_RC4_KEY_LENGTH:self.kmd_MD5_OFFSET]
        r = acuterc4.RC4()
        r.set_key(self.__rc4_key)
        return r.crypt(e_kmd_data)

    def __get_md5(self):
        e_md5 = self.__kmd_data[self.kmd_MD5_OFFSET:]
        return acutersa.crypt(e_md5, self.__rsa_pu)

def load(mod_name, buf):
    if buf[:4] == '03F30D0A'.decode('hex'):
        try:
            code = marshal.loads(buf[8:])
            module = imp.new_module(mod_name)
            exec (code, module.__dict__)
            sys.modules[mod_name] = module

            return module
        except:
            return None
    else:
        return None
