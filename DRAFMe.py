#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: n0t4u
# Version: 1.2.5

#TODO.
# Check recursive
# Consider import latest-user-agents https://pypi.org/project/latest-user-agents/
# Add external resources links
# Add metrics of analyzed routes --> Graph?

#TODO. Backlog
# Detect JS versions
# Selenium support
# Add proxy support for Windows
# Take a nap zzzZZZ
# Oh yes! Check routes in comments

# Imports
from bs4 import BeautifulSoup
import argparse
from termcolor import colored
import logging
# https://docs.python.org/3.7/library/mmap.html
import mmap
import os
import random
import re
import requests
import sys
import time
import threading
from urllib.parse import urlparse
import urllib3

urllib3.disable_warnings()

# Variables and classes

dictionary = []

userAgents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36 OPR/67.0.3575.115",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36 OPR/67.0.3575.115",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36 OPR/67.0.3575.115",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Vivaldi/5.4.2753.47",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Vivaldi/3.7",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Vivaldi/3.7",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
    # Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33"
]
# userAgent = userAgents[random.randint(0, len(userAgents) - 1)]

cookies = "cookies.txt"
headers = {}
crawlRoot = ""
proxies = None


class Spider(object):
    def __init__(self):
        self.lock = threading.Lock()
        self.toCrawl = []
        self.routes = []
        self.documents = []
        self.css = []
        self.javascript = []
        self.sources = []
        self.forms = []
        self.phones = []
        self.mails = []
        self.total = 0

    def getRoute(self, route):
        # self.toCrawl
        self.lock.acquire()
        try:
            nextRoute = self.toCrawl.pop(self.toCrawl.index(route))
        except:
            nextRoute = ""
        finally:
            self.lock.release()
            return nextRoute

    def newRoute(self, newRoute):
        # self.routes
        self.lock.acquire()
        try:
            if newRoute not in self.routes:
                self.routes.append(newRoute)
        except Exception as e:
            # raise e
            pass
        finally:
            self.lock.release()

    def newRouteToCrawl(self, newRoute):
        # self.routes
        self.lock.acquire()
        try:
            if newRoute not in self.routes:
                self.routes.append(newRoute)
                if re.search(crawlRoot, newRoute) and not re.search(r'logout', newRoute):
                    self.toCrawl.append(newRoute)
        except Exception as e:
            # raise e
            pass
        finally:
            self.lock.release()

    def newDocument(self, newRoute):
        # self.documents
        self.lock.acquire()
        try:
            if newRoute not in self.documents:
                self.documents.append(newRoute)
        except Exception as e:
            # raise e
            pass
        finally:
            self.lock.release()

    def newCSS(self, newRoute):
        # self.css
        self.lock.acquire()
        try:
            if newRoute not in self.css:
                self.css.append(newRoute)
        except Exception as e:
            # raise e
            pass
        finally:
            self.lock.release()

    def newJavaScript(self, newRoute, url):
        # self.javascript
        self.lock.acquire()
        try:
            if newRoute not in self.javascript:
                self.javascript.append(newRoute)
                if re.search(url, newRoute):
                    self.toCrawl.append(newRoute)
        except Exception as e:
            # raise e
            pass
        finally:
            self.lock.release()

    def newSource(self, newRoute):
        # self.sources
        self.lock.acquire()
        try:
            if newRoute not in self.sources:
                self.sources.append(newRoute)
        except Exception as e:
            # raise e
            pass
        finally:
            self.lock.release()

    def newPhone(self, phone):
        # self.phones
        self.lock.acquire()
        try:
            if phone not in self.phones:
                self.phones.append(phone)
        except Exception as e:
            # raise e
            pass
        finally:
            self.lock.release()

    def newMail(self, mail):
        # self.mails
        self.lock.acquire()
        try:
            if mail not in self.mails:
                self.mails.append(mail)
        except Exception as e:
            # raise e
            pass
        finally:
            self.lock.release()

    def newForm(self, form):
        # self.forms
        self.lock.acquire()
        try:
            if form not in self.forms:
                self.forms.append(form)
        except Exception as e:
            # raise e
            pass
        finally:
            self.lock.release()

    def printRoutes(self):
        # print("\n")
        self.routes.sort()
        print(colored("[*]", "yellow"), "Discovered %d different routes" % self.getTotal())
        for route in range(len(self.routes)):
            print(colored("[" + str(route + 1) + "]", "green").ljust(14, " "), self.routes[route])
        print(colored("--------------------------------------------------", "blue"))

    def printMisc(self):
        # print("\n")
        self.documents.sort()
        self.css.sort()
        self.javascript.sort()
        self.sources.sort()
        self.forms.sort()
        self.mails.sort()
        self.phones.sort()
        n = 1
        print(colored("[*]", "yellow"),
              "Discovered %d routes with documents (PDF, docs, excel,...)." % len(self.documents))
        for doc in self.documents:
            print(colored("[" + str(n) + "]", "green").ljust(14, " "), doc)
            n += 1
        print(colored("--------------------------------------------------", "blue"))
        n = 1
        print(colored("[*]", "yellow"), "Discovered %d routes with style sheets (CSS)." % len(self.css))
        for link in self.css:
            print(colored("[" + str(n) + "]", "green").ljust(14, " "), link)
            n += 1
        print(colored("--------------------------------------------------", "blue"))
        n = 1
        print(colored("[*]", "yellow"), "Discovered %d routes with JavaScript libraries." % len(self.javascript))
        for script in self.javascript:
            print(colored("[" + str(n) + "]", "green").ljust(14, " "), script)
            n += 1
        print(colored("--------------------------------------------------", "blue"))
        n = 1
        print(colored("[*]", "yellow"), "Discovered %d routes with resources (images)." % len(self.sources))
        for source in self.sources:
            print(colored("[" + str(n) + "]", "green").ljust(14, " "), source)
            n += 1
        print(colored("--------------------------------------------------", "blue"))
        n = 1
        print(colored("[*]", "yellow"), "Discovered %d routes with forms" % len(self.forms))
        for form in self.forms:
            print(colored("[" + str(n) + "]", "green").ljust(14, " "), form)
            n += 1
        print(colored("[!] Fuzzing forms is NOT done to avoid problems.", "red"))
        print(colored("--------------------------------------------------", "blue"))
        n = 1
        print(colored("[*]", "yellow"), "Discovered %d routes with mails." % len(self.mails))
        for mail in self.mails:
            print(colored("[" + str(n) + "]", "green").ljust(14, " "), mail)
            n += 1
        print(colored("--------------------------------------------------", "blue"))
        n = 1
        print(colored("[*]", "yellow"), "Discovered %d routes with phone numbers" % len(self.phones))
        for phone in self.phones:
            print(colored("[" + str(n) + "]", "green").ljust(14, " "), phone)
            n += 1
        print(colored("--------------------------------------------------", "blue"))

    def getTotal(self):
        self.lock.acquire()
        self.total = len(self.routes)
        self.lock.release()
        return self.total


