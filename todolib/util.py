import os,glob

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
