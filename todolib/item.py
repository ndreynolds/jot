import time, hashlib, os, tempfile

class Item:
    '''Creates a todo item with an identifier and various methods.'''
    def __init__(self, db, identifier=None, priority=None, content=None, timestamp=None):
        '''Creates a new todo item, with new or preset attributes'''

        # By setting parameters, we can create a clone of any previous Item instance that's
        # attributes are saved in the database. This is handled by giving an identifier to
        # the getItem method of the Connection class, which then creates the clone with the
        # appropriate parameters.

        if timestamp is None:
            self.timestamp = time.time()
        else:
            self.timestamp = timestamp
        if identifier is None:
            self.identifier = hashlib.md5(str(time.time())).hexdigest()
        else:
            self.identifier = identifier
        if priority is None:
            self.priority = priority
        else:
            self.priority = priority
        self.content = content
        self.db = db

    def fill(self):
        '''Launch an editor with a tempfile for filling in the item's content,
           then retrieve the content.'''
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
        path = tempfile.mkstemp()[1]
        syscall = editor + ' ' + path
        os.system(syscall)
        if os.path.exists(path):
            fp = open(path,'r')
            self.content = ''.join([line for line in fp])
            fp.close()
            print 'Content saved'
            return True
        else:
            print 'Aborting'
            return False
        
    def save(self):
        '''Puts the item in the local database.'''
        if self.content is not None:
            self.db.insertItem(self)

    def remove(self):
        '''Removes the item from the local database.'''
        self.db.deleteItem(self)

    def display(self):
        '''Prints the item's attributes.'''
        print self.identifier
        print self.timestamp
        print self.priority
        print self.content
