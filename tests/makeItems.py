import os,random,string,sys

def getWords():
    fp = open('/usr/share/dict/words','r')
    words = [line.strip() for line in fp]
    fp.close()
    return words

def makeItems(n=20):
    words = getWords()
    for i in range(n):
        message = ' '.join([random.choice(words) for i in range(random.randint(20,35))])
        os.system('todo add -m "%s"' % message)

if __name__ == '__main__':
    if len(sys.argv[1:]) > 0:
        makeItems(int(sys.argv[1]))
    else:
        makeItems()
