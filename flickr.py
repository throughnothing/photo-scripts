#hide depracation warnings
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

import sys
import flickrapi
import ConfigParser
import simplejson as json


CONFIG_FILE='flickr.config'

config = ConfigParser.ConfigParser()
#Read configfile
success = config.read(CONFIG_FILE)
if not success:
    print "Error loading " + CONFIG_FILE + " file!"
    sys.exit(0)

api_key=config.get('flickr','api_key')
api_secret=config.get('flickr','api_secret')
my_userid=config.get('flickr','my_userid')
collection=config.get('flickr','collection')

# Authenticate with flickr API
#flickr = flickrapi.FlickrAPI(api_key,api_secret, format='json')
flickr = flickrapi.FlickrAPI(api_key,api_secret)
(token, frob) = flickr.get_token_part_one(perms='write')
if not token: raw_input("Press ENTER after you authorized this program")
flickr.get_token_part_two((token, frob))


class Ls:
    userid=''
    def __init__(self, userid):
        self.userid = userid

    def collections(self):
        cs = flickr.collections_getTree(user_id=self.userid)
        for c in cs.find('collections').findall('collection'):
            print c.attrib['title'] + "(" + c.attrib['id'] + "): " + c.attrib['description']

    def collection(self,collection_id):
        cs = flickr.collections_getTree(user_id=collection_id)
        for c in cs.find('collections').findall('collection'):
            print c.attrib['title'] + "(" + c.attrib['id'] + "): " + c.attrib['description']

    def sets(self,collection_id=""):
        if collection_id != "":
            sets = flickr.collections_getTree(collection_id=collection_id).find('collections').find('collection').findall('set')
            for s in sets:
                print s.attrib['title'] + "(" + s.attrib['id'] + "): " + s.attrib['description']
        else:
            sets = flickr.photosets_getList(user_id=self.userid).find('photosets').findall('photoset')
            for s in sets:
                print s.find('title').text + "(" + str(s.attrib['id']) + ")[" + \
                    str(s.attrib['photos']) + " photos]: " + str(s.find('description').text)


l = Ls(my_userid)
#l.collections()

commands = {
    "ls" : l
}

def run_command(command):
    cparts = command.split(' ')
    if len(cparts) < 2:
        print "Not enough arguments"
        return -1;

    obj = commands[cparts[0]]
    if  obj:
        try:
            f = getattr(obj, cparts[1])
            numArgs = len(cparts[2:])
            if numArgs > 0:
                f(*cparts[2:]) 
            else:
                f()
        except Exception as e:
            print e
    else:
        print "Command not found!"


while True:
    command = raw_input('flickr>')
    if command:
        if command == "quit":
            sys.exit(0)

        run_command(command)



