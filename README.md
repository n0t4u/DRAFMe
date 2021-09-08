# DRAFMe

Don't Run Away From Me is a fast multi-threading Python 3 web crawler.
It's features include:
- Obtain all web pages in seconds.
- Distinguish between pages, documents, scripts, style sheets, images,...
- Flexible crawl, you decide the number of threads, the timeout between requests, the crawl depth, the user agent or the headers.
- Generate a path diccionary and add it to your personal dictionary for future directory fuzzings.
- Stop the crawler whenever you want, you will get the routes obtained until that moment.

## Installation
Simple installation, simple usage
```sh
$ git clone https://github.com/n0t4u/DRAFMe.git
$ cd DRAFMe
$ python3 -m pip install -r requirements.txt
$ chmod +x DRAFMe.py
```
## Usage
The only mandatory attribute is the FQDN of the domain you want to crawl.
All the options can be diplayed with the option -h or --help

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
$ python3 DRAFMe.py -o routes_file.txt -do dictionary.txt
````

### Store path dictionary into dictionary file
This will perform a basic crawl, generate a dictionary with all the unique paths found and write them into the given file only if this path is not already in the dictionary.
Useful for future directory fuzzings.
```sh
$ python3 DRAFMe.py  -do dictionary.txt --check
````

### Play with the directories
Sometimes the main page is in one directory and then all the resources in a diferent one. This option will force the root directory for the next requests.
Furthermore, you can specify directories you do not want to crawl. (Note. The more specific the subdirectory it is, the more restrictive it works this option. The routes will still appear in the results, but no crawling will be done inside them).
```sh
$ python3 DRAFME.py -a -R "/" -A "/media/" https://example.com/example
```

### Customize options
This will perform a recursive crawl with the options given, including the crawling depth, the timeout between requests and the number of simultaneous threads. Customize your own User Agent or add specific headers.
```sh
$ python3 DRAFME.py -a -r 2 -s 200 -t 10 -U "Mozilla/5.0 n0t4u" -H "Authorization: Bearer <n0t4u>" https://example.com
```

### Verbose mode
If you don't believe this tool works (sometimes i really don't) use the verbose mode to check that your computer is doing something useful.
```sh
$ python3 DRAFME.py -a -r 2 -s 200 -t 100 -v https://example.com
```
## TO DO
Take a nap ***zzzZZZ***
And then check routes in comments

## Author 
n0t4u

## License
GNU General Public License Version 3

## Disclaimer
This tool is only purposed for Ethical Hacking audits. This tool will ignore robots.txt. The author is not responsible for any use by third parties.