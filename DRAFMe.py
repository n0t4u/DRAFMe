#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Author: n0t4u
#Version: 1.0.0

#TODO
#Avoid directories to be crawled

#Imports
from bs4 import BeautifulSoup
#https://docs.python.org/3/library/argparse.html
import argparse
import logging
import pycurl
import sys
import os
import random
import re
from termcolor import colored
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO
from urllib.parse import urlparse
import urllib.request
import time
#from concurrent.futures import ThreadPoolExecutor
import threading
#https://docs.python.org/3.7/library/mmap.html
import mmap
import xml.etree.ElementTree as ET

#Variables and classes

dictionary= []

userAgents = [
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:74.0) Gecko/20100101 Firefox/74.0",
	"Mozilla/5.0 (Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0",
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
	"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36 OPR/67.0.3575.115",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36 OPR/67.0.3575.115",
	"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36 OPR/67.0.3575.115",
	"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36 Vivaldi/2.11",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36 Vivaldi/2.11",
	"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36 Vivaldi/2.11"
	#Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko
	#Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43
]
userAgent = userAgents[random.randint(0,len(userAgents)-1)]

cookies = "cookies.txt"
crawlRoot=""

class Spider(object):
	def __init__(self):
		self.lock= threading.Lock()
		self.toCrawl= []
		self.routes = []
		self.documents = []
		self.css =[]
		self.javascript =[]
		self.sources = []
		self.forms = []
		self.phones = []
		self.mails = []
		self.total = 0
	def getRoute(self,route):
		self.toCrawl
		self.lock.acquire()
		try:
			nextRoute= self.toCrawl.pop(self.toCrawl.index(route))
		except:
			nextRoute=""
		finally:
			self.lock.release()
			return nextRoute
	def newRoute(self,newRoute):
		self.routes
		self.lock.acquire()
		try:
			if newRoute not in self.routes:
				self.routes.append(newRoute)
		except Exception as e:
			#raise e
			pass
		finally:
			self.lock.release()
	def newRouteToCrawl(self,newRoute):
		self.routes
		self.lock.acquire()
		try:
			if newRoute not in self.routes:
				self.routes.append(newRoute)
				#if re.search(crawlRoot,newRoute):
				print(newRoute)
				if re.match(crawlRoot,newRoute):
					self.toCrawl.append(newRoute)
		except Exception as e:
			#raise e
			pass
		finally:
			self.lock.release()
	def newDocument(self,newRoute):
		self.documents
		self.lock.acquire()
		try:
			if newRoute not in self.documents:
				self.documents.append(newRoute)
		except Exception as e:
			#raise e
			pass
		finally:
			self.lock.release()
	def newCSS(self,newRoute):
		self.css
		self.lock.acquire()
		try:
			if newRoute not in self.css:
				self.css.append(newRoute)
		except Exception as e:
			#raise e
			pass
		finally:
			self.lock.release()
	def newJavaScript(self,newRoute,url):
		self.javascript
		self.lock.acquire()
		try:
			if newRoute not in self.javascript:
				self.javascript.append(newRoute)
				if re.search(url,newRoute):
					self.toCrawl.append(newRoute)
		except Exception as e:
			#raise e
			pass
		finally:
			self.lock.release()
	def newSource(self,newRoute):
		self.sources
		self.lock.acquire()
		try:
			if newRoute not in self.sources:
				self.sources.append(newRoute)
		except Exception as e:
			#raise e
			pass
		finally:
			self.lock.release()			
	def newPhone(self,phone):
		self.phones
		self.lock.acquire()
		try:
			if phone not in self.phones:
				self.phones.append(phone)
		except Exception as e:
			#raise e
			pass
		finally:
			self.lock.release()
	def newMail(self,mail):
		self.mails
		self.lock.acquire()
		try:
			if mail not in self.mails:
				self.mails.append(mail)
		except Exception as e:
			#raise e
			pass
		finally:
			self.lock.release()
	def newForm(self,form):
		self.forms
		self.lock.acquire()
		try:
			if form not in self.forms:
				self.forms.append(form)
		except Exception as e:
			#raise e
			pass
		finally:
			self.lock.release()
	def printRoutes(self):
		#print("\n")
		self.routes.sort()
		print(colored("[*]","yellow"),"Discovered %d differents routes" %self.getTotal())
		for route in range(len(self.routes)):
			print(colored("["+str(route+1)+"]","green").ljust(14," "),self.routes[route])
		print(colored("--------------------------------------------------","blue"))
	def printMisc(self):
		#print("\n")
		self.documents.sort()
		self.css.sort()
		self.javascript.sort()
		self.sources.sort()
		self.forms.sort()
		self.mails.sort()
		self.phones.sort()
		n=1
		print(colored("[*]","yellow"),"Discovered %d routes with documents (PDF, docs, excel,...)." %len(self.documents))
		for doc in self.documents:
			print(colored("["+str(n)+"]","green").ljust(14," "),doc)
			n +=1
		print(colored("--------------------------------------------------","blue"))
		n=1
		print(colored("[*]","yellow"),"Discovered %d routes with style sheets (CSS)." %len(self.css))
		for link in self.css:
			print(colored("["+str(n)+"]","green").ljust(14," "),link)
			n +=1
		print(colored("--------------------------------------------------","blue"))
		n=1
		print(colored("[*]","yellow"),"Discovered %d routes with JavaScript libraries." %len(self.javascript))
		for script in self.javascript:
			print(colored("["+str(n)+"]","green").ljust(14," "),script)
			n +=1
		print(colored("--------------------------------------------------","blue"))
		n=1
		print(colored("[*]","yellow"),"Discovered %d routes with resources (images)." %len(self.sources))
		for source in self.sources:
			print(colored("["+str(n)+"]","green").ljust(14," "),source)
			n +=1
		print(colored("--------------------------------------------------","blue"))
		n=1
		print(colored("[*]","yellow"),"Discovered %d routes with forms" %len(self.forms))
		for form in self.forms:
			print(colored("["+str(n)+"]","green").ljust(14," "),form)
			n +=1
		print(colored("[!] Fuzzing forms is NOT done to avoid problems.","red"))
		print(colored("--------------------------------------------------","blue"))
		n=1
		print(colored("[*]","yellow"),"Discovered %d routes with mails." %len(self.mails))
		for mail in self.mails:
			print(colored("["+str(n)+"]","green").ljust(14," "),mail)
			n +=1
		print(colored("--------------------------------------------------","blue"))
		n=1
		print(colored("[*]","yellow"),"Discovered %d routes with phone numbers" %len(self.phones))
		for phone in self.phones:
			print(colored("["+str(n)+"]","green").ljust(14," "),phone)
			n +=1
		print(colored("--------------------------------------------------","blue"))

	def getTotal(self):
		self.lock.acquire()
		self.total= len(self.routes)
		self.lock.release()
		return self.total