# Functions
def header():
    print("""
	 ______  _____          ______ __  __        
	|____  \|  __ \   /\   |  ____|  \/  |       
	 _   |  | |__) | /  \  | |__  | \  / | ___   
	|_|  |  |  _  / / /\ \ |  __| | |\/| |/ _ \  
	 ____|  | | \ \/ ____ \| |    | |  | |  __/  
	|______/|_|  \/_/    \_\_|    |_|  | |\___|  
	                                   | |       
	                     This is n0t4u |_| v.1.2.5


	Pages, Don't Run Away From Me, I will find you all!!!\n""")


def curlRequest(url, session):
    try:
        response = session.get(url, headers=headers, allow_redirects=True, verify=False, timeout=args.timeout[0],
                               proxies=proxies)
        return response.text
    except requests.exceptions.Timeout as timeout:
        print("Resquest to %s took to long. Consider increase timeout." % url)
        logging.debug(url, timeout)
        return False
    except requests.exceptions.TooManyRedirects as redirects:
        print("Too Many Redirects for %s" % url)
        logging.debug(url, redirects)
        return False
    except requests.exceptions.RequestException as e:
        print(e)
        logging.debug(e)
        # print(colored("Unable to connect with the specified domain.\nCheck is URL is correctly written.\n[NOTE] It is possible that a network security system is blocking the requests (Firewall/IPS)\n", "red") + colored("[ERROR] %s", "yellow") % e.args[1])
        sys.exit(0)


