import sys
import os
import threading
import atexit

BASE_PATH = os.path.dirname(__file__)
LOG_PATH = os.path.join(BASE_PATH, 'output', 'build.log')

LOG_FILE = open(LOG_PATH, 'w')
log_writer_lock = threading.Lock()

def close_log():
    sys.stderr = sys.__stderr__
    sys.stdout = sys.__stdout__
    with log_writer_lock:    
        LOG_FILE.flush()
        LOG_FILE.close()
        

atexit.register(close_log)

class STD(object):
    
    def __init__(self, std, stream_type):
        self._std = std
        self._stream_type = stream_type
    
    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
            
        return getattr(self._std, item)
        
    def write(self, data):
        with log_writer_lock:
            LOG_FILE.write(self._stream_type + ': ' + data)
            LOG_FILE.flush()
            self._std.write(data)
            self.flush()
