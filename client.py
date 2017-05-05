import pickle
from socket import *

'''
    This is the client side. Everything the client does is inside this class named clientTcp().
    Its pretty easy to understand once you break it up. I have split most of the program up into functions.
    def readMsg() is a function for reading messages from the server and writeMsg() is a similar function that 
    handles writing messages to the server. 
'''
class clientTcp():

    def __init__(self):
        self.host = ''
        self.port = 5001
        self.soc = socket(family=AF_INET, type=SOCK_STREAM)

        self.authorised = False
        self.credentials = []

    def start(self):

        try:
            self.soc.connect((self.host, self.port))
        except error as e:  # socket.error has been raised. Is the server running?
            print("Error connecting to the server: %s" % str(e))
        else:
            for i in range(3):
                self.authenticate()
            self.chat()

    def chat(self):
        while True:
            msg = input("say something: ")

            if msg in ['q', 'quit', 'exit']:
                self.writeMsg(msg)
                break

            self.writeMsg(msg)
            msg = self.readMsg()
            print(msg)

        self.soc.close()

    def authenticate(self):
        switch = False
        #   Get the users username and password
        username = input("Username: ")
        password = input("Password: ")

        #   Store it in a tuple
        attempt = [username, password]
        print(str(type(attempt)))
        print(attempt)
        #   Send it over the network to the server
        self.writeMsg(attempt)

        result = self.readMsg()

        if result == 'OK':
            switch = True

        return switch

    def readMsg(self):
        ''' 
        This function looks confusing because of the exceptions 
        Without the exceptions it looks like this:
        
            data = self.soc.recv(1024)
            msg = pickle.loads(data)
            return msg
        
        pickle comes with the standard library. It is used to 
        serialize objects so they can be sent over the network.
        Similar to how we encoded an decoded the text to utf-8,
        we now serialize and deserialize the object.
        '''
        try:
            data = self.soc.recv(1024)
            try:
                msg = pickle.loads(data)
            except:
                print("error pickling data")
            else:
                return msg
        except error as e:
            print("ERROR: %s" % str(e))

    def writeMsg(self, msg: object):
        try:
            data = pickle.dumps(msg)
            try:
                self.soc.send(data)
            except error: # socket.error raised
                print("error sending data")
        except pickle.PicklingError:
            print("error serializing the object...")
        except:
            print("unknown error serializing...")

client = clientTcp()
client.start()