def show(db,args):
    '''Display saved items in a variety of ways.'''
    #
    # Methods:
    #   show
    #       --displays the 5 most recent items.
    #   show all 
    #       --displays all jot items.
    #   show [identifier]
    #       --shows the item with the given identifier.
    #   show last
    #       --shows the most recent item.
    #
    if len(args) > 0:
        sub = args[0]
        if sub == 'all':
            items = db.grabAll()
        elif sub == 'last':
            items = db.grabMostRecent(1)
        else:
            items = [db.grabItem(sub)]
    else:
        items = db.grabMostRecent(5)
    if items is None:
        print 'No items to display'
        return False
    if len(items) > 0:
        for item in items:
            if item is not None:
                item.display()
        return True
    print 'No items to display'
    return False
