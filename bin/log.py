import util
from lib.log import Log
try: import cPickle as pickle
except ImportError: import pickle

def log(args,config):
    '''Unpickles and dumps the todo log. Only really useful
    for development.'''
    
    logfile = open(util.matchPath('~/.todo/todo.log'),'r')
    while True:
        try:
            logitem = pickle.load(logfile)
            logitem.display()
        except EOFError:
            break
    return True