#Functions
def header():
	print("""
	 ______  _____          ______ __  __       
	|____  \|  __ \   /\   |  ____|  \/  |      
	 _   |  | |__) | /  \  | |__  | \  / | ___  
	|_|  |  |  _  / / /\ \ |  __| | |\/| |/ _ \ 
	 ____|  | | \ \/ ____ \| |    | |  | |  __/ 
	|______/|_|  \/_/    \_\_|    |_|  | |\___| 
	                                  | |      
	                    This is n0t4u |_|      
	

	Pages, Don't Run Away From Me, I will find you all!!!\n""")

def curlRequest(url):
	try:	
		buffer= BytesIO()
		c= pycurl.Curl()
		c.setopt(c.URL, url)
		c.setopt(c.FOLLOWLOCATION, True)
		c.setopt(pycurl.MAXREDIRS, 5)
		c.setopt(pycurl.SSL_VERIFYPEER,0)
		c.setopt(pycurl.SSL_VERIFYHOST, False)
		c.setopt(c.WRITEFUNCTION,buffer.write)
		c.setopt(pycurl.USERAGENT,userAgent) #Change if more UserAgents are added
		c.setopt(pycurl.COOKIEJAR, cookies)
		c.setopt(pycurl.COOKIEFILE, cookies)
		c.perform()
		c.close()
		
		body= buffer.getvalue()
		return body.decode('iso-8859-1')
	except Exception as e:
		if e.args[0]==6:
			print(colored("Unable to connect with the specified domain.\nCheck is URL is correctly written.\n[NOTE] It is possible that a network security system is blocking the requests (Firewall/IPS)\n","red")+ colored("[ERROR] %s","yellow") % e.args[1])
			sys.exit(0)
		else:
			#raise e
			return False