def getURLs(html, url):
    try:
        soup = BeautifulSoup(html, 'html.parser')
    except:
        pass
    else:
        for link in soup.find_all("a"):
            newRoute = link.get("href")
            if newRoute and len(newRoute) > 1:
                if re.search(r'[#?]', newRoute):
                    newRoute = re.split(r'[#?]', newRoute)[0]
                elif re.search(r'javascript:', newRoute):
                    if re.search(r'javascript:(next|window\.open)\([\"\']', newRoute):
                        newRoute = re.split(r'javascript:(next|window\.open)\([\"\']', newRoute)[1]
                    else:
                        continue
                elif re.search(r'mailto:', newRoute):
                    newRoute, mail = re.split(r'mailto:', newRoute, 1)
                    spider.newMail(mail)
                elif re.search(r'tel:', newRoute):
                    newRoute, phone = re.split(r'tel:', newRoute, 1)
                    spider.newPhone(phone)
                elif re.search(r'[\./]$', newRoute):
                    if re.search(r'[\./]{2}$', newRoute):
                        newRoute = newRoute[:-2]
                    else:
                        newRoute = newRoute[:-1]
                if not re.search(r'http[s]?://', newRoute):
                    newRoute = url + "/" + newRoute.lstrip("/")
                newRoute = newRoute.replace(" ", "%20")
                if re.search(r'\.(pdf|doc[x]?)$', newRoute, re.IGNORECASE):
                    spider.newDocument(newRoute)
                else:
                    spider.newRoute(newRoute)
        if args.all:
            getMisc(soup, url)
            getForms(soup)


def getURLsRecursive(html, url):
    try:
        soup = BeautifulSoup(html, 'html.parser')
    except:
        return
    else:
        for link in soup.find_all("a"):
            newRoute = link.get("href")
            if newRoute and len(newRoute) > 1:
                if re.search(r'[#?]', newRoute):
                    newRoute = re.split(r'[#?]', newRoute)[0]
                elif re.search(r'javascript:', newRoute):
                    if re.search(r'javascript:(next|window\.open)\([\"\']', newRoute):
                        newRoute = re.split(r'javascript:(next|window\.open)\([\"\']', newRoute)[1]
                    else:
                        continue
                elif re.search(r'mailto:', newRoute):
                    newRoute, mail = re.split(r'mailto:', newRoute, 1)
                    spider.newMail(mail)
                elif re.search(r'tel:', newRoute):
                    newRoute, phone = re.split(r'tel:', newRoute, 1)
                    phone = phone.replace(" ", "")
                    spider.newPhone(phone)
                elif re.search(r'[\./]$', newRoute):
                    if re.search(r'[\./]{2}$', newRoute):
                        newRoute = newRoute[:-2]
                    else:
                        newRoute = newRoute[:-1]
                if not re.search(r'http[s]?\://', newRoute):
                    newRoute = url + "/" + newRoute.strip("/")
                newRoute = newRoute.replace(" ", "%20")
                if re.search(r'\.(pdf|doc[x]?|odt|xls[x]?|sxc|txt|rft)$', newRoute, re.IGNORECASE):
                    spider.newDocument(newRoute)
                else:
                    if not args.avoid:
                        spider.newRouteToCrawl(newRoute)
                    elif args.avoid and not re.search(args.avoid[0], newRoute):
                        spider.newRouteToCrawl(newRoute)
        if args.all:
            getMisc(soup, url)
            getForms(soup)
        return


def getAPIURLsRecursive(html, url):
    try:
        urls = re.findall(r'http[s]?://[^\"]+', html, re.I)
    except Exception as e:
        logging.exception(e)
    else:
        for newRoute in urls:
            if re.search(r'[#?]', newRoute):
                newRoute = re.split(r'[#?]', newRoute)[0]
            elif re.search(r'javascript:', newRoute):
                if re.search(r'javascript:(next|window\.open)\([\"\']', newRoute):
                    newRoute = re.split(r'javascript:(next|window\.open)\([\"\']', newRoute)[1]
                else:
                    continue
            elif re.search(r'mailto:', newRoute):
                newRoute, mail = re.split(r'mailto:', newRoute, 1)
                spider.newMail(mail)
            elif re.search(r'tel:', newRoute):
                newRoute, phone = re.split(r'tel:', newRoute, 1)
                phone = phone.replace(" ", "")
                spider.newPhone(phone)
            elif re.search(r'[\./]$', newRoute):
                if re.search(r'[\./]{2}$', newRoute):
                    newRoute = newRoute[:-2]
                else:
                    newRoute = newRoute[:-1]
            if not re.search(r'http[s]?://', newRoute):
                newRoute = url + "/" + newRoute.strip("/")
            newRoute = newRoute.replace(" ", "%20")
            if re.search(r'\.(pdf|doc[x]?|odt|xls[x]?|sxc|txt|rft)$', newRoute, re.IGNORECASE):
                spider.newDocument(newRoute)
            else:
                if not args.avoid:
                    spider.newRouteToCrawl(newRoute)
                elif args.avoid and not re.search(args.avoid[0], newRoute):
                    spider.newRouteToCrawl(newRoute)
        return


