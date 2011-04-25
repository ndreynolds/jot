def setup():
    '''Puts todo.py in bin, Makes the directory, database, and config file for todo'''
    import os,stat,shutil,sqlite3,todo
    relative_path = '/.todo/'
    base_path = os.getenv('HOME')
    path = base_path + relative_path
    dbpath = path + 'todo.db'
    cpath = path + 'todo.config'
    lbin = '/usr/local/bin'
    sbin = '/usr/bin'
    # Copy todo.py to /usr/local/bin
    try:
        shutil.copy('todo.py','todo')
    except IOError:
        print 'Fatal: Permission Denied'
        print '''Try running:
              sudo python setup.py'''
        return False
    os.chmod('todo',0755)
    if os.path.exists(lbin):
        try:
            shutil.copy('todo',lbin)
            print 'Moved todo to',lbin
        except IOError:
            print 'Fatal: Permission Denied'
            print '''Try running:
                  sudo python setup.py'''
            return False
    else:
        if os.path.exists(sbin):
            try:
                shutil.copy('todo',sbin)
                print 'Moved todo to',sbin
            except IOError:
                print 'Fatal: Permission Denied'
                print '''Try running:
                      sudo python setup.py'''
                return False
        else:
            print 'Fatal: Could not find',lbin,'or',sbin
            return False
    # Make the directory:
    if not os.path.exists(path):
        print 'Created base directory at',path
        os.mkdir(path)
    else:
        print 'Fatal: Base directory already exists:',path
        print '''To remove todo, run:
                    todo remove'''
        return False
    # Make the database:
    if not os.path.exists(dbpath):
        print 'Initialized database at',dbpath
        c,connected = todo.dbConnect(dbpath)
        if connected:
            c.execute('''create table todo (hash text, descrip text, ts datetime)''')
            c.close()
        else:
            print 'Fatal: Could not create database'
            return False
    else:
        print 'Fatal: Database already exists:',path + 'todo.db'
        print '''To remove todo, run:
                    todo remove'''
        return False
    # Move the configuration file:
    if not os.path.exists(cpath):
        try:
            shutil.copy('todo.config',cpath)
            print 'Copying std. config to',cpath
        except IOError:
            print 'Fatal: Permission Denied'
            print '''Try running:
                        sudo python setup.py'''
            return False
    return True

if __name__ == '__main__':
    result = setup()
    if result:
        print 'Installation Successful.'
    else:
        print 'Installation Failed.'
