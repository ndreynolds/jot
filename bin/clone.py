from lib.peer import Peer
import util

def clone(db,args):
    address = args[0]
    newPeer = Peer(address)
    newPeer.clone()
    log = '~/.todo/todo.log.*'
    log = open(util.matchPath(log),'r')
    print util.decorate('OKGREEN','Data retrieved')
    print 'Preparing to clone'
    db.rawQuery('delete * from todo')
    db.rawQuery('delete * from transactions')
    count = 0
    print 'Cloning from',address
    for line in log:
        line = line.strip()
        query = line[33:]
        db.rawQuery(query,commit=False)
        count += 1
    db.commit()
    log.close()
    os.remove(log)
    print 'Done.'
