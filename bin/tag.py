import util

def tag(db,args):
    '''Associate an item with one or more tags'''

    if len(args) > 1:
        # tag remove
        if args[0] == 'remove':
            if args[1] == 'last':
                items = db.grabMostRecent() # this method always returns a list or None
            elif args[1] == 'last^':
                items = db.grabMostRecent(1,1)
            elif args[1] == 'last^^':
                items = db.grabMostRecent(1,2)
            elif args[1][0:5] == 'last~' and len(args[1]) == 6:
                items = db.grabMostRecent(1,int(args[1][5]))
            elif args[1][0:4] == 'last' and len(args[1]) == 5:
                items = db.grabMostRecent(int(args[1][4]))
            else:
                items = [db.grabItem(args[1])]
            if items is not None: 
                # the Connection object's methods return None when they can't
                # get an item (most likely because the identifier can't be matched)
                for item in items:
                    try: # try to remove specific tag if args[2] is set.
                        item.tags = [el for el in item.tags if el != unicode(args[2])]
                    except IndexError:
                        item.tags = [] # reset the list to 0 elements.
                    item.save()
                return True
            else:
                return False
        # tag
        if args[0] == 'last': # check for last keyword
            items = db.grabMostRecent()
        elif args[0] == 'last^':
            items = db.grabMostRecent(1,1)
        elif args[0] == 'last^^':
            items = db.grabMostRecent(1,2)
        elif args[0][0:5] == 'last~' and len(args[0]) == 6:
            items = db.grabMostRecent(1,int(args[0][5]))
        elif args[0][0:4] == 'last' and len(args[0]) == 5:
            items = db.grabMostRecent(int(args[0][4]))
        else: # assume args[0] is an identifier hash
            items = [db.grabItem(args[0])]
        if items is not None:
            newTags = args[1].split(',')
            for item in items:
                if len(item.tags) != 0:
                    item.tags = newTags
                else:
                    item.tags += newTags
                item.save()
            return True
        else:
            return False
    return False
