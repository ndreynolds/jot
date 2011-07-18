from lib.pager import Pager

def show(db,args):
    '''Display saved items in a variety of ways.'''

    if len(args) > 0:
        sub = args[0]
        if sub == 'all':
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
        elif db.isTag(sub):
            print 'yuppers'
            items = db.grabAllWithTag(sub)
        else:
            items = [db.grabItem(sub)]
    else:
        items = db.grabMostRecent(5)
    if items is None:
        print 'No items to display'
        return False
    if len(items) > 0:
        page = False
        wc = sum([len(item.content) for item in items if item is not None]) 
        if wc > 1000:
            page = True
            pager = Pager()
            pager.begin()
        for item in items:
            if item is not None:
                item.display()
        if page:
            pager.end()
        return True
    print 'No items to display'
    return False
