import util

def remove(db,args):
    '''Remove item(s) from the db.'''
    #
    # Methods:
    #   remove [identifier]
    #       --removes the item with the given identifier.
    #   remove all
    #       --removes all todo items.
    #   remove last
    #       --removes the most recent item.
    #

    if len(args) > 0:
        sub = args[0]
        if sub == "all":
            items = db.grabAll()
        elif sub == "last":
            items = db.grabMostRecent(1)
        else:
            items = [db.grabItem(sub)]
        removed = 0 
        for item in items:
            if item is not None:
                item.remove()
                print 'Removed',util.decorate('WARNING',item.identifier)
                removed += 1
        if removed > 0:
            print util.decorate('OKGREEN',str(removed) + ' item(s) successfully removed.')
