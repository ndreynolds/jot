import util

def edit(db,args,config):
    if len(args) == 0:
        print util.decorate('FAIL','Fatal: No reference to item to edit supplied.')
        return False
    for arg in args:
        if arg == 'last':
            items = db.grabMostRecent(1)
        elif arg == 'last^':
            items = db.grabMostRecent(1,1)
        elif arg == 'last^^':
            items = db.grabMostRecent(1,2)
        elif arg[0:5] == 'last~' and len(arg) == 6:
            items = db.grabMostRecent(1,int(arg[5]))
        elif len(arg) > 0:
            items = [db.grabItem(arg)]
        else:
            print util.decorate('FAIL','Fatal: No reference to item to edit supplied.')
            return False
    if items is not None:
        item = items[0]
        item.edit()
        item.save()
        print util.decorate('OKGREEN','Item was successfully modified.\n')
        item.display()
        return True
    return False
