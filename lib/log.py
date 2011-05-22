class Log:
    def __init__(self,identifier,query,values=None):
        self.query = query
        self.values = values
        self.identifier = identifier
    def display(self):
        print self.identifier,self.query,self.values
