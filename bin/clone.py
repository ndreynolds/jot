from lib.peer import Peer
import util,os

def clone(db,args):
    address = args[0]
    newPeer = Peer(address)
    newPeer.clone()
    log = util.matchPath('~/.todo/todo.log.*')
    logfile = open(log,'r')
    print util.decorate('OKGREEN','Data retrieved')
    print 'Preparing to clone'
    db.rawQuery('delete from todo')
    db.rawQuery('delete from transactions')
    count = 0
    print 'Cloning from',address
    for line in logfile:
        line = line.strip()
        query = line[33:]
        db.rawQuery(query,commit=False)
        count += 1
    db.commit()
    logfile.close()
    os.remove(log)
    print 'Done.'
