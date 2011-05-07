import util

def edit(db,args,config):
    if len(args) == 0:
        print util.decorate('FAIL','Fatal: No reference to item to edit supplied.')
        return False
    for arg in args:
        if arg == 'last':
            item = db.grabMostRecent(1)
        elif len(arg) > 0:
            item = [db.grabItem(arg)]
        else:
            print util.decorate('FAIL','Fatal: No reference to item to edit supplied.')
            return False
    if item is not None:
        item = item[0]
        item.edit()
        item.save()
        print util.decorate('OKGREEN','Item was successfully modified.\n')
        item.display()
        return True
    return False
