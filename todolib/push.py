from peer import Peer

def push(args):
    address = args[0]
    newPeer = Peer(address)
    newPeer.push()