def robots(rootDomain, session):
    print(colored("[»] Checking robots.txt...", "green"))
    robotsUrl = rootDomain.scheme + "://" + rootDomain.netloc.rstrip("/") + "/robots.txt"
    robots = curlRequest(robotsUrl, session)
    # TODO Rewrite code
    if robots and args.recursive:
        for route in re.findall(r"(?:A|Disa)+llow:\s+\S*", robots, re.X):
            if not re.search(r"[\*\$]+", route):
                logging.debug(route)
                try:
                    spider.newRouteToCrawl(rootDomain.scheme + "://" + rootDomain.netloc.rstrip("/") +
                                           re.split(r':\s+', route, maxsplit=1)[1].rstrip("/"))
                except Exception as e:
                    logging.debug(e)
    elif robots:
        for route in re.findall(r"(?:A|Disa)+llow:\s+\S*", robots, re.X):
            if not re.search(r"[\*$]+", route):
                logging.debug(route)
                try:
                    spider.newRoute(rootDomain.scheme + "://" + rootDomain.netloc.rstrip("/") +
                                    re.split(r':\s+', route, maxsplit=1)[1].rstrip("/"))
                except Exception as e:
                    logging.debug("[Exception] %s" % e)
    else:
        print(colored("[!] No robots detected", "yellow"))
    return


def sitemap(rootDomain):
    print(colored("[»] Checking sitemap.xml...", "green"))
    sitemapUrl = rootDomain.scheme + "://" + rootDomain.netloc.rstrip("/") + "/sitemap.xml"
    logging.info("[*] " + sitemapUrl)
    # req = urllib.request.Request(sitemapUrl, headers={'User-Agent': userAgent})
    try:
        # response = urllib.request.urlopen(req)
        response = curlRequest(sitemapUrl, session)
    except OSError as e:
        print(colored("[!] No sitemap detected", "yellow"))
        logging.debug("[Error] %s" % e)
    except Exception as e:
        logging.debug("[Error] %s" % e)
    else:
        try:
            soup = BeautifulSoup(response, 'xml')
        except Exception as e:
            raise e
        if sitemap and args.recursive:
            for route in soup.find_all("loc"):
                r1 = re.sub(r"^[\s]+", "", route.text)
                r2 = re.sub(r"[\s]+$", "", r1)
                spider.newRouteToCrawl(r2)
        elif sitemap:
            for route in soup.find_all("loc"):
                r1 = re.sub(r"^[\s]+", "", route.text)
                r2 = re.sub(r"[\s]+$", "", r1)
                # print(r2)
                spider.newRoute(r2)
        else:
            logging.info("[!] No sitemap detected.")
    return