def curlLoginRequest(url,credentials,csrf):
	info.logging("cURL login request")
	try:	
		buffer= BytesIO()
		c= pycurl.Curl()
		c.setopt(c.URL, url)
		c.setopt(c.FOLLOWLOCATION, True)
		c.setopt(pycurl.MAXREDIRS, 5)
		c.setopt(pycurl.SSL_VERIFYPEER,0)
		c.setopt(c.WRITEFUNCTION,buffer.write)
		c.setopt(pycurl.USERAGENT,userAgent) #Change if more UserAgents are added
		c.setopt(pycurl.COOKIEJAR, cookies)
		c.setopt(pycurl.COOKIEFILE, cookies)
		c.setopt(pycurl.POST, True)
		if csrf != None:
			credentials = credentials.replace("$",csrf)
			print(colored(credentials,"yellow"))
		c.setopt(pycurl.POSTFIELDS, credentials)
		c.perform()
		c.close()
		
		body= buffer.getvalue()
		f = open("cookie.txt","r")
		print(body.decode('iso-8859-1'))
		return body.decode('iso-8859-1')
	except Exception as e:
		if e.args[0]==6:
			print(colored("Unable to connect with the specified domain.\nCheck is URL is correctly written.\n[NOTE] It is possible that a network security system is blocking the requests (Firewall/IPS)\n","red")+ colored("[ERROR] %s","yellow") % e.args[1])
			sys.exit(0)
		else:
			#raise e
			return False

def checkCSRF(html):
	soup=BeautifulSoup(html,'html.parser')
	for hiddenInput in soup.find_all("input", type="hidden"):
		print(hiddenInput)
		if re.search(r'(token|login|csrf)',str(hiddenInput)):
			print(colored(hiddenInput.get("value"),"red"))
			return hiddenInput.get("value")

def getURLs(html,url):
	robots()
	try:
		soup=BeautifulSoup(html,'html.parser')
	except:
		pass
	else:
		for link in soup.find_all("a"):
			newRoute= link.get("href")
			if newRoute and len(newRoute) >1:
				if re.search(r'[#?]',newRoute):
					newRoute= re.split(r'[#?]',newRoute)[0]
				elif re.search(r'javascript:',newRoute):
					if re.search(r'javascript:(next|window\.open)\([\"\']{1}',newRoute):
						newRoute = re.split(r'javascript:(next|window\.open)\([\"\']{1}',newRoute)[1]
					else:
						continue
				elif re.search(r'mailto:',newRoute):
					newRoute,mail = re.split(r'mailto:',newRoute,1)
					spider.newMail(mail)
				elif re.search(r'tel:',newRoute):
					newRoute,phone=re.split(r'tel:',newRoute,1)
					spider.newPhone(phone)
				elif re.search(r'[\.\/]{1}$',newRoute):
					if re.search(r'[\.\/]{2}$',newRoute):
						newRoute = newRoute[:-2]
					else:	
						newRoute = newRoute[:-1]
				if not re.search(r'http[s]?\:\/\/',newRoute):
					newRoute= url+"/"+newRoute.lstrip("/")
				newRoute = newRoute.replace(" ","%20")
				if re.search(r'\.(pdf|doc[x]?)$',newRoute,re.IGNORECASE):
					spider.newDocument(newRoute)
				else:
					spider.newRoute(newRoute)
		if args.all:
			getMisc(soup,url)
			getForms(soup)

def getURLsRecursive(html,url):
	try:
		soup=BeautifulSoup(html,'html.parser')
	except:
		pass
	else:
		for link in soup.find_all("a"):
			newRoute= link.get("href")
			if newRoute and len(newRoute) >1:
				if re.search(r'[#?]',newRoute):
					newRoute= re.split(r'[#?]',newRoute)[0]
				elif re.search(r'javascript:',newRoute):
					if re.search(r'javascript:(next|window\.open)\([\"\']{1}',newRoute):
						newRoute = re.split(r'javascript:(next|window\.open)\([\"\']{1}',newRoute)[1]
					else:
						continue
				elif re.search(r'mailto:',newRoute):
					newRoute,mail = re.split(r'mailto:',newRoute,1)
					spider.newMail(mail)
				elif re.search(r'tel:',newRoute):
					newRoute,phone=re.split(r'tel:',newRoute,1)
					phone= phone.replace(" ","")
					spider.newPhone(phone)
				elif re.search(r'[\.\/]{1}$',newRoute):
					if re.search(r'[\.\/]{2}$',newRoute):
						newRoute = newRoute[:-2]
					else:	
						newRoute = newRoute[:-1]
				if not re.search(r'http[s]?\:\/\/',newRoute):
					newRoute= url+"/"+newRoute.strip("/")
				newRoute = newRoute.replace(" ","%20")
				if re.search(r'\.(pdf|doc[x]?|odt|xls[x]?|sxc|txt|rft)$',newRoute,re.IGNORECASE):
					spider.newDocument(newRoute)
				else:
					spider.newRouteToCrawl(newRoute)
		if args.all:
			getMisc(soup,url)
			getForms(soup)

