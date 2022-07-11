import argparse
import socket
import time 
import threading
from queue import Queue
from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import os
from datetime import datetime
import sys 
import webbrowser
parser = argparse.ArgumentParser()

parser.add_argument('--target', type=str, required=False)
parser.add_argument('--delay', type=str, required=False)
parser.add_argument('--test', type=str, required=False)
parser.add_argument('--gui', type=str, required=False)
args = parser.parse_args()
os.system('clear')
if args.gui =='v1':
    os.system('cd webapp')
    os.system('python3 start.py')
print('Scanning: ', args.target)
target = args.target
# Defining a target
 
# Add Banner
print("-" * 50)
print("Scanning Target: " + target)
print("Scanning started at:" + str(datetime.now()))
print("-" * 50)
  
try:
     
    # will scan ports between 1 to 65,535
    for port in range(1,65535):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
         
        # returns an error indicator
        result = s.connect_ex((target,port))
        if result ==0:
            print("Port {} is open".format(port))
        s.close()
         
except KeyboardInterrupt:
        print("\n Exiting Program !!!!")
        sys.exit()
except socket.gaierror:
        print("\n Hostname Could Not Be Resolved !!!!")
        sys.exit()
except socket.error:
        print("\ Server not responding !!!!")
        sys.exit()

class Worker:
    base_url = ''
    queue = []
    crawled = set()
    lock = threading.Semaphore(value=1)

    def __init__(self, base_url):
        self.base_url = base_url
        self.queue = [base_url]

    @staticmethod
    def write_file(path, data):
        with open(path, 'a') as f:
            f.write(data)
            f.close()

    def report(self, url):
        with self.lock:
            print("Successfully crawled", url)

    def work(self):
        for link in self.queue:

            try:
                page = urlopen(link)
                soup = BeautifulSoup(page, 'lxml')

                self.write_file("dump.txt", soup.text)
                self.write_file("log.txt", link + "\n")
                self.report(link)
                self.crawled.add(link)

                for upper_domain in soup.find_all('a', href=True):
                    joined_link = urljoin(self.base_url, upper_domain['href'])
                    if joined_link not in self.crawled:
                        self.queue.append(joined_link)

            except:
                # log any failed URL crawls and continue
                self.write_file("error_log.txt", str(link) + "\n")
                pass
