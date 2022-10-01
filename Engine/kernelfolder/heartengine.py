import os
import imp
import StringIO
import datetime
import types
import mmap
import glob
import re
import shutil
import struct
import zipfile
import hashlib
import acutetimelib
import acutekmdfile
import acutersa
import acutefile
import constants

class EngineKnownError(Exception):
    def __init__(self, value):
        self.value = ret_value
    def __str__(self):
        return repr(self.value)

class Engine:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.plugins_path = None
        self.temp_path = None
        self.kmdfiles = []
        self.kmd_modules = []
        self.max_datetime = datetime.datetime(1980, 1, 1, 0, 0, 0, 0)
        acutefile.AcuteTemp().removetempdir()
        self.__set_temppath()

    def __del__(self):
        self.temp_path.removetempdir()

        try:
            shutil.rmtree(self.temp_path.temp_path)
        except OSError:
            pass

    def set_plugins(self, plugins_path, callback_fn=None):
        self.plugins_path = plugins_path
        if constants.DEBUG:
            pu = None
            ret = self.__get_kmd_list(os.path.join(plugins_path, 'acute.lst'), pu)
        else:
            pu = acutersa.read_key(os.path.join(plugins_path, 'key.pkr'))
            if not pu:
                return False
            ret = self.__get_kmd_list(os.path.join(plugins_path, 'acute.kmd'), pu)

        if not ret:
            return False

        if self.verbose:
            print '[*] acute.%s :' % ('lst' if constants.DEBUG else 'kmd')
            print '   ', self.kmdfiles

        for kmd_name in self.kmdfiles:
            kmd_path = os.path.join(plugins_path, kmd_name)
            try:
                name = kmd_name.split('.')[0]
                if constants.DEBUG:
                    a = None
                    module = imp.load_source(name, os.path.splitext(kmd_path)[0] + '.py')
                    try:
                        os.remove(os.path.splitext(kmd_path)[0] + '.pyc')
                    except OSError:
                        pass
                else:
                    a = acutekmdfile.kmd(kmd_path, pu)
                    data = a.body
                    module = acutekmdfile.load(name, data)

                if module:
                    self.kmd_modules.append(module)
                    self.__get_last_kmd_build_time(k)
                else:
                    if isinstance(callback_fn, types.FunctionType):
                        callback_fn(name)
            except IOError:
                pass
            except acutekmdfile.KMDFormatError:
                pass

        fl = glob.glob1(plugins_path, '*.n??')
        for fname in fl:
            try:
                fname = os.path.join(plugins_path, fname)
                buf = open(fname, 'rb').read(12)
                if buf[0:4] == 'kmdS':
                    sdate = acutetimelib.convert_date(struct.unpack('<H', buf[8:10])[0])
                    stime = acutetimelib.convert_time(struct.unpack('<H', buf[10:12])[0])

                    t_datetime = datetime.datetime(sdate[0], sdate[1], sdate[2], stime[0], stime[1], stime[2])

                    if self.max_datetime < t_datetime:
                        self.max_datetime = t_datetime
            except IOError:
                pass

        if self.verbose:
            print '[*] kmd_modules :'
            print '   ', self.kmd_modules
            print '[*] Last updated %s UTC' % self.max_datetime.ctime()

        return True
    def __set_temppath(self):
        self.temp_path = acutefile.AcuteTempfile()

    def create_instance(self):
        ei = EngineInstance(self.plugins_path, self.temp_path, self.max_datetime, self.verbose)
        if ei.create(self.kmd_modules):
            return ei
        else:
            return None

    def __get_last_kmd_build_time(self, kmd_info):
        if constants.DEBUG:
            t_datetime = datetime.datetime.utcnow()
        else:
            d_y, d_m, d_d = kmd_info.date
            t_h, t_m, t_s = kmd_info.time
            t_datetime = datetime.datetime(d_y, d_m, d_d, t_h, t_m, t_s)

        if self.max_datetime < t_datetime:
            self.max_datetime = t_datetime

    def __get_kmd_list(self, acute_kmd_file, pu):
        kmdfiles = []

        if constants.DEBUG:
            lst_data = open(acute_kmd_file, 'rb').read()
        else:
            k = acutekmdfile.KMD(acute_kmd_file, pu)
            lst_data = k.body

        if lst_data:
            msg = StringIO.StringIO(lst_data)
            while True:
                line = msg.readline().strip()
                if not line:
                    break
                elif line.find('.kmd') != -1:
                    kmdfiles.append(line)
                else:
                    continue
        if len(kmdfiles):
            self.kmdfiles = kmdfiles
            return True
        else:
            return False

class EngineInstance:
    def __init__(self, plugins_path, temp_path, max_datetime, verbose=False):
        self.verbose = verbose
        self.plugins_path = plugins_path
        self.temp_path = temp_path
        self.max_datetime = max_datetime

        self.options = {}
        self.set_options()
        self.acutemain_inst = []
        self.update_info = []
        self.result = {}
        self.identified_virus = set()
        self.set_result()

        self.quarantine_name = {}
        self.disinfect_callback_fn = None
        self.update_callback_fn = None
        self.quarantine_callback_fn = None

        self.disable_path = re.compile(r'/<\W+>')

    def create(self, kmd_modules):
        for mod in kmd_modules:
            try:
                t = mod.AcuteMain()
                self.acutemain_inst.append(t)
            except AttributeError:
                continue
        if len(self.acutemain_inst):
            if self.verbose:
                print '[*] Count of AcuteMain: %d' % (len(self.acutemain_inst))
            return True
        else:
            return False

    def init(self, callback_fn = None):
        t_acutemain_inst = []
        if self.verbose:
            print '[*] AcuteMain.init() :'

        for inst in self.acutemain_inst:
            try:
                if constants.DEBUG:
                    ret = inst.init(self.plugins_path, self.options['opt_verbose'])
                else:
                    ret = inst.init(self.plugins_path, False)

                if not ret:
                    t_acutemain_inst.append(inst)
                    if self.verbose:
                        print '    [-] %s.init() : %d' % (inst.__module__, ret)
                else:
                    if isinstance(callback_fn, types.FunctionType):
                        callback_fn(inst.__module__)
            except AttributeError:
                continue
        self.acutemain_inst = t_acutemain_inst
        if len(self.acutemain_inst):
            if self.verbose:
                print '[*] Count of AcuteMain.init() : %d' % (len(self.acutemain_inst))
            return True
        else:
            return False
    def uninit(self):
        if self.verbose:
            print '[*] AcuteMain.uninit() :'
        for inst in self.acutemain_inst:
            try:
                ret = inst.uninit()
                if self.verbose:
                    print '    [-] %s.uninit() : %d' % (inst.__module__, ret)
            except AttributeError:
                continue
    def getinfo(self):
        ginfo = []
        if self.verbose:
            print '[*] AcuteMain.getinfo() :'

        for inst in self.acutemain_inst:
            try:
                ret = inst.getinfo()
                ginfo.append(ret)
                if self.verbose:
                    print '    [-] %s.getinfo() :' % inst.__module__
                    for key in ret.keys():
                        print '        - %-10s : %s' % (key, ret[key])
            except AttributeError:
                continue
        return ginfo

    def listvirus(self, *callback):
        vlist = []
        argc = len(callback)

        if argc == 0:
            cb_fn = None
        elif argc == 1:
            cb_fn = callback[0]
        else:
            return []
        
