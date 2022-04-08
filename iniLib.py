import configparser as cp
import os

class IniFile(object):
    def __init__(self,_file):
        self.file = _file

    def write(self,sec,key,value):
        try:
            config = cp.ConfigParser()
            config.read(self.file)
            if not sec in config.sections():
                config[sec] = {}
                config[sec][key] = ""
                config.write(open(self.file, 'w'))
            config[sec][key] = value
            config.write(open(self.file, 'w'))
        except:
            return False,traceback.format_exc()
    
    def read(self,sec,key):
        try:
            config = cp.ConfigParser()
            config.read(self.file)
            if not sec in config.sections():
                return False,"Section not found!"
            if not key in config[sec]:
                return False,"Key not found!"
            return True,config[sec][key]
        except:
            return False,traceback.format_exc()