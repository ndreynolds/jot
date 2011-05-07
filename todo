#!/usr/bin/env python

import sys, glob, os, time
    
usage = '''
Usage:    todo [command]
For help: todo help
'''
    
def main():
    '''Get, interpret, and pass on any commands'''
    
    # Find and import support files
    path = os.getenv('HOME') + '/.todo'
    sys.path.append(path)

    # Class modules
    from lib import item, connection, peer

    # Command modules
    from bin import add, version, remove, show, util, config, search, edit, pull, push

    # Parse the configuration file
    config = util.parseConfig()

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
        add.add(db,args,config)
    elif command == 'version':
        version.version()
    elif command == 'remove' or command == 'rm':
        remove.remove(db,args)
    elif command == 'config':
        config.config(args)
    elif command == 'show':
        show.show(db,args)
    elif command == 'search':
        search.search(db,args)
    elif command == 'edit':
        edit.edit(db,args,config)
    elif command == 'pull':
        pull.pull(args)
    elif command == 'push':
        push.push(args)
    else:
        print util.decorate('FAIL','Fatal: Command not recognized.')
        guess = util.guessCommand(command)
        if guess is not None:
            print 'Did you mean:',' or '.join(guess)
        return False
    return True

if __name__ == '__main__':
    result = main()
    if not result:
        print usage