def robots():
	print(colored("[»] Checking robots.txt...","green"))
	robotsUrl = rootDomain.scheme+"://"+rootDomain.netloc.rstrip("/")+"/robots.txt"
	robots = curlRequest(robotsUrl)
	if robots and args.recursive:
		for route in re.findall(r"(?:A|Disa)+llow:\s+\S*",robots,re.X):
			if not re.search(r"[\*\$]+",route):
				logging.debug(route)
				try:
					spider.newRouteToCrawl(rootDomain.scheme+"://"+rootDomain.netloc.rstrip("/")+re.split(r':\s+',route,maxsplit=1)[1].rstrip("/"))
				except Exception as e:
					logging.debug(e)
	elif robots:
		for route in re.findall(r"(?:A|Disa)+llow:\s+\S*",robots,re.X):
			if not re.search(r"[\*\$]+",route):
				logging.debug(route)
				try:
					spider.newRoute(rootDomain.scheme+"://"+rootDomain.netloc.rstrip("/")+re.split(r':\s+',route,maxsplit=1)[1].rstrip("/"))
				except Exception as e:
					logging.debug("[Exception]",e)
	else:
		logging.info("[!] No robots detected")
	return

def sitemap():
	print(colored("[»] Checking sitemap.xml...","green"))
	sitemapUrl = rootDomain.scheme+"://"+rootDomain.netloc.rstrip("/")+"/sitemap.xml"
	logging.info("[*] "+sitemapUrl)
	req = urllib.request.Request(sitemapUrl,headers={'User-Agent':userAgent})
	response = urllib.request.urlopen(req)
	soup = BeautifulSoup(response,"lxml")
	if sitemap and args.recursive:
		for route in soup.find_all("loc"):
			r1 = re.sub(r"^[\s]+","",route.text)
			r2 = re.sub(r"[\s]+$","",r1)
			spider.newRouteToCrawl(r2)
	elif sitemap:
		for route in soup.find_all("loc"):
			r1 = re.sub(r"^[\s]+","",route.text)
			r2 = re.sub(r"[\s]+$","",r1)
			print(r2)
			spider.newRoute(r2)
	else:
		logging.info("[!] No sitemap detected.")
	return

def getMisc(soup,url):
	for link in soup.find_all("link"):
		newRoute=link.get("href")
		if newRoute and re.search(r'\.(css|jsp)',newRoute):
			if re.search(r'[#?]',newRoute):
				#Removes the parameters "#?" from the path and recover the path below
				route,att= re.split(r'[#?]',newRoute,maxsplit=1)
				if att and len(re.split('/',att,maxsplit=1)) ==2 :
					newRoute = route+"/"+re.split(r'/',aux,maxsplit=1)[1]
			if not re.search(r'http[s]?\:\/\/',newRoute):
				newRoute= url+"/"+newRoute.lstrip("/")
			newRoute = newRoute.replace(" ","%20")
			spider.newCSS(newRoute)
		elif newRoute and re.search(r'\.ico',newRoute):
			if not re.search(r'http[s]?\:\/\/',newRoute):
				newRoute= url+"/"+newRoute.lstrip("/")
			newRoute = newRoute.replace(" ","%20")
			spider.newSource(newRoute)

	for link in soup.find_all("script"):
		if link.get("rel") == "canonical":
			continue
		newRoute=link.get("src")
		if newRoute:
			if re.search(r'[#?]',newRoute):
				newRoute,aux= re.split(r'[#?]',newRoute,maxsplit=1)
				if aux and len(re.split('/',aux,maxsplit=1)) ==2 :
					newRoute = newRoute+"/"+re.split(r'/',aux,1)[1]
			if not re.search(r'http[s]?\:\/\/',newRoute):
				newRoute = url+"/"+newRoute.lstrip("/")
			newRoute = newRoute.replace(" ","%20")
			spider.newJavaScript(newRoute,url)
	for link in soup.find_all("img"):
		newRoute=link.get("src")
		if newRoute:
			if re.search(r'base(64|32)',newRoute):
				return
			elif re.search(r'[#?]',newRoute):
				newRoute,aux= re.split(r'[#?]',newRoute,maxsplit=1)
				try:
					newRoute = newRoute+"/"+re.split(r'/',aux,1)[1]
				except:
					continue
			if not re.search(r'http[s]?\:\/\/',newRoute):
				newRoute= url+"/"+newRoute.lstrip("/")
			newRoute = newRoute.replace(" ","%20")
			spider.newSource(newRoute)

