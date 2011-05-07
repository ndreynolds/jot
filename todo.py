#!/usr/bin/env python

import sys, glob, os, time
    
def main():
    '''Get, interpret, and pass on any commands'''
    
    # Find and import support files
    path = matchPath('~/.todo')
    sys.path.append(path)
    # Class modules
    from todolib import item, connection, util
    # Command modules
    from todolib import add, version, remove, show, peer, config, search, edit, pull, push

    # Parse the configuration file
    config = { 'peers' : {} }
    config = util.parseConfig(config)

    # Apply changelog
    util.processChangelog()

    # Parse the command/arguments
    args = []
    if len(sys.argv) > 1:
        command = sys.argv[1]
    else:
        return False
    if len(sys.argv) > 2:
        args = util.parseArgs(sys.argv[2:])
    if len(args) > 0:
        args = util.parseArgs(args)

    # Create a database connection
    db = connection.Connection()

    # Pass off the db and any arguments to a 
    # command-specific function.
    if command == 'add':
        add.add(db,args)
    elif command == 'version':
        version.version()
    elif command == 'remove':
        remove.remove(db,args)
    elif command == 'config':
        config.config(args)
    elif command == 'peers':
        peer.peer(args)
    elif command == 'show':
        show.show(db,args)
    elif command == 'search':
        search.search(db,args)
    elif command == 'edit':
        edit.edit(db,args)
    elif command == 'pull':
        pull.pull(args)
    elif command == 'push':
        push.push(args)
    else:
        return False
    return True

def matchPath(path):
    '''Matches file paths with bash wildcards and shortcuts to an
       absolute path'''
    import os
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
    result = main()
    if not result:
        print usage
