#!/usr/bin/env python

import sys, glob, os, sqlite3, time, hashlib

# Overview:
#   The program is run by typing todo in to the shell followed
#   by a single whitespace, a command that tells it what to do,
#   and possibly some arguments.
# Examples:
#   todo add    
#       --opens the default editor to enter a todo item
#   todo add -m "item text"   
#       --the same thing without using an editor
#   todo version 
#       --displays version information
#   todo config show
#       --opens the configuration file in the default editor
#   todo remove [hash]
#       --removes the todo item with the given hash identifier
#   todo remove last
#       --removes the most recently created todo item
#   todo remove all
#       --removes all todo items
#   todo peers show
#       --lists peers from the todo.config file

class Item:
    '''Creates a todo item with an identifier and various methods.'''
    def __init__(self, db, identifier=None, priority=None, text=None):
        '''Creates a new todo item or loads one from the database'''
        if identifier is not None:
            pass # Grab item characteristics from db.
        self.timestamp = time.time()
        self.identifier = hashlib.md5(str(time.time())).hexdigest()
        self.priority = priority
        self.content = text

    def fill(self):
        '''Launch the default editor with a file for writing the todo item.'''
        # Look for a default editor using os.getenv
        envs = ['EDITOR','VISUAL']
        editor = None
        for env in envs:
            env = os.getenv(env)
            if env is not None:
                editor = env
                break
        if editor is None:
            editor = 'vim'
        # Launch the editor with a filename self.identifier in the todo directory
        path = matchPath('~/.todo/') + '/' + self.identifier
        syscall = editor + ' ' + path
        os.system(syscall)

    def save(self):
        '''Puts the item in the local database.'''
        db.insertItem(self)

    def remove(self):
        '''Removes the item from the local database.'''
        db.deleteItem(self)

class Connection:
    '''Creates a sqlite3 database connection and offers methods for selecting, deleting,
       and updating items. All actions are written to the changelog.'''
    def __init__(self,path='~/.todo/todo.db',log='~/.todo/todo.changelog'):
        self.path = matchPath(path)
        self.cursor = None
        self.connected = False
        try:
            connection = sqlite3.connect(self.path)
            self.cursor = connection.cursor()
            self.connected = True
        except sqlite3.Error:
            print 'Fatal: Could not connect to database.'

    def insertItem(item):
        '''Inserts an item.'''
        query = 'insert into todo values(%s,%s,%s)' % (item.identifier, item.content, item.timestamp)
        if self.connected:
            self.cursor.execute(query)

    def deleteItem(item):
        '''Deletes an item.'''
        query = 'delete from todo where hash="%s"' % (item.identifier)
        if self.connected:
            self.cursor.execute(query)
    
    def updateItem(item):
        '''Updates an item.'''
        query = 'update todo where hash="%s"' % (item.identifier)
        if self.connected:
            self.cursor.execute(query)

    def grabItem(item):
        '''Retrieves item content, priority, and timestamp, given an identifier.'''
        pass

    def grabMostRecent(item):
        '''Grabs the most recent item from the database.'''
        pass

def main():
    '''Get, interpret, and pass on any commands'''
    config = { 'peers' : {} } # The default configuration, stored in a dictionary
    config = parseConfig(config)
    args = []
    if len(sys.argv) > 1:
        command = sys.argv[1]
    else:
        return False
    if len(sys.argv) > 2:
        args = parseArgs(sys.argv[2:])
    if len(args) > 0:
        args = parseArgs(args)
    if command == 'add':
        add(args)
    if command == 'version':
        version()
    if command == 'remove':
        remove(args)
    if command == 'config':
        config(args)
    if command == 'peers':
        peers(args)
    return True

def parseArgs(args):
    '''Parse arguments that follow the command'''
    prevArg = None 
    parsedArgs = []
    for arg in args:
        if arg[0] == '-':
            if prevArg is not None:
                tup = prevArg,None
                parsedArgs.append(tup)
            prevArg = [ch for ch in arg[1:]]
        elif prevArg is not None:
            tup = prevArg,arg
            parsedArgs.append(tup)
            prevArg = None
        else:
            parsedArgs.append(arg)
    if prevArg is not None:
        tup = prevArg,None
        parsedArgs.append(tup)
    return parsedArgs

def parseConfig(config,path='~/.todo/todo.config'):
    '''Update configuration with settings from todo.config.'''
    path = matchPath(path)
    configfile = open(path,'r')
    for line in configfile:
        if line[0].isalpha():
            line = line.strip().split()
            if line[1] != '#':
                config[line[0]] = line[1]
    return config

def matchPath(path):
    '''Matches file paths with bash wildcards and shortcuts to an
       absolute path'''
    if path[0] == '~':
        path = os.getenv('HOME') + path[1:]
    newPath = glob.glob(path)
    if len(newPath) == 0:
        print 'Fatal: Could not match path: "%s"' % path
        return False
    newPath = newPath[0]
    return os.path.abspath(newPath)

if __name__ == '__main__':
    usage = '''
Usage: todo [command]
For help: todo help
    '''
    x = Item()
    x.addContent()
    result = main()
    if not result:
        print usage
