from ConfigParser import SafeConfigParser
from multiprocessing import Process, Queue
import getpass
import poplib
import sys
import os
import time



global debug
debug = False

global qIncomingMail
qIncomingMail = Queue()

global qMessageObj
qMessageObj = Queue()

global qMessageStore
qMessageStore = Queue()


class Config(object):
    def __init__(self):
        self.parser = SafeConfigParser()
        config_dir = './config/'
        for f in os.listdir(config_dir):
            if f[-4:] == '.cfg':

                self.parser.read(config_dir+f)


        for section_name in self.parser.sections():

            if debug:
                print 'Section:', section_name

            setattr(self, section_name, self.parser._sections[section_name])

            

            if debug:
                print '  Options:', self.parser.options(section_name)

            if self.parser.has_option(section_name, 'type'):  # bit of magic to build lists of types
                
                if self.parser._sections[section_name]['type'].lower() == 'endpoint':
                    if not hasattr(self, 'endpoints'):
                        setattr(self, 'endpoints', {})
                        
                    
                    for schema in self.parser._sections[section_name]['filetypes'].split(','):
                        
                        getattr(self, 'endpoints')[schema] = self.parser._sections[section_name]['__name__']
                    

                if not hasattr(self, self.parser.get(section_name, 'type')):
                    setattr(self, self.parser.get(section_name, 'type'), [])

                getattr(self, self.parser.get(section_name, 'type')).append(section_name)

global c
c = Config()


def logging():
    import logging

    

    log = logging.getLogger('Octopus')
    exec("log.setLevel(logging."+c.Logging['baselevel']+")")
    # create file handler which logs even debug messages
    fh = logging.FileHandler('./octopus.log')
    exec("fh.setLevel(logging."+c.Logging['filelevel']+")")
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    exec("ch.setLevel(logging."+c.Logging['screenlevel']+")")
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    # add the handlers to logger
    log.addHandler(ch)
    log.addHandler(fh)

    return log



global log
log = logging()


class MT4Schema(object):
    def __init__(self):
        pass




class omail(object):
    def __init__(self):
        self.headers = ('Return-Path', 'Received', 'DKIM-Signature', 'MIME-Version', 'Reply-To', 'Date', 
                       'Message-ID', 'Subject', 'From', 'To', 'Content-Type')        
        for x in self.headers:
            setattr(self, x, '')


def getMail():            
    """Connects to pop server and retrieves messages"""

    while 1:

        try:
            Mailbox = poplib.POP3(c.Server['host'], c.Server['port']) 
            Mailbox.user(c.Server['username']) 
            Mailbox.pass_(c.Server['password']) 
            numMessages = len(Mailbox.list()[1])

            log.info("Connected to %s and there are %i messages"%(c.Server['host'], numMessages))
    
            for i in range(numMessages):
                msg = Mailbox.top(i+1, 10000)
                qIncomingMail.put(msg)
            Mailbox.quit()
            time.sleep(60)
        except:
            log.error("Failed to connect to %s"%c.Server['host'])


def getMessagefromQ():
    
    return qIncomingMail.get()


def messages2Obj(msg):

    omsg = omail()
    htype = ''
    for x in msg[1]:
        if x.split(':')[0] in omsg.headers:
            htype = x.split(':')[0]
            if len(getattr(omsg, htype)) == 0:
                setattr(omsg, htype, x.split(':')[1:][0])
            else:
                setattr(omsg, htype, "%s\n%s"%(getattr(omsg,htype), x.split(':')[1:][0]))
        else:
            setattr(omsg, htype, "%s\n%s"%(getattr(omsg,htype), x))
            
    if debug:        
        for k in omsg.headers:
            print k, getattr(omsg, k)
    
    return omsg
        
def messageProcessingFactory():
     
    while 1:
        try:
            m = getMessagefromQ()
            om = messages2Obj(m)
            # Now message is useful object. Process headers/body and store.
            
            # validate that we want to process it.
            
            # pull out body and objectise it.
            
    
            qMessageObj.put()
            qMessageStore.put()
        except:
            log.error("Failed to process Message: %"%m)
####################################

if __name__ == '__main__':
    
    p = Process(target=getMail)
    p.start()
    
    
    
    #p.join()