def getMisc(soup, url):
    for link in soup.find_all("link"):
        newRoute = link.get("href")
        if newRoute and re.search(r'\.(css|jsp)', newRoute):
            if re.search(r'[#?]', newRoute):
                # Removes the parameters "#?" from the path and recover the path below
                route, att = re.split(r'[#?]', newRoute, maxsplit=1)
                if att and len(re.split('/', att, maxsplit=1)) == 2:
                    newRoute = route + "/" + re.split(r'/', att, maxsplit=1)[1]
            if not re.search(r'http[s]?://', newRoute):
                newRoute = url + "/" + newRoute.lstrip("/")
            newRoute = newRoute.replace(" ", "%20")
            spider.newCSS(newRoute)
        elif newRoute and re.search(r'\.(ico|jp[e]?g|png|svg)', newRoute):
            if not re.search(r'http[s]?://', newRoute):
                newRoute = url + "/" + newRoute.lstrip("/")
            newRoute = newRoute.replace(" ", "%20")
            spider.newSource(newRoute)

    for link in soup.find_all("script"):
        if link.get("rel") == "canonical":
            continue
        newRoute = link.get("src")
        if newRoute:
            if re.search(r'[#?]', newRoute):
                newRoute, aux = re.split(r'[#?]', newRoute, maxsplit=1)
                if aux and len(re.split('/', aux, maxsplit=1)) == 2:
                    newRoute = newRoute + "/" + re.split(r'/', aux, 1)[1]
            if not re.search(r'http[s]?://', newRoute):
                newRoute = url + "/" + newRoute.lstrip("/")
            newRoute = newRoute.replace(" ", "%20")
            spider.newJavaScript(newRoute, url)
    for link in soup.find_all("img"):
        newRoute = link.get("src")
        if newRoute:
            if re.search(r'base(64|32)', newRoute):
                return
            elif re.search(r'[#?]', newRoute):
                newRoute, aux = re.split(r'[#?]', newRoute, maxsplit=1)
                try:
                    newRoute = newRoute + "/" + re.split(r'/', aux, 1)[1]
                except:
                    continue
            if not re.search(r'http[s]?://', newRoute):
                newRoute = url + "/" + newRoute.lstrip("/")
            newRoute = newRoute.replace(" ", "%20")
            spider.newSource(newRoute)


def getForms(soup):
    for form in soup.find_all("form"):
        newForm = form.get("action")
        if newForm and newForm != "#":
            spider.newForm(newForm.lstrip("."))


def recursiveCrawl(spider, url, session):
    # logging.info(url)
    for i in range(args.recursive):
        for route in spider.toCrawl:
            nextRoute = spider.getRoute(route)
            html = curlRequest(nextRoute, session)
            time.sleep(args.sleep[0] / 1000)
            if html:
                logging.debug("%d\tThread %s %s" % (len(spider.toCrawl), threading.current_thread().name, route))
                logging.info(" %d routes left \t%s" % (len(spider.toCrawl), route))
                if args.api:
                    getAPIURLsRecursive(html, url)
                else:
                    getURLsRecursive(html, url)
            else:
                continue


def generateDictionary(spider, url):
    globalList = spider.routes + spider.documents + spider.css + spider.javascript + spider.sources
    logging.info(len(globalList))
    for route in globalList:
        if re.search(url, route):
            directories = route.lstrip("https://").lstrip("http://").split("/")
            directories.pop(0)
            for d in directories:
                if d not in dictionary and not re.search(
                        r'.(pdf|doc[x]?|htm[l]?|asp[x]?|php|jp[e]?g|png|svg|js|css|ico|jsp)$', d):
                    dictionary.append(d)
    dictionary.sort()


parser = argparse.ArgumentParser(description=header())
# Positional arguments
parser.add_argument("url", help="URL to crawl.", nargs=1)
# Main options
parser.add_argument("-r", "--recursive", dest="recursive", help="Recursive crawling. Number of depth crawl.", type=int,
                    choices=range(1, 6), default=0)
parser.add_argument("-s", "--sleep", dest="sleep", help="Sleeping time , in milliseconds, between requests.", type=int,
                    nargs=1, default=[0])
parser.add_argument("-t", "--threads", dest="threads", help="Number of threads. 4 by default.", type=int, nargs=1,
                    default=[4])
parser.add_argument("-T", "--timeout", dest="timeout", help="Set timeout for slow pages (sec).", nargs=1, type=int, default=[10])

# Headers options
parser.add_argument("-H", "--header", dest="header",
                    help="Add headers given to the request.\nExample:\"Authorization: Bearer <>,Cookie: <>\"", nargs=1)
parser.add_argument("-U", "--userAgent", dest="userAgent", help="User Agent for cURL requests. Random by default.",
                    nargs=1)
# Miscellaneous options
parser.add_argument("-R", "--root", dest="root", help="Root path for all the requests \n Example: www/ o /", nargs=1)
parser.add_argument("-A", "--avoid", dest="avoid", help="Route to avoid to crawl.", nargs=1)
parser.add_argument("--api", dest="api", help="Perform API crawler", action="store_true")
parser.add_argument("-P", "--proxy", dest="proxies", help="Proxy with IP:PORT format (Crawling performance will reduce).", nargs=1)
parser.add_argument("--cert", dest="cert", help="Proxy certificate path", nargs=1)

