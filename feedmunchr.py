#!/usr/bin/python

import feedparser, os, hashlib, pickle, cStringIO, urllib2, magic, subprocess

# initialize file magic
ms = magic.open(magic.MAGIC_NONE)
ms.load()

# For example, to ask for the roaming 'Application Data' directory:
# (CSIDL_APPDATA asks for the roaming, CSIDL_LOCAL_APPDATA for the local one)
# (See microsoft references for further CSIDL constants)
try:
   from win32com.shell import shellcon, shell
   homedir = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0)
except ImportError: # quick semi-nasty fallback for non-windows/win32com case
   homedir = os.path.expanduser("~")

STORAGE="/home/stef/.config/munchr/rsscache/"
DZENPIPE="/home/stef/.config/munchr/notifications"
FEEDLIST=homedir+'/.feedmunchr'

def hash(data):
   return hashlib.sha1(data).hexdigest()

def getfeedimage(url):
   # get feed icon
   f=urllib2.urlopen(url)
   image=f.read()
   f.close()

   # detect icon image format
   type=ms.buffer(image).split(" ")[0].lower()
   #print type

   # convert image to xpm
   convert=subprocess.Popen("convert -resize 12 "+type+":- xpm:-",shell=True,stdin=subprocess.PIPE, stdout=subprocess.PIPE)
   xpm,err=convert.communicate(image)
   return xpm


class DzenOutput:
   def __init__(self,dzenpipe=DZENPIPE):
      self.__dict__['lines']=[]
      self.__dict__['pipe']=dzenpipe

   def push(self,data,feed):
      self.__dict__['lines'].append(str(self.fetchicon(feed))+data.title)

   def fetchicon(self,feed):
      if(not feed.has_key('image')):
         return ""
      key=(feed.link,feed.image.href)
      if(not storage.query(key)):
         storage.store(key,getfeedimage(feed.image.href))
      return "^i("+storage.query(key)+") "

   def flush(self):
      dzen=open(self.__dict__['pipe'],'a+')
      if(len(self.__dict__['lines'])):
         self.__dict__['lines'].reverse()
         # write dzen title bar
         dzen.write("^tw()^fg(red)["+str(len(self.__dict__['lines']))+"]^fg() "+self.__dict__['lines'][-1].encode('utf8')+'\n'+'\n'.join(self.__dict__['lines']).encode('utf8'))
      else:
         dzen.write("^tw()\n")
      dzen.close()

class Storage:
   def __init__(self,path=STORAGE):
      if not os.path.isdir(path):
         #print "mkdir", path
         os.mkdir(path)
      self.__dict__['path']=path
      self.__dict__['index']={}

   def store(self,labels,data):
      # default cache basedir
      path=self.__dict__['path']

      # changed item?
      changed=None

      # store pickled item in string
      itemstr = cStringIO.StringIO()
      pickle.dump(data,itemstr)
      itemraw=itemstr.getvalue()
      itemstr.close()

      # calculate item name from pickled itemd
      itemname=path+hash(itemraw.encode('string_escape'))

      # update index
      self.__dict__['index'][labels]=itemname

      if not os.path.isfile(itemname): 
         changed=1
         #print "write",labels,itemname

         # write pickled item to file
         item=open(itemname, 'w+')
         item.write(itemraw.encode('string_escape'))
         item.close()
      return changed

   def query(self,labels):
      if(not self.__dict__['index'].has_key(labels)):
         return
      itemfname=self.__dict__['index'][labels]
      if not os.path.isfile(itemfname): 
         return

      # read pickled item from file
      item=open(itemfname, 'r')
      itemstr = cStringIO.StringIO()
      itemstr.write(item.read().decode('string_escape'))
      item.close()
      itemstr.seek(0)
      return pickle.load(itemstr)

   def query(self,labels):
      if(self.__dict__['index'].has_key(labels) and
            os.path.isfile(self.__dict__['index'][labels])):
         return self.__dict__['index'][labels]

   def get(self,labels):
      itemfname=self.query(labels)

      # read pickled item from file
      item=open(itemfname, 'r')
      itemstr = cStringIO.StringIO()
      itemstr.write(item.read().decode('string_escape'))
      item.close()
      itemstr.seek(0)
      return pickle.load(itemstr)

##### MAIN #####

storage=Storage()
output=DzenOutput()
f=open(FEEDLIST, 'r')
for url in f:
   # get next feed
   feed=feedparser.parse(url)
   # store feed info
   storage.store((feed.feed.link),feed.feed)
   # process entries
   for entry in feed.entries:
      if (storage.store((feed.feed.link,entry.title),entry)):
         # do something with this new entry
         output.push(entry,feed.feed)

# tidy up
f.close()
output.flush()
ms.close()