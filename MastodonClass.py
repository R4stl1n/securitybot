import os
import sys
from mastodon import Mastodon

class MastodonClass:

    def __init__(self):

        self.mastodon = None
        self.instance_url = 'https://securitymastod.one'

    def initialize(self):
        if not os.path.isfile("security_bot_clientcred.txt"):
            print("Creating app")
            self.mastodon = Mastodon.create_app(
                'security_bot_main',
                to_file = 'security_bot_clientcred.txt',
                api_base_url=self.instance_url
            )


        # Fetch access token if I didn't already
        if not os.path.isfile("security_bot_usercred.txt"):
            print("Logging in")
            self.mastodon = Mastodon(
                client_id = 'security_bot_clientcred.txt',
                api_base_url=self.instance_url        
            )
			email = sys.argv[1]
			password = sys.argv[2]
			self.mastodon.log_in(email, password, to_file = 'security_bot_usercred.txt')

        self.mastodon = Mastodon(
            client_id = 'security_bot_clientcred.txt',
            access_token = 'security_bot_usercred.txt',
            api_base_url=self.instance_url    
        )

    def toot(self, msg):
        print "Sending Toot"
        self.mastodon.toot(msg)

