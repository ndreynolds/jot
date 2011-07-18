import os, sys, tempfile, subprocess

class Pager:
    def begin(self):
        '''Start redirecting stdout to the pager.'''
        self.__setPager()
        self.temp_path = tempfile.mkstemp()[1]
        self.temp = open(self.temp_path, 'a')
        sys.stdout = self.temp

    def __setPager(self):
        '''Get and set the pager command from the system variable.'''
        self.pager = os.getenv('PAGER')
        if self.pager is None:
            self.pager = 'less'

    def end(self):
        '''Start the pager, then reset stdout.'''
        self.temp.flush()
        self.temp.close()
        proc = subprocess.Popen(['less', self.temp_path], stdin=subprocess.PIPE)
        proc.communicate()
        sys.stdout = sys.__stdout__
