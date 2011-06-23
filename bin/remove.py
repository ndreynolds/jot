import util

def remove(db,args):
    '''Remove item(s) from the db.'''

    if len(args) > 0:
        sub = args[0]
        if sub == "all":
            items = db.grabAll()
        elif sub == 'last':
            items = db.grabMostRecent(1)
        elif sub == 'last^':
            items = db.grabMostRecent(1,1)
        elif sub == 'last^^':
            items = db.grabMostRecent(1,2)
        elif sub[0:5] == 'last~' and len(sub) == 6:
            items = db.grabMostRecent(1,int(sub[5]))
        elif sub[0:4] == 'last' and len(sub) == 5:
            items = db.grabMostRecent(int(sub[4]))
        else:
            items = [db.grabItem(sub)]
        removed = 0 
        for item in items:
            if item is not None:
                item.remove(commit=False) # Don't commit so we can bundle transactions. 
                print 'Removed',util.decorate('WARNING',item.identifier)
                removed += 1
        db.commit()
        if removed > 0:
            print util.decorate('OKGREEN',str(removed) + ' item(s) successfully removed.')