# Verbose options
verbosegroup = parser.add_mutually_exclusive_group()
verbosegroup.add_argument("-v", "--verbose", dest="verbose", help="Verbose mode.", action="store_true")
verbosegroup.add_argument("-vv", "--vverbose", dest="vverbose", help="Even more verbose", action="store_true")

# Output options
urlsgroup = parser.add_mutually_exclusive_group()
urlsgroup.add_argument("-u", "--urls", dest="urls", help="Print routes at the end of the rawling", action="store_true")
urlsgroup.add_argument("-a", "--all", dest="all", help="Print routes  and resources at the end of the crawling.",
                       action="store_true")
outputgroup = parser.add_mutually_exclusive_group()
outputgroup.add_argument("-o", "--output", dest="output", help="Output results in one file.", nargs=1)
outputgroup.add_argument("-oS", "--output-split", dest="outputSplit", help="Ouput results in two files, one for URLs and another for the rest of the routes (only valid with -a option).", nargs=1)
outputgroup.add_argument("-oA", "--output-split-all", dest="outputSplitAll", help="Output results  in several files, each one with its resources (only valid with -a option).", nargs=1)

dictgroup = parser.add_mutually_exclusive_group()
dictgroup.add_argument("-d", "--dictionary", dest="dictionary",
                       help="Generates a dictionary with all the paths detected and print them.", action="store_true")
dictgroup.add_argument("-do", "--dOutput", dest="dOutput",
                       help="Generates a dictionary with all the paths detected and store them in an output file.",
                       nargs=1)
parser.add_argument("--check", dest="check",
                    help="Check if dictionary paths are in the output file specified and write only new ones.",
                    action="store_true")

args = parser.parse_args()

