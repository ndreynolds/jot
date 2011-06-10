import util

def tag(db,args):
    '''Associate an item with one or more tags'''
    #
    # The tag command is used to associate an item with a tag. This can
    # be done with the add command's -t flag. Here, we're tagging preexisting
    # items. Since an item can have multiple tags, we're appending tags. They
    # can be removed (individually or collectively) with the remove subcommand.
    #
    # tag [identifier] [tag,tag, ...]
    # tag last [tag,tag, ...]
    #
    # tag remove [identifier] [tag]
    #
    if len(args) > 1:
        # tag remove
        if args[0] == 'remove':
            if args[1] == 'last':
                item = db.grabMostRecent()[0] # this method always returns a list or None
            else:
                item = db.grabItem(args[1])
            if item is not None: 
                # the Connection object's methods return None when they can't
                # get an item (most likely because the identifier can't be matched)
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
            item = db.grabMostRecent()[0]
        else: # assume args[0] is an identifier hash
            item = db.grabItem(args[0])
        if item is not None:
            newTags = args[1].split(',')
            if len(item.tags) != 0:
                item.tags = newTags
            else:
                item.tags += newTags
            item.save()
            return True
        else:
            return False
    return False
