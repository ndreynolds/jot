def setup(config):
    '''Puts jot.py in bin, Makes the directory, database, and config file for jot'''
    import os,stat,shutil,sqlite3
    from bin import util
    # Set options from config
    install_path = config['--path'] 
    # Everything else is based on $HOME
    relative_path = '/.jot/'
    base_path = os.getenv('HOME')
    path = base_path + relative_path
    dbpath = path + 'jot.db'
    cpath = path + 'jot.conf'
    # Copy jot.py to install_path 
    try:
        shutil.copy('jot.py','jot') # Strip .py
    except IOError:
        print 'Fatal: Permission Denied'
        print 'jot was trying to make a copy of jot.py as jot'
        print 'A copy of file "jot" most likely already exists, and you lack permission to overwrite it.'
        print 'Try running:'
        print '    sudo python setup.py'
        return False
    os.chmod('jot',0755) # Make it executable
    if os.path.exists(install_path):
        try:
            shutil.copy('jot',install_path)
            print 'Moved jot to',install_path
        except IOError:
            print 'Fatal: Permission Denied'
            print 'jot was trying to move the executable to',install_path
            print 'Try running:'
            print '    sudo python setup.py'
            print 'Or install jot in a directory you own with:'
            print '    python setup.py --path [path]'
            return False
    # Make the directory:
    if not os.path.exists(path):
        print 'Created base directory at',path
        os.mkdir(path)
    else:
        print 'Fatal: Base directory already exists:',path
        print 'To remove jot, run:'
        print '    jot remove'
        return False
    # Make the database:
    if not os.path.exists(dbpath):
        print 'Initialized database at',dbpath
        connection = sqlite3.connect(dbpath)
        c = connection.cursor()
        try:
            c.execute('''create virtual table jot using fts4(hash text, content text, priority text, tags text, ts datetime)''')
        except sqlite3.OperationalError:
            print 'Warning--fts3/fts4 not supported. Falling back to basic table, this may affect search speed and accuracy.'
            c.execute('''create table jot (hash text, content text, priority text, ts datetime)''')
        c.execute('''create table transactions (hash text, ts datetime)''')
        connection.commit()
        c.close()
    else:
        print 'Fatal: Database already exists:',path + 'jot.db'
        print 'To remove jot, run:'
        print '    jot remove'
        return False
    # Move the configuration file:
    if not os.path.exists(cpath):
        try:
            shutil.copy('jot.conf',cpath)
            print 'Copied std. config to',cpath
        except IOError:
            print 'Fatal: Permission Denied'
            print '''Try running:
                        sudo python setup.py'''
            return False
    # Move the support modules:
    try:
        shutil.copytree('lib',path + 'lib')
        shutil.copytree('bin',path + 'bin')
        print 'Moved support modules to',path
    except IOError:
        print 'Fatal: Permission Denied'
        print '''Try running:
                    sudo python setup.py'''
    # Change the ownership of .jot:
    # 
    # Why? When sudo is used to run this, root owns the directory which causes problems connecting to the db
    # as a normal user. To fix this, we first need to determine whether sudo was used to run this script. 
    # We'll check the $SUDO_USER system variable and change the ownership to that user if it's set.  If it's
    # not set, we can only assume sudo is not being used and we'll leave the ownership alone. If the script
    # was run while logged in as root, there's not a lot we can do.  The user will have to change the ownership
    # manually.
    try:
        sudo_user = os.getenv('SUDO_USER')
        os.chmod(path,0777)
        os.chmod(dbpath,0777)
    except OSError:
        print 'Fatal: Could not set database permissions. jot needs write access to the database.'
        return False
    return True

if __name__ == '__main__':
    import sys
    config = {
            '--path' : '/usr/local/bin'
            }
    pos = 0
    for arg in sys.argv[1:]:
        if arg in config.iterkeys():
            config[arg] = sys.argv[pos+2]
        pos += 1
    if setup(config):
        print 'Installation Successful.'
    else:
        print 'Installation Failed.'
