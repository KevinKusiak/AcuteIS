from optparse import OptionParser

class OptionParsingError(RuntimeError):
    def __init__(self, msg):
        self.msg = msg

class OptionParsingExit(Exception):
    def __init__(self, status, msg):
        self.msg = msg
        self.status = status


class ModifiedOptionParser(OptionParser):
    def error(self, msg):
        raise OptionParsingError(msg)

    def exit(self, status=0, msg=None):
        raise OptionParsingExit(status, msg)