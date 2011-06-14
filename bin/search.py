import util

def search(db,args):
    '''Search item content and display matches.'''
    #
    # Methods:
    #   search [query] 
    #       --displays all items that match the query.
    #
    if len(args) > 0:
        query = args[0]
        items = db.searchContent(query)
    else:
        print util.decorate('FAIL', 'Requires a search parameter.\n    usage: jot search [query]')
        return False
    if items is None:
        print util.decorate('WARNING', 'No matches found for "%s"' % query)
    else:
        print util.decorate('OKGREEN', '%d matching items found for "%s"\n' % (len(items),query))
        for item in items:
            if item is not None:
                item.display()
        return True
    return False
