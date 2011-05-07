from lib.peer import Peer

def pull(args):
    address = args[0]
    newPeer = Peer(address)
    newPeer.pull()
