# DRAFMe

Don't Run Away From Me is a fast multi-threading Python 3 web crawler.
It's features include:
- Obtain all web pages in seconds.
- Distinguish between pages, documents, scripts, style sheets, images,...
- Flexible craswl, you decide the number of threads, the timeout between requests, the crawl depth or the user agent.
- Generate path diccionary and add it to you personal dictionary for directory fuzzing.
- Stop the crawler whenever you want, you will get the routes obtained until that moment.

## Installation
```sh
$ git clone https://github.com/n0t4u/DRAFMe.git
$ cd DRAFMe
$ python3 -m pip install -r requirements.txt
$ chmod +x DRAFMe.py
```
## Usage
Usage is simple and all the options can be diplayed with the option -h or --help

### Basic usage
This will perform a basic crawl and will display the pages routes in the terminal
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
### Customize options
This will perform a recursive crawl with the options given, including the crawling depth, the timeout between requests and th number of simultaneous threads. Customize your own User Agent.
```sh
$ python3 DRAFME.py -a -r 2 -s 200 -t 10 -U "Mozilla/5.0 n0t4u" https://example.com
```

### Verbose mode
If you don't believe this tool works (sometimes i really don't) use the verbose mode to check that your computer is doing something useful.
```sh
$ python3 DRAFME.py -a -r 2 -s 200 -t 100 -v https://example.com
```
## TO DO
Option to avoid crawl specific directories

## Author 
n0t4u

## License
GNU General Public License Version 3
