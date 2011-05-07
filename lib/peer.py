import hashlib,os,time
from bin import util

class Peer:
    '''Provides methods for interacting with a peer.'''

    def __init__(self,address,changelog='~/.todo/todo.changelog',log='~/.todo/todo.log'):
        '''Creates a Peer object with an address'''
        self.address = address
        self.changelog = changelog
        self.log = log
    
    def push(self):
        '''Push the changelog to the peer.'''
        destpath = self.changelog + '.' + hashlib.md5(str(time.time())).hexdigest()
        command = 'scp -q %s %s:%s' % (self.changelog,self.address,destpath)
        os.system(command)
        
    def pull(self):
        '''Pull the changelog from the peer.'''
        receivepath = self.changelog + '.' + hashlib.md5(str(time.time())).hexdigest()
        command = 'scp -q %s:%s %s' % (self.address,self.changelog,receivepath)
        os.system(command)
        util.processChangelog() # We can process the changelog immediately

    def clone(self):
        '''Pulls the master log from the peer.'''
        receivepath = self.log + '.' + hashlib.md5(str(time.time())).hexdigest()
        command = 'scp -q %s:%s %s' % (self.address,self.log,receivepath)
        os.system(command)
