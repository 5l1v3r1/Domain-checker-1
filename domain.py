#!/usr/bin/python

import pythonwhois
import threading
import Queue
import sys


queue = Queue.Queue()
domains = open('/root/Desktop/domains','r').read().splitlines()


class CheckDomains(threading.Thread):
    
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while not self.queue.empty():
            dom = self.queue.get()
            details = pythonwhois.get_whois(dom)
            try:
                exist = details['creation_date']
                if exist:
                    print "%s does exist" % (dom)
            except:
	        print "[!] - %s does not exist" % (dom)
                pass
            

threads = []

for domain in domains:
    queue.put(domain)


for i in range(20):
    t = CheckDomains(queue)
    t.daemon = True
    t.start()
    threads.append(t)

queue.join()

if Queue.empty():
    print "yes"

for thread in threads:
    thread.join()
