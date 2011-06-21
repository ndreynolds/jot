import sqlite3, hashlib, time, pickle
try: import cPickle as pickle
except: import pickle
from item import Item
from log import Log
from bin import util 

class Connection:
    '''Creates a sqlite3 database connection and offers methods for selecting, deleting,
       and updating items. All actions are written to the changelog.'''

    def __init__(self,path='~/.jot/jot.db',log='~/.jot/jot.log',changelog='~/.jot/jot.changelog',table='jot',verbose=False):
        '''Constructs a Connection object with option to set locations and verbosity'''
        self.path = util.matchPath(path)
        self.cursor = None
        self.connected = False
        self.verbose = verbose
        self.table = table
        self.changelog = util.matchPath(changelog,mustExist=False)
        self.masterlog = util.matchPath(log,mustExist=False)
        try:
            self.connection = sqlite3.connect(self.path)
            self.cursor = self.connection.cursor()
            self.connected = True
        except sqlite3.Error:
            print 'Fatal: Could not connect to database.'

    def rawQuery(self,query,values=None,commit=True,log=False):
        '''Executes a raw SQL query.'''
        if self.connected:
            if self.verbose:
                print query

            # If possible, we'll still want to use the ? format to escape what's added to the query
            # to prevent SQL injection. For this reason, the values parameter is available. It should
            # be a tuple with the appropriate number of elements.
            if values is not None:
                self.cursor.execute(query,values)
            else:
                self.cursor.execute(query)

            if commit: 
                self.commit()
                # For performance reasons, we don't always want separate transactions for each query
                # SQLite can perform thousands of inserts per second, but usually only about 10 transactions.
                # A commit triggers a new transaction in the sqlite3 module, for large batches we want as few
                # transactions as possible to maintain performance.
            self.log(query,values,log) 

    def insertItem(self,item,commit=True):
        '''Inserts an item.'''
        values = (item.identifier, item.content, item.priority, ','.join(item.tags), item.timestamp)
        # Need to use the ? to insert variables in to the query to protect against injection 
        # We do, however, need to add the table name without escaping.
        query = 'insert into %s(hash,content,priority,tags,ts) values(?,?,?,?,?)' % self.table
        if self.connected:
            self.cursor.execute(query,values)
            if commit:
                self.commit()
            self.log(query,values) # Need to log any queries that add, remove, or modify table rows

    def deleteItem(self,item,commit=True):
        '''Deletes an item.'''
        values = (item.identifier,)
        query = 'delete from %s where hash=?' % self.table
        if self.connected:
            self.cursor.execute(query,values)
            if commit:
                self.commit()
            self.log(query,values)
    
    def updateItem(self,item,commit=True):
        '''Updates an item.'''
        values = (item.content, item.priority, ','.join(item.tags), item.identifier)
        query = 'update %s set content=?, priority=?, tags=? where hash=?' % self.table
        if self.connected:
            self.cursor.execute(query,values)
            if commit:
                self.commit()
            self.log(query,values)

    def grabItem(self, identifier, quiet=False):
        '''Given an identifier hash, returns an Item object.'''
        identifier = self.matchIdentifier(identifier, quiet)
        if identifier is None:
            return None
        values = (identifier,)
        query = 'select * from %s where hash=?' % self.table
        if self.connected:
            self.cursor.execute(query,values)
            row = self.cursor.fetchone()
            if row is not None:
                item = Item(db=self, identifier=row[0], content=row[1], priority=row[2], tags=row[3].split(','), timestamp=row[4])
                return item
            else:
                return None

    def grabMostRecent(self, n=1, offset=0):
        '''Returns the n most recent items, with an optional offset, from the database as a list of Item objects.'''
        query = 'select * from %s order by ts desc' % self.table
        if self.connected:
            self.cursor.execute(query)
            rows = self.cursor.fetchmany(n + offset)
            items = []
            if len(rows) > 0:
                for row in rows:
                    item = Item(db=self,identifier=row[0], content=row[1], priority=row[2], tags=row[3].split(','), timestamp=row[4])
                    items.append(item)
                return items[offset:len(items)]
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
                    item = Item(db=self, identifier=row[0], content=row[1], priority=row[2], tags=row[3].split(','), timestamp=row[4])
                    items.append(item)
                return items
            else:
                return None

    def matchIdentifier(self,identifier,quiet=False):
        '''Since entering partial identifier hashes is allowed, we need a way to match them'''
        values = (identifier + '%',)
        query = 'select hash from %s where hash like ?' % self.table
        if self.connected:
            self.cursor.execute(query,values)
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
        values = (searchStr,)
        query = 'select * from jot where content match ?'
        altQuery = 'select * from jot where content like "%?%"'
        if self.connected:
            try:
                self.cursor.execute(query,values)
            except sqlite3.OperationalError:
                self.cursor.execute(altQuery,values)
            rows = self.cursor.fetchall()
            items = []
            if len(rows) > 0:
                for row in rows:
                    item = Item(db=self, identifier=row[0], content=row[1], priority=row[2], tags=row[3].split(','), timestamp=row[4])
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

    def log(self,query,values=None,useChlog=True):
        '''Logs queries to the log (and changelog), for backup and peer use.'''

        # The change log includes all queries that insert, update, or delete originating from
        # a local jot command.  
        #
        # The master log includes all of the above AND queries originating from bin.util.processChangelog().
        #
        # Changelogs are copied for pushes and pulls, while logs are used for clones. A log has
        # everything needed to make a complete db copy, while a changelog only has changes local to the
        # machine that created it.
        if self.verbose:
            print query
        identifier = hashlib.md5(str(time.time()) + str(values)).hexdigest()
        log = Log(identifier,query,values)
        logfile = open(self.masterlog,'ab')
        pickle.dump(log,logfile)
        logfile.close()
        if useChlog:
            chlogfile = open(self.changelog,'ab')
            pickle.dump(log,chlogfile)
            chlogfile.close()
        return True