def getForms(soup):
	for form in soup.find_all("form"):
		newForm= form.get("action")
		if newForm and newForm != "#":
			spider.newForm(newForm.lstrip("."))

def recursiveCrawl(spider,url):
	for i in range(args.recursive):
		for route in spider.toCrawl:
			nextRoute= spider.getRoute(route)
			html= curlRequest(nextRoute)
			time.sleep(args.sleep[0]/1000)
			if html:
				logging.debug("%d\tThread %s %s" %(len(spider.toCrawl),threading.currentThread().getName(),route))
				logging.info(" %d routes left \t%s" %(len(spider.toCrawl),route))
				getURLsRecursive(html,url)

def generateDictionary():
	globalList = spider.routes +spider.documents+spider.css +spider.javascript +spider.sources
	for route in globalList:
		directories = route.lstrip("https://").lstrip("http://").split("/")
		directories.pop(0)
		for d in directories:
			if not d in dictionary and not re.search(r'.(pdf|doc[x]?|htm[l]?|asp[x]?|php|jp[e]?g|png|svg|js|css|ico|jsp)$',d):
				dictionary.append(d)
	dictionary.sort()


#Main
parser= argparse.ArgumentParser(description=header())

parser.add_argument("url",help="URL to crawl.",nargs=1)
parser.add_argument("-r","--recursive",dest="recursive",help="Recursive crawling. Number of depth crawl.",type=int,choices=range(1,6), default=0)
parser.add_argument("-s","--sleep",dest="sleep",help="Sleeping time , in miliseconds, between requests.",type=int,nargs=1, default=[0])
parser.add_argument("-t","--threads",dest="threads",help="Number of threads. 4 by default.",type=int,nargs=1,default=[4])
parser.add_argument("-v","--verbose",dest="verbose", help="Verbose mode.", action="store_true")
parser.add_argument("-o","--output",dest="output",help="Output file.", nargs = 1)
parser.add_argument("-U","--userAgent",dest="userAgent", help="User Agent for cURL requests. Random by default.",nargs=1)
parser.add_argument("-R","--root",dest="root", help="Root path for all the requests \n Example: www/ o /", nargs=1)
sessiongroup= parser.add_mutually_exclusive_group()
sessiongroup.add_argument("-l","--login",dest="login",help="Login credentials. Use $ for CSRF token. (EXPERIMENTAL)\n Example: \"username=n0t4u&pwd=n0t4u&csrf_token=$\"", nargs=1, default=[0])
sessiongroup.add_argument("-c","--cookie",dest="cookie", help="Session cookie", nargs=1)
sessiongroup.add_argument("-cf","--cookie-file",dest="cookieFile", help="Session cookies file",nargs=1)

urlsgroup= parser.add_mutually_exclusive_group()
urlsgroup.add_argument("-u","--urls",dest="urls",help="Print routes at the end of the rawling",action="store_true")
urlsgroup.add_argument("-a","--all",dest="all",help="Print routes  and resources at the end of the crawling.",action="store_true")

dictgroup = parser.add_mutually_exclusive_group()
dictgroup.add_argument("-d","--dictionary",dest="dictionary", help="Generates a dictionary with all the paths detected and print them.", action="store_true")
dictgroup.add_argument("-do","--dOutput",dest="dOutput", help="Generates a dictionary with all the paths detected and store them in an output file.", nargs=1)
parser.add_argument("--check",dest="check", help="Check if dictionary paths are in the output file specified and write only new ones.", action="store_true")

args = parser.parse_args()

