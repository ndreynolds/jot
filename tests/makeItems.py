import os,random,string,sys

# This is very slow (in comparison to todo's internal batch operations) because it has 
# to use separate db transactions for each addition.  The only solution is to create
# a batch mode for the add command, but I can't think of the benefit outside of testing.

def makeItems(n=20):
    words = ['hello','my','good','friend','it','seems','we','have','a','bit','of','a','problem']
    for i in range(n):
        message = ' '.join([random.choice(words) for i in range(random.randint(20,35))])
        print message
        os.system('todo add --quiet -m "%s"' % message)

if __name__ == '__main__':
    if len(sys.argv[1:]) > 0:
        makeItems(int(sys.argv[1]))
    else:
        makeItems()
    print 'Done.'
