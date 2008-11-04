#!/usr/bin/env python
#     Copyright (C) 2008  Stefan Marsiske
# 
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
import tidy, sys, pycurl, cStringIO
from Ft.Xml.Domlette import NonvalidatingReader
from Ft.Xml.XPath.Context import Context
from Ft.Xml.XPath import Compile
from Ft.Xml.Domlette import PrettyPrint
from urlparse import urlsplit, urlunsplit

XHTML_NS = "http://www.w3.org/1999/xhtml"

# TODO config
HEADERS = ['User-agent: Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)', 'Accept-Language: en-us,en;q=0.5']
COOKIEFILE = '/home/stef/.config/munchr/cookies.lwp'
VERSION="v0.2"

urlquoted = dict((chr(i), '%%%02X' % i) for i in range(256))
urlquoted.update(dict((c, c) for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' +
                                      'abcdefghijklmnopqrstuvwxyz' +
                                      '0123456789._-'))
def urlquote(text):
    return ''.join(map(urlquoted.get, text))
    
def urlencode(params):
    pairs = ['%s=%s' % (urlquote(key), urlquote(value).replace('%20', '+'))
             for key, value in params.items()]
    return '&'.join(pairs)

def normalize(raw,debug=None):
   # tidy to xhtml
   if debug: print >> sys.stderr, 'cleaning response'   
   options = dict(output_xhtml=1, add_xml_decl=0, indent=0, tidy_mark=0, doctype="strict", wrap=0)
   return str(tidy.parseString(raw, **options))

def send(params, debug=None, nopost=None):
   if debug: print >> sys.stderr, 'setting up http connection to', params['action']
   c = pycurl.Curl()
   b = cStringIO.StringIO()
   c.setopt(pycurl.URL, params['action'])
   c.setopt(pycurl.HTTPHEADER, HEADERS)
   c.setopt(pycurl.WRITEFUNCTION, b.write)
   if(params.has_key('postfields') and len(params['postfields'])>0):
      if(nopost):
         newquery=urlencode(params['postfields'])
         scheme, host, path, query, fragment = urlsplit(params['action'])
         uo=urlunsplit((scheme, host, path, "&".join((newquery,query)), fragment))
         c.setopt(pycurl.URL, uo)
      else:
         c.setopt(pycurl.HTTPPOST, params['postfields'].items())
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

def fetch(params, debug=None,nopost=None):
   if(not params.has_key('resultxpath')):
      return None

   xhtml=send(params,debug,nopost)
   if debug: print >> sys.stderr, 'checking results'   
   # make it a 4suite document
   doc = NonvalidatingReader.parseString(xhtml,params['action'])
   context = Context(doc, processorNss={"h": XHTML_NS})
   #Compute the XPath against the context
   results=Compile(params['resultxpath'])
   results=results.evaluate(context)
   res=[]
   for a in results:
      tf = cStringIO.StringIO()
      PrettyPrint(a,tf)
      t=tf.getvalue()
      res.append(t)
      tf.close()
   results=res
   if debug: print >> sys.stderr, 'done', params['action']
   return (results, xhtml)

if(__name__=="__main__"):
   pass
