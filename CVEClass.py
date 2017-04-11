import os
import json
from CustQueue import CustQueue
from ares import CVESearch
from dateutil import parser
from MastodonClass import MastodonClass

class CVEClass:

    def __init__(self):
        self.cve = CVESearch()
        self.store_name = 'cvestore.db'
        self.cached_cve_ids = []
        self.message_queue = CustQueue()
        self.mastodonClass = MastodonClass()
        self.mastodonClass.initialize()
        self.readCVEListFromFile()

    def cveUpdate(self):

        cves = json.loads(self.cve.last())
        str_list = []

        for result in cves['results']:

            cve_string = ""

            if result['id'].strip() in self.cached_cve_ids:
                pass
                #print "Ignoring - " + result['id']
            else:

                if len(self.cached_cve_ids) == 30:
                    self.cached_cve_ids.pop()

                self.cached_cve_ids.append(str(result['id']))
                self.cached_cve_ids = sorted(self.cached_cve_ids, reverse=True)
                
                dt = parser.parse(result['Published'])

                cve_string += "New CVE Notification"
                cve_string += "\n\n"
                cve_string += "Date: "
                cve_string += "{:%B %d, %Y}".format(dt) + "\n"               
                cve_string += "CVE-ID : "
                cve_string += result['id'] + "\n\n"
                cve_string += "Summary: "
                cve_string += result['summary'][:197] +"...\n\n"
                cve_string += "References: \n"

                for ref in result['references']:
                    cve_string += ref + "\n"

                str_list.append(cve_string +"\n")

        for revstr in list(reversed(str_list)):
            self.message_queue.enqueue(revstr)

        self.writeCVEListToFile()

    def dequeueMessage(self):
        if self.message_queue.size() > 0:
            #print self.message_queue.dequeue()
            self.shareToMastodon(self.message_queue.dequeue())

    def shareToMastodon(self, cve_str):
        self.mastodonClass.toot(cve_str)

    def readCVEListFromFile(self):
        print "Reading CVEList from file"
        if os.path.isfile(self.store_name):
            with open(self.store_name, 'r') as cveStoreFile:
                data= cveStoreFile.read().replace('\n', '')

                for result in json.loads(data):
                    self.cached_cve_ids.append(str(result))

    def writeCVEListToFile(self):
        print "Writing CVEList to file"
        file = open(self.store_name, 'w')
        file.write(json.dumps(self.cached_cve_ids))
        file.close()
