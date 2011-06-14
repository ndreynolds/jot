from lib.item import Item
import util

def add(db, args, config):
    '''Create, fill, save, and display a new jot Item.'''
    #
    # Arguments:
    #   [none]     
    #           opens the default editor with a temp file. 
    #
    #   -m "string"
    #   --manual "string"
    #           uses the supplied string as the item content.
    #
    #   -q
    #   --quiet
    #           suppress output, would really only make sense to
    #           run with -m, but works either way.
    #   -h
    #   --high
    #           attaches a 'high' priority to the item. Priority
    #           defaults to normal when this and the -l option are
    #           omitted.
    #   
    #   -l
    #   --low
    #           attaches a 'low' priority to the item.
    #
    #   -t "string, string, ... "
    #   --tags "string, string, ... "
    #           attaches one or more comma-separated strings as
    #           to the item as tags. These are optional and can
    #           always be added later with the tag command.

    manual = False
    quiet = False
    content = None
    batchMode = False
    priority = 'Normal'
    tags = None
    for tup in args:
        arg1 = tup[0]
        arg2 = tup[1]
        if (arg1 == 'm' or arg1 == '-manual') and arg2 is not None:
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
        if (arg1 == '-tags' or arg1 == 't') and arg2 is not None:
            tags = arg2.split(',')
            
    if manual:
        item = Item(db, content=content, priority=priority, tags=tags)
    else:
        item = Item(db, priority=priority, tags=tags)
        item.fill()
    item.save()
    if not quiet:
        print util.decorate('OKGREEN','New item addition was successful.\n')
        item.display()
    return True
