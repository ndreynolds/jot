import os,glob,time
from StringIO import StringIO
try: import cPickle as pickle
except: import pickle
from lib.log import Log

def processChangelog(basepath='~/.todo/todo.changelog'):
    '''Look for foreign changelogs and update and delete them'''
    from lib.connection import Connection
    path = matchPath(basepath,mustExist=False) + '.*'
    logfiles = glob.glob(path)

    def writeQuery(db,log):
        '''Executes the query and records the transaction'''
        if db.matchIdentifier(log.identifier,quiet=True) is None:
            if log.values is not None:
                db.rawQuery(log.query,log.values,commit=False)
            else:
                db.rawQuery(log.query,commit=False)
            transaction = 'insert into transactions(hash,ts) values("%s","%s")' % (log.identifier,time.time()) 
            db.rawQuery(transaction,commit=False)
            return True
        return False

    if len(logfiles) > 0:
        print 'Found new changelog. Updating local database...'
        db = Connection(table='transactions',verbose=False)
        changesCount = 0
        for logfile in logfiles:
            fp = open(logfile,'rb')
            while True:
                try:
                    log = pickle.load(fp)
                    if writeQuery(db,log):
                        changesCount += 1
                except EOFError:
                    break
            fp.close()
            os.remove(logfile)
        db.commit()
        if changesCount > 0:
            print 'Done.'
            print decorate('OKGREEN',str(changesCount) + ' changes were made.')
        else:
            print 'Nothing to update.'

    return True

def decorate(colorCode,text):
    '''Returns a string enveloped by an ANSI color code'''
    colors = {'HEADER' : '\033[95m',
              'OKBLUE' : '\033[94m',
              'OKGREEN' : '\033[92m',
              'WARNING' : '\033[93m',
              'FAIL' : '\033[91m',
              'ENDC' : '\033[0m'}
    return colors[colorCode] + text + colors['ENDC']

def parseArgs(args):
    '''Parse arguments that follow the command'''
    prevArg = None 
    parsedArgs = []
    for arg in args:
        # pairs arguments in to tuples
        if arg[0] == '-': 
            # the first char of the first element of the tuple must be a '-'
            if prevArg is not None:
                tup = prevArg,None
                parsedArgs.append(tup)
            prevArg = arg[1:]
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

def parseConfig(path='~/.todo/todo.conf'):
    '''Return dictionary with configuration .'''
    path = matchPath(path)
    configfile = open(path,'r')
    config = {'debug':False,'editor':'nano'}
    for line in configfile:
        if line[0] != '#':
            line = line.strip().split(':')
            line = [el.strip() for el in line]
            if len(line) > 1:
                if line[1][0] != '#':
                    config[line[0]] = line[1]
    return config

def matchPath(path,mustExist=True):
    '''Matches file paths with bash wildcards and shortcuts to an
       absolute path'''
    if path[0] == '~':
        path = os.getenv('HOME') + path[1:]
    newPath = glob.glob(path)
    if len(newPath) == 0:
        if not mustExist:
            return path
        print 'Fatal: Could not match path: "%s"' % path
        return False
    newPath = newPath[0]
    return os.path.abspath(newPath)

def guessCommand(word):
    '''Tries to 'guess' what the user meant when an unknown command was
       used.'''
    knowns = ['add','version','remove','config','peers','show','search', \
            'edit','pull','push','tag','clone']
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    # uses list comprehensions from norvig.com/spell-correct.html
    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
    replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts    = [a + c + b for a, b in splits for c in alphabet]
    # the set of all the edits of the original word
    edits = set(deletes + transposes + replaces + inserts)
    # the set of all edits found in matches
    matches = set(word for word in edits if word in knowns)
    if len(matches) > 0:
        return matches
    else:
        return None
