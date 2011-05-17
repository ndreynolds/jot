from lib.item import Item
import util

def add(db,args,config):
    '''Create, fill, save, and display a new todo Item.'''
    #
    # Methods:
    #   add     
    #       --opens the default editor with a temp file. 
    #   add -m "string"
    #       --uses the supplied string as the item content.

    manual = False
    quiet = False
    content = None
    batchMode = False
    priority = 'Normal'
    for tup in args:
        arg1 = tup[0]
        arg2 = tup[1]
        if arg1 == 'm' and arg2 is not None:
            manual = True
            content = arg2
        if arg1 == '-high' or arg1 == 'h':
            priority = 'High'
        if arg1 == '-low' or arg1 == 'l':
            priority = 'Low'
        if arg1 == '-quiet' or arg1 == 'q':
            quiet = True
        if arg1 == '-batch' or arg1 == 'b':
            batchMode = True
    if manual:
        item = Item(db,content=content,priority=priority)
    else:
        item = Item(db,priority=priority)
        item.fill()
    item.save()
    if not quiet:
        print util.decorate('OKGREEN','New item addition was successful.\n')
        item.display()
    return True