# Main
if __name__ == '__main__':
    startTime = time.time()
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
        logging.captureWarnings(True)
    elif args.vverbose:
        logging.basicConfig(level=logging.DEBUG)
        logging.captureWarnings(True)
    spider = Spider()
    session = requests.session()
    session.max_redirects = 5
    # Proxy configuration. https://requests.readthedocs.io/en/latest/user/advanced/
    if args.proxies:
        if os.name == 'nt':
            print(colored("[!] Proxy functionality is not implemented yet for Windows.  Check README.md for more information.", "yellow"))
            check = input('Do you want to continue with this proxy functionality? (yes/NO)')
            if check.lower() == "yes":
                http_proxy = 'http://%s' % args.proxies[0]
                proxies = {'http': http_proxy, 'https': http_proxy}
        else:
            # Python requests configuration
            http_proxy = 'http://%s' % args.proxies[0]
            proxies = {'http': http_proxy, 'https': http_proxy}
            logging.info(colored("[*]", "blue") + "%s" % proxies)
            # System configuration
            certPath = args.cert[0] if args.cert else './cacert.pem'
            command = "export HTTP_PROXY='%s';export HTTPS_PROXY='%s';export REQUESTS_CA_BUNDLE='%s'" % (http_proxy, http_proxy, certPath)
            os.system(command)
    # Setup of headers
    if args.header:
        for header in args.header[0].split(","):
            key, value = header.split(":", 1)
            headers[key.strip(" ")] = value.strip(" ")
    spider.newRoute(args.url[0])
    rootDomain = urlparse(args.url[0])
    crawlRoot = rootDomain.netloc + rootDomain.path.rstrip("/")
    if not rootDomain.scheme:
        sys.exit(colored("FQDN must be given. https://n0t4u.com", "red"))
    print(colored("[»] Starting crawling...", "green"))
    # Setup of User-Agent
    if args.userAgent:
        userAgent = args.userAgent[0]
    else:
        userAgent = userAgents[random.randint(0, len(userAgents) - 1)]
    headers["User-Agent"] = userAgent

    # Setup of application root directory
    if args.root:
        if args.root[0] == "/":
            url = rootDomain.scheme + "://" + rootDomain.netloc
        else:
            url = rootDomain.scheme + "://" + rootDomain.netloc + "/" + args.root[0].strip("/")
    elif rootDomain[2]:
        url = rootDomain.scheme + "://" + rootDomain.netloc + "/" + rootDomain.path.strip("/")
    else:
        url = rootDomain.scheme + "://" + rootDomain.netloc.rstrip("/")
    # Start active execution
    startExecution = "[*] DRAFMe started '%s' command at %s." % (" ".join(sys.argv[:]).lstrip(" "), time.strftime("%a, %d %b %Y %H:%M:%S"))
    logging.info(startExecution)

    # Obtain information from robots.txt and sitemap.xml files
    robots(rootDomain, session)
    sitemap(rootDomain)
    htmlResponse = curlRequest(args.url[0], session)
    if args.recursive:
        if args.api:
            getAPIURLsRecursive(htmlResponse, url)
        else:
            getURLsRecursive(htmlResponse, url)
        try:
            threads = []
            for i in range(args.threads[0]):
                thread = threading.Thread(target=recursiveCrawl, args=(spider, url, session), name=i, daemon=True)
                thread.start()
                threads.append(thread)
            for thread in threads:
                thread.join()
        except KeyboardInterrupt:
            # CTRL+C
            print(colored("Crawling canceled...", "red"))
            threads.clear()
    else:
        if htmlResponse:
            getURLs(htmlResponse, url)
    print(colored("[»] Crawling ended", "green"))

    stopExecution = "[*] DRAFMe finished '%s' command at %s." % (" ".join(sys.argv[:]).lstrip(" "), time.strftime("%a, %d %b %Y %H:%M:%S"))
    logging.info(stopExecution)
    # Generate dictionary
    if args.dictionary:
        print(colored("[*] Creating path dictionary...", "blue"))
        generateDictionary(spider, url)
        logging.info(dictionary)
        for word in dictionary:
            print(word)
        print(colored("[*]", "blue"), "Discovered %d different paths" % len(dictionary))
    # Generate dictionary file
    elif args.dOutput:
        print(colored("[*]", "blue"), "Creating path dictionary...")
        generateDictionary(spider, url)
        # Avoid inserting duplicates
        if args.check:
            try:
                print(colored("[*]", "blue"), "Discovered %d different paths" % len(dictionary))
                with open(args.dOutput[0], "a+", encoding="utf-8") as file:
                    s = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
                    counter = 0
                    for word in dictionary:
                        if s.find(word.encode()) == -1:
                            file.write(word + "\n")
                            counter += 1
                    print(colored("%d new paths where written in %s dictionary" % (counter, args.dOutput[0]), "green"))
                file.close()
            except Exception as e:
                if e.args[0] == 13:
                    sys.exit(args.dOutput[0] + " " + colored(e.args[1], "red"))
                else:
                    # print(colored("[ERROR]", "red"), "File does not exist.")
                    with open(args.dOutput[0] + ".txt", "w+", encoding="utf-8") as file:
                        for word in dictionary:
                            file.write(word + "\n")
                        file.truncate(file.tell() - 1)
                    print(colored("[»] Dictionary created with %d new paths." % len(dictionary), "green"))
        else:
            if os.path.isfile(args.dOutput[0]):
                with open(args.dOutput[0], "a", encoding="utf-8") as file:
                    for word in dictionary:
                        file.write(word + "\n")
                    file.truncate(file.tell() - 1)
            else:
                with open(args.dOutput[0] + ".txt", "w", encoding="utf-8") as file:
                    for word in dictionary:
                        file.write(word + "\n")
                    file.truncate(file.tell() - 1)
            print(colored("[»] Dictionary created with %d new paths." % len(dictionary), "green"))
    # Output results into file
    if args.output:
        # f = open(args.output[0]+".txt","w", encoding="utf-8") #Cambiar por "a"
        with open(args.output[0] + ".txt", "w", encoding="utf-8") as file:
            file.write(startExecution + "\n\n")
            globalList = spider.routes + spider.documents + spider.css + spider.javascript + spider.sources
            for route in globalList:
                file.write(route + "\n")  # route.encode("utf-8")
            file.write("\n" + stopExecution)
        file.close()
        logging.info(colored("[*]", "blue") + " File %s.txt created" % args.output[0])
        print(colored("[*]", "blue"), "Discovered %d routes." % spider.getTotal())
    elif args.outputSplit:
        with open(args.outputSplit[0] + "_routes.txt", "w", encoding="utf-8") as file:
            file.write(startExecution + "\n\n")
            for route in spider.routes:
                file.write(route + "\n")  # route.encode("utf-8")
            # file.truncate(file.tell() - 1)
            file.write("\n" + stopExecution)
        logging.info(colored("[*]", "blue") + " File %s_routes.txt created" % args.outputSplit[0])
        if args.all:
            with open(args.outputSplit[0] + "_resources.txt", "w", encoding="utf-8") as file:
                file.write(startExecution + "\n\n")
                resourcesList = spider.documents + spider.css + spider.javascript + spider.sources
                for route in resourcesList:
                    file.write(route + "\n")  # route.encode("utf-8")
                # file.truncate(file.tell() - 1)
                file.write("\n" + stopExecution)
            logging.info(colored("[*]", "blue") + " File %s_resources.txt created" % args.outputSplit[0])
        print(colored("[*]", "blue"), "Discovered %d routes." % spider.getTotal())
    elif args.outputSplitAll:
        with open(args.outputSplitAll[0] + "_routes.txt", "w", encoding="utf-8") as file:
            file.write(startExecution + "\n\n")
            for route in spider.routes:
                file.write(route + "\n")  # route.encode("utf-8")
            # file.truncate(file.tell() - 1)
            file.write("\n" + stopExecution)
        logging.info(colored("[*]", "blue") + " File %s_routes.txt created" % args.outputSplitAll[0])
        if args.all:
            with open(args.outputSplitAll[0] + "_documents.txt", "w", encoding="utf-8") as file:
                file.write(startExecution + "\n\n")
                for route in spider.documents:
                    file.write(route + "\n")
                # file.truncate(file.tell() - 1)
                file.write("\n" + stopExecution)
            with open(args.outputSplitAll[0] + "_css.txt", "w", encoding="utf-8") as file:
                file.write(startExecution + "\n\n")
                for route in spider.css:
                    file.write(route + "\n")
                # file.truncate(file.tell() - 1)
                file.write("\n" + stopExecution)
            with open(args.outputSplitAll[0] + "_javascript.txt", "w", encoding="utf-8") as file:
                file.write(startExecution + "\n\n")
                for route in spider.javascript:
                    file.write(route + "\n")
                # file.truncate(file.tell() - 1)
                file.write("\n" + stopExecution)
            with open(args.outputSplitAll[0] + "_images.txt", "w", encoding="utf-8") as file:
                file.write(startExecution + "\n\n")
                for route in spider.sources:
                    file.write(route + "\n")
                # file.truncate(file.tell() - 1)
                file.write("\n" + stopExecution)
            with open(args.outputSplitAll[0] + "_forms.txt", "w", encoding="utf-8") as file:
                file.write(startExecution + "\n\n")
                for route in spider.forms:
                    file.write(route + "\n")
                # file.truncate(file.tell() - 1)
                file.write("\n" + stopExecution)
            with open(args.outputSplitAll[0] + "_emails.txt", "w", encoding="utf-8") as file:
                file.write(startExecution + "\n\n")
                for route in spider.mails:
                    file.write(route + "\n")
                # file.truncate(file.tell() - 1)
                file.write("\n" + stopExecution)
            with open(args.outputSplitAll[0] + "_phones.txt", "w", encoding="utf-8") as file:
                file.write(startExecution + "\n\n")
                for route in spider.phones:
                    file.write(route + "\n")
                # file.truncate(file.tell() - 1)
                file.write("\n" + stopExecution)
            logging.info(colored("[*]", "blue") + " Files %s_documents.txt, %s_css.txt, %s_javascript.txt, %s_images.txt, %s_forms.txt, %s_emails.txt and %s_phones.txt created" % (args.outputSplitAll[0], args.outputSplitAll[0], args.outputSplitAll[0], args.outputSplitAll[0],args.outputSplitAll[0], args.outputSplitAll[0], args.outputSplitAll[0]))
        print(colored("[*]", "blue"), "Discovered %d routes." % spider.getTotal())
    # Print only URLs.
    if args.urls:
        spider.printRoutes()
    # Print URLs, documents, images, JS, CSS, ...
    elif args.all:
        spider.printRoutes()
        spider.printMisc()
    if args.proxies and os.name != 'nt':
        unsetCommand = "unset HTTP_PROXY HTTPS_PROXY REQUESTS_CA_BUNDLE"
        os.system(unsetCommand)
    executionTime = time.time() - startTime
    if executionTime / 60 > 1:
        print(colored("--- %d secs --- (%d mins) ---" % (round(executionTime, 3), round(executionTime / 60, 3)),
                      "yellow"))
    else:
        print(colored("--- %d secs ---" % round(executionTime, 3), "yellow"))
