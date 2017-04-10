import os, sys
import json
from sets import Set
from time import sleep
from CVEClass import CVEClass
from RedditClass import RedditClass
from RepeatedTimer import RepeatedTimer

print "starting..."

cveClass = CVEClass()
cveClassRt = RepeatedTimer(300, cveClass.cveUpdate) # Update every 5 minutes
cvePostRt = RepeatedTimer(480, cveClass.dequeueMessage) # Post every 8 minutes

redditClass = RedditClass('/r/netsec')
redditClassRt = RepeatedTimer(1800, redditClass.redditUpdate) # Update every 30 minutes
redditPostRt = RepeatedTimer(480, redditClass.dequeueMessage) # Post every 8 minutes

try:
    while True:
        sleep(60)
except Exception as e:
    e.msg()
finally:
    redditClassRt.stop()
    redditPostRt.stop()
