#!/usr/bin/env python
import tidy, sys, pycurl, cStringIO
from Ft.Xml.Domlette import NonvalidatingReader
from Ft.Xml.XPath.Context import Context
from Ft.Xml.XPath import Compile, Evaluate

XHTML_NS = "http://www.w3.org/1999/xhtml"

# TODO config
HEADERS = ['User-agent: Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)', 'Accept-Language: en-us,en;q=0.5']
COOKIEFILE = '/home/stef/.config/munchr/cookies.lwp'
VERSION="v0.2"

def normalize(raw,debug=None):
   # tidy to xhtml
   if debug: print >> sys.stderr, 'cleaning response'   
   options = dict(output_xhtml=1, add_xml_decl=0, indent=0, tidy_mark=0, doctype="strict", wrap=0)
   return str(tidy.parseString(raw, **options))

def send(params, debug=None):
   if debug: print >> sys.stderr, 'setting up http connection to', url
   c = pycurl.Curl()
   b = cStringIO.StringIO()
   c.setopt(pycurl.URL, params['action'])
   c.setopt(pycurl.HTTPHEADER, HEADERS)
   c.setopt(pycurl.WRITEFUNCTION, b.write)
   if(params.has_key('postfields') and len(params['postfields'])>0):
      postparams=[]
      for field in params['postfields'].items(): postparams.append(field)
      c.setopt(pycurl.HTTPPOST, postparams)
   c.setopt(pycurl.FOLLOWLOCATION, 1)
   c.setopt(pycurl.SSL_VERIFYPEER, 0)
   c.setopt(pycurl.MAXREDIRS, 5)
   c.setopt(pycurl.COOKIEFILE, COOKIEFILE)
   c.setopt(pycurl.COOKIEJAR, COOKIEFILE)
   c.perform()
   c.close
   res=b.getvalue()
   b.close
   return normalize(res)

def fetch(params, debug=None):
   if(not params.has_key('resultxpath')):
      return None

   xhtml=send(params)
   if debug: print >> sys.stderr, 'checking results'   
   # make it a 4suite document
   doc = NonvalidatingReader.parseString(xhtml,params['action'])
   context = Context(doc, processorNss={"h": XHTML_NS})
   #Compute the XPath against the context
   results=Compile(params['resultxpath']).evaluate(context)
   if debug: print >> sys.stderr, 'done', params['action']
   return (results, xhtml)

if(__name__=="__main__"):
   pass
