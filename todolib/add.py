from item import Item

def add(db,args):
    '''Create, fill, save, and display a new todo Item.'''
    #
    # Methods:
    #   add     
    #       --opens the default editor with a temp file. 
    #   add -m "string"
    #       --uses the supplied string as the item content.
    #
    manual = False
    for tup in args:
        if tup[0][0] == 'm' and tup[1] is not None:
            item = Item(db,content=tup[1])
            manual = True
            break
    if not manual:
        item = Item(db)
        item.fill()
    item.save()
    print 'New Item Added'
    item.display()
    return True
