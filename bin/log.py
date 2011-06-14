import util
from lib.log import Log
try: import cPickle as pickle
except ImportError: import pickle

def log(args,config):
    '''Unpickles and dumps the jot log. Only really useful
    for development.''' 
    
    def logDump(logPath):
        path = util.matchPath(logPath)
        print '#',path
        logfile = open(path,'r')
        while True:
            try:
                logitem = pickle.load(logfile)
                logitem.display()
            except EOFError:
                break

    logDump('~/.jot/jot.log')
    logDump('~/.jot/jot.changelog')
    return True
