# DRAFMe

Don't Run Away From Me is a fast multi-threading Python 3 web crawler.
It's features include:
- Obtain all web pages in seconds.
- Distinguish between pages, documents, scripts, style sheets, images,...
- Flexible crawl, you decide the number of threads, the timeout between requests, the crawl depth, the user agent or the headers.
- Generate a path dictionary and add it to your personal dictionary for future directory fuzzing.
- Stop the crawler whenever you want, you will get the routes obtained until that moment.

## Installation
Simple installation, simple usage
```sh
$ sudo git clone https://github.com/n0t4u/DRAFMe.git /opt/DRAFMe
$ cd /opt/DRAFMe
$ sudo python3 -m pip install -r requirements.txt
$ chmod +x DRAFMe.py
$ (Optional) echo 'alias DRAFMe="python3 /opt/DRAFMe/DRAFMe.py"' >> ~/.zshrc
```
## Usage
The only mandatory attribute is the FQDN of the domain you want to crawl.
All the options can be displayed with the option -h or --help

### Basic usage
This will perform a basic crawl and will display the page routes obtained in the terminal
```sh
$ python3 DRAFMe.py -u  https://example.com
```
### Display all the resources
This will perform a basic crawl and will display all the routes obtained, including all the resources found, in the terminal
```sh
$ python3 DRAFMe.py -a https://example.com
````
### Generate a dictionary with all the paths
This will perform a basic crawl and will display the unique paths found during the crawler.
```sh
$ python3 DRAFMe.py -d https://example.com
````
### Output the results
This will perform a basic crawl and will store all the routes and the dictionary into the files you specified.
```sh
# Basic output
$ python3 DRAFMe.py -o routes_file -do dictionary_file
# Split output in several files base on its contents (see help)
$ python3 DRAFMe.py -oS routes_file
$ python3 DRAFMe.py -oA routes_file
````

### Store path dictionary into dictionary file
This will perform a basic crawl, generate a dictionary with all the unique paths found and write them into the given file only if this path is not already in the dictionary.
Useful for future directory fuzzing.
```sh
$ python3 DRAFMe.py  -do dictionary.txt --check
````

### Play with the directories
Sometimes the main page is in one directory and then all the resources in a different one. This option will force the root directory for the next requests.
Furthermore, you can specify directories you do not want to crawl. (Note. The more specific the subdirectory it is, the more restrictive it works this option. The routes will still appear in the results, but no crawling will be done inside them).
```sh
$ python3 DRAFME.py -a -R "/" -A "/media/" https://example.com/example
```

### API Crawling
In some cases, it is possible to get multiple routes from open API. Use the --api option to change the behaviour of the crawler.
```sh
$ python3 DRAFMe.py -a https://example.com --api
````

### Customize options
This will perform a recursive crawl with the options given, including the crawling depth, the timeout between requests and the number of simultaneous threads, the response timeout o the use of a proxy. Customize your own User Agent or add specific headers.
```sh
$ python3 DRAFME.py -a -r 2 -s 200 -t 10 -T 10 --proxy "127.0.0.1:8080" --cert "/home/user/cacert.pem" -U "Mozilla/5.0 n0t4u" -H "Authorization: Bearer <n0t4u>" https://example.com
```

#### Setup proxy (Linux only)
In order to properly handle request via proxy it is necessary to add this configuration to your machine before executing DRAFMe.
```
# Generate certificate in PEM format
$ openssl x509 -in cacert.der -out cacert.pem

# Set environmental variables
$ export HTTP_PROXY="http://127.0.0.1:8080"
$ export HTTPS_PROXY="http://127.0.0.1:8080"
$ export REQUESTS_CA_BUNDLE="path/to/cert/file.pem"

# Back to the initial state
$ unset HTTP_PROXY HTTPS_PROXY REQUESTS_CA_BUNDLE
```

References: https://requests.readthedocs.io/en/latest/user/advanced/#proxies

**Note.** For Windows machines try to add the environmental variables manually ([Windows --> Edit system environment variables](https://docs.cloudfoundry.org/cf-cli/http-proxy.html#windows))([Self-Signed Certificates](https://docs.cloudfoundry.org/cf-cli/self-signed.html#windows))

### Verbose mode
If you don't believe this tool works (sometimes i really don't) use the verbose mode to check that your computer is doing something useful.

Verbose mode: -v
Debug mode: -vv
```sh
$ python3 DRAFME.py -a -r 2 -s 200 -t 100 -v https://example.com
```
## TO DO
- Add external resources links
- Add metrics of analyzed routes --> Graph?

### Backlog
- Detect JS versions
- Add Selenium support
- Add proxy support for Windows
- Check recursive
- Consider import latest-user-agents https://pypi.org/project/latest-user-agents/
- Take a nap ***zzzZZZ***
- And then check routes in comments.


## Note
Main branch is a major update and now uses Python3 requests library.

If you want to use an old, but fully operative, version with Pycurl library, check [pycurl-requests](https://github.com/n0t4u/DRAFMe/tree/pycurl-requests) branch.

## Author 
n0t4u

## License
GNU General Public License Version 3

## Disclaimer
This tool has been designed for Ethical Hacking audits and it can only be used with the authorization of the client. This tool will ignore robots.txt. The author is not responsible for any use by third parties.