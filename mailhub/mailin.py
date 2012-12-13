import ConfigParser
import getpass, poplib



def logging():
    import logging

    c = Config()

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



            for name, value in self.parser.items(section_name):
                if debug:
                    print '  %s = %s' % (name, value)
                if name == 'schema':
                    vschema = value.replace(' ', '').split(',')
                    for i in range(len(vschema)):
                        if len(vschema[i]) == 0:
                            vschema[i] = 'field%i'%i
                    value = ','.join(vschema)
                    getattr(self, section_name)[name] = value.strip()

                    # Validate the schema if schema
                    dtype = getattr(self, section_name)['datatypes'].split(',')
                    dtypelen = len(dtype)
                    sch = getattr(self, section_name)['schema'].split(',')
                    schlen = len(sch)

                    if dtypelen <> schlen:
                        print """\nschema definition error in %s
                        \nThere are %i fields in the schema. and %i datatypes defined.
                        \nThere needs to be the same number"""%(section_name, schlen, dtypelen)
                        for x in range(max([dtypelen,schlen])):
                            try:
                                print sch[x], dtype[x]
                            except IndexError:
                                if dtypelen > schlen:
                                    print 'missing  ' + dtype[x]
                                else:
                                    print 'missing'

                        raise SystemExit                    


                if name == 'enabled' and type(value) <> bool:
                    getattr(self, section_name)[name] = ast.literal_eval(value)


            #if getattr(self, section_name).has_key('enabled'):
                #if type(getattr(self, section_name)['enabled']) <> bool:
                    #getattr(self, section_name)['enabled'] = ast.literal_eval(getattr(self, section_name)['enabled'])

            #for name, value in self.parser.items(section_name):
                #if name == 'schema':










Mailbox = poplib.POP3('mail.o2.co.uk', '110') 
Mailbox.user(user) 
Mailbox.pass_(password) 
numMessages = len(Mailbox.list()[1])

class omail(object):
    def __init__(self):
        self.headers = ('Return-Path', 'Received', 'DKIM-Signature', 'MIME-Version', 'Reply-To', 'Date', 
                       'Message-ID', 'Subject', 'From', 'To', 'Content-Type')        
        for x in self.headers:
            setattr(self, x, '')
            
            
for i in range(numMessages):
    
    msg = Mailbox.top(i+1, 10000)
    dmess = {}
    
    #headers = ( 'Subject', 'Content-Type')
    
    omsg = omail()
    htype = ''
    for x in msg[1]:
        if x.split(':')[0] in omsg.headers:
            htype = x.split(':')[0]
            setattr(omsg, htype, "%s\n%s"%(getattr(omsg,htype), x.split(':')[1:][0]))
        else:
            setattr(omsg, htype, "%s\n%s"%(getattr(omsg,htype), x))
            
            
    for k in omsg.headers:
        print k, getattr(omsg, k)
        
        
        #print 'xx',x
        
    
    # write message -> object function
    # parse object -> exteact info.
    # store message
    # parse/import message
    
    



Mailbox.quit()