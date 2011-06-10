from lib.peer import Peer
import util,os

def clone(db,args):
    address = args[0]
    newPeer = Peer(address)
    newPeer.clone()
    os.remove(log)
    print 'Done.'