if __name__ == '__main__':
	
	#header()
	startTime = time.time()
	if args.verbose:
		logging.basicConfig(level=logging.INFO)
	spider = Spider()
	spider.newRoute(args.url[0])
	rootDomain= urlparse(args.url[0])
	crawlRoot = rootDomain.netloc+rootDomain.path.rstrip("/")
	if not rootDomain.scheme:
		sys.exit(colored("FQDN must be give. https://n0t4u.com","red"))
	print(colored("[»] Starting crawling...","green"))
	if args.userAgent:
		userAgent = args.userAgent[0]
	else:
		userAgent = userAgents[random.randint(0,len(userAgents)-1)]

	if args.login[0]:
		getResponse=curlRequest(args.url[0])
		csrf= checkCSRF(getResponse)
		html=curlLoginRequest(args.url[0],args.login[0],csrf)
	else:
		if args.cookie:
			with open(cookies,"w+",encoding="iso-8859-1") as file:
				file.write(args.cookie[0]) 
			file.close()
		elif args.cookieFile:
			cookies = args.cookieFile[0]
		html= curlRequest(args.url[0])

	if args.root:
		if args.root[0] == "/":
			url = rootDomain.scheme+"://"+rootDomain.netloc
		else:
			url= rootDomain.scheme+"://"+rootDomain.netloc+"/"+args.root[0].strip("/")
	elif rootDomain[2]:
		url = rootDomain.scheme+"://"+rootDomain.netloc+"/"+rootDomain.path.strip("/")
	else:
		url = rootDomain.scheme+"://"+rootDomain.netloc.rstrip("/")

	robots()
	sitemap()

	if args.recursive:
		getURLsRecursive(html,url)
		try:
			threads=[]
			for i in range(args.threads[0]):
				thread= threading.Thread(target=recursiveCrawl,args=(spider,url),name=i,daemon=True)
				thread.start()
				threads.append(thread)
			for thread in threads:
				thread.join()
		except KeyboardInterrupt:
			#CTRL+C
			print(colored("Crawling canceled...","red"))
			threads.clear()
	else:
		if html:
			getURLs(html,url)
	print(colored("[»] Crawling ended","green"))
	if args.dictionary:
		print(colored("[*] Creating path dictionary...","blue"))
		generateDictionary()
		for word in dictionary:
			print(word)
		print(colored("[*]","blue"),"Discovered %d different paths" % len(dictionary))
	elif args.dOutput:
		print(colored("[*]","blue"),"Creating path dictionary...")
		generateDictionary()
		if args.check:
			try:
				print(colored("[*]","blue"),"Discovered %d different paths" % len(dictionary))
				with open(args.dOutput[0],"a+", encoding="iso-8859-1") as file:
				    s= mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
				    counter =0
				    for word in dictionary:
				    	if s.find(word.encode()) == -1:
				    		file.write(word+"\n")
				    		counter +=1
				    print(colored("%d new paths where written in %s dictionary" %(counter,args.dOutput[0]),"green"))
				file.close()
			except Exception as e:
				if e.args[0]==13:
					sys.exit(args.dOutput[0] +" "+ colored(e.args[1],"red"))
				else:
					print(colored("[ERROR]","red"),"File does not exist.")
		else:
			try:
				f = open(args.dOutput[0],"a+", encoding="iso-8859-1")
			except:
				f = open(args.dOutput[0],"w+", encoding="iso-8859-1")
			finally:
				for word in dictionary:
					f.write(word+"\n")
				f.close()
				print(colored("[»] Dictionary created with %d new paths." % len(dictionary),"green"))
	if args.output:
		logging.info(colored("[*]","blue"),"File %s created" %args.output[0])
		#f = open(args.output[0]+".txt","w", encoding="iso-8859-1") #Cambiar por "a"
		with open(args.output[0],"w", encoding="iso-8859-1") as file:
			globalList = spider.routes +spider.documents +spider.css +spider.javascript +spider.sources
			for route in globalList:
				file.write(route+"\n") #route.enconde("iso-8859-1")
		file.close()
		print(colored("[*]","blue"),"Discovered %d routes." %spider.getTotal())
	if args.urls:
		spider.printRoutes()
	elif args.all:
		spider.printRoutes()
		spider.printMisc()
	try:
		os.remove(cookies)
	except Exception as e:
		pass
	executionTime = time.time()- startTime
	if executionTime/60 > 1:
		print(colored("--- %d secs --- (%d mins) ---" %(round(executionTime,3), round(executionTime/60,3)),"yellow"))
	else:
		print(colored("--- %d secs ---" %round(executionTime,3),"yellow"))

