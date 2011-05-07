import sqlite3, hashlib, time
from item import Item
from bin import util 

class Connection:
    '''Creates a sqlite3 database connection and offers methods for selecting, deleting,
       and updating items. All actions are written to the changelog.'''

    def __init__(self,path='~/.todo/todo.db',log='~/.todo/todo.log',changelog='~/.todo/todo.changelog',table='todo',verbose=False):
        '''Constructs a Connection object with option to set locations and verbosity'''
        self.path = util.matchPath(path)
        self.cursor = None
        self.connected = False
        self.verbose = verbose
        self.table = table
        self.changelog = util.matchPath(changelog,mustExist=False)
        self.log = util.matchPath(log,mustExist=False)
        try:
            self.connection = sqlite3.connect(self.path)
            self.cursor = self.connection.cursor()
            self.connected = True
        except sqlite3.Error:
            print 'Fatal: Could not connect to database.'

    def rawQuery(self,query,commit=True,log=False):
        '''Executes a raw SQL query.'''
        if self.connected:
            if self.verbose:
                print query
            self.cursor.execute(query)
            if commit: 
                self.commit()
                # For performance reasons, we don't always want separate transactions for each query
                # SQLite can perform thousands of inserts per second, but usually only about 10 transactions.
                # A commit triggers a new transaction in the sqlite3 module, for large batches we want as few
                # transactions as possible to maintain performance.
            self.log(query,log) 

    def insertItem(self,item,commit=True):
        '''Inserts an item.'''
        query = 'insert into %s(hash,content,priority,ts) values("%s","%s","%s","%s")' \
            % (self.table,item.identifier, item.content, item.priority, item.timestamp)
        if self.connected:
            self.cursor.execute(query)
            if commit:
                self.commit()
            self.log(query) # Need to log any queries that add, remove, or modify table rows

    def deleteItem(self,item,commit=True):
        '''Deletes an item.'''
        query = 'delete from %s where hash="%s"' % (self.table,item.identifier)
        if self.connected:
            self.cursor.execute(query)
            if commit:
                self.commit()
            self.log(query)
    
    def updateItem(self,item,commit=True):
        '''Updates an item.'''
        query = 'update %s set content="%s", priority="%s" where hash="%s"' \
            % (self.table,item.content,item.priority,item.identifier)
        if self.connected:
            self.cursor.execute(query)
            if commit:
                self.commit()
            self.log(query)

    def grabItem(self, identifier, quiet=False):
        '''Given an identifier hash, returns an Item object.'''
        identifier = self.matchIdentifier(identifier, quiet)
        if identifier is None:
            return None
        query = 'select * from %s where hash="%s"' % (self.table,identifier)
        if self.connected:
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            if row is not None:
                item = Item(db=self,identifier=row[0],content=row[1],priority=row[2],timestamp=row[3])
                return item
            else:
                return None

    def grabMostRecent(self, n=1):
        '''Returns the n most recent items from the database as a list of Item objects.'''
        query = 'select * from %s order by ts desc' % self.table
        if self.connected:
            self.cursor.execute(query)
            rows = self.cursor.fetchmany(n)
            items = []
            if len(rows) > 0:
                for row in rows:
                    item = Item(db=self,identifier=row[0],content=row[1],priority=row[2],timestamp=row[3])
                    items.append(item)
                return items
            else:
                return None

    def grabAll(self):
        '''Returns all items from the database as a list of Item objects.'''
        query = 'select * from %s order by ts desc' % self.table
        if self.connected:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            items = []
            if len(rows) > 0:
                for row in rows:
                    item = Item(db=self,identifier=row[0],content=row[1],priority=row[2],timestamp=row[3])
                    items.append(item)
                return items
            else:
                return None

    def matchIdentifier(self,identifier,quiet=False):
        '''Since entering partial identifier hashes is allowed, we need a way to match them'''
        query = 'select hash from %s where hash like "%s%%"' % (self.table,identifier)
        if self.connected:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            if len(rows) == 0:
                if not quiet:
                    print util.decorate('FAIL','Fatal: No identifier could be matched')
                return None 
            if len(rows) > 1:
                if not quiet:
                    print util.decorate('FAIL','Fatal: Supplied identifier has multiple matches, please be more specific.')
                return None 
            else:
                return str(rows[0][0])

    def searchContent(self,searchStr):
        '''Returns a list of Item objects whose content attribute matches the search string.'''
        query = 'select * from todo where content match "%s"' % searchStr
        altQuery = 'select * from todo where content like "%%%s%%"' % searchStr
        if self.connected:
            try:
                self.cursor.execute(query)
            except sqlite3.OperationalError:
                self.cursor.execute(altQuery)
            rows = self.cursor.fetchall()
            items = []
            if len(rows) > 0:
                for row in rows:
                    item = Item(db=self,identifier=row[0],content=row[1],priority=row[2],timestamp=row[3])
                    items.append(item)
                return items
            else:
                return None

    def commit(self):
        '''Commit the change(s) to the database.'''
        if self.connected:
            self.connection.commit()
            return True
        return False

    def log(self,query,useChlog=True):
        '''Logs queries to the log (and changelog), for backup and peer use.'''

        # The changelog includes all queries that insert, update, or delete originating from
        # a local todo command.  
        #
        # The log includes all of the above AND queries originating from bin.util.processChangelog().
        #
        # Changelogs are copied for pushes and pulls, while logs are used for clones. A log has
        # everything needed to make a complete db copy, while a changelog only has changes local to the
        # machine that created it.

        try:
            if self.verbose:
                print query
            identifier = hashlib.md5(str(time.time()) + query).hexdigest()
            log = open(self.log,'a')
            log.write('%s %s\n' % (identifier,query))
            log.close()
            if useChlog:
                chlog = open(self.changelog,'a')
                log.write('%s %s\n' % (identifier,query))
                chlog.close()
            return True
        except:
            return False

