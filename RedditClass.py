import os
import requests
import json
from CustQueue import CustQueue
from MastodonClass import MastodonClass
from time import sleep

class RedditClass:

	def __init__(self, subreddit):
		self.subreddit = subreddit
		self.URL = 'https://www.reddit.com' + subreddit + '/hot/.json'
		self.store_name = 'redditstore.db'
		self.cached_reddit_ids = []
		self.message_queue = CustQueue()
		self.mastodonClass = MastodonClass()
		self.mastodonClass.initialize()
		self.readRedditFromFile()

	def redditUpdate(self):
		print 'Browsing Reddit...'
		r = requests.get(self.URL)
		sleep(2)
		data = r.json()
		
		print 'Processing request'
		
		for child in data['data']['children']:

			reddit_string = ''
			id = child['data']['id']

			if id in self.cached_reddit_ids or id=='640qr2' or id=='63ph2l':
				pass
			else:
				self.cached_reddit_ids.append(id)

				reddit_string += child['data']['title']
				reddit_string += ':\n\n'
				reddit_string += child['data']['url']

				self.message_queue.enqueue(reddit_string)

		self.writeRedditToFile()
	
	def dequeueMessage(self):
		if self.message_queue.size() > 0:
			#print self.message_queue.dequeue()
			self.shareToMastodon(self.message_queue.dequeue())
	
	def shareToMastodon(self, reddit_str):
		self.mastodonClass.toot(reddit_str)
	
	def readRedditFromFile(self):
		print "Reading Reddits from File"

		if os.path.isfile(self.store_name):
			with open(self.store_name, 'r') as redditStoreFile:
				data = redditStoreFile.read()

				for result in json.loads(data):
					self.cached_reddit_ids.append(str(result))
	
	def writeRedditToFile(self):
		print "Writing Reddits to File"

		file = open(self.store_name, 'w')
		file.write(json.dumps(self.cached_reddit_ids))
		file.close()
