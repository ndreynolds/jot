import os,random,string,sys

def makeItems(n=20):
    for i in range(n):
        letters = [ch for ch in string.letters]
        message = ''.join([random.choice(letters) for i in range(random.randint(20,35))])
        os.system('todo add -m "%s"' % message)

if __name__ == '__main__':
    if len(sys.argv[1:]) > 0:
        makeItems(int(sys.argv[1]))
    else:
        makeItems()
