import sys
import requests
import json
import random
import yaml
import tweepy

class Quote:
    def __init__(self,person):
        self.person = person
        self.res = requests.get("https://www.reddit.com/r/Shit"+person+"Says/search.json?q=site%3Atwitter.com&restrict_sr=on&sort=relevance&t=all",headers ={"user-agent":"Bot by /u/joshmcgrath"} )
        self.dic = json.loads(self.res.text)
        self.secrets = yaml.safe_load(open('secrets.json'))
        auth = tweepy.OAuthHandler(self.secrets["CONSUMER_KEY"],self.secrets["CONSUMER_SECRET"])
	auth.set_access_token(self.secrets["ACCESS_KEY"], self.secrets["ACCESS_SECRET"]) 
        self.api = tweepy.API(auth)
    def get(self):
        length = len(self.dic["data"]["children"])
        selectedUrl =  self.dic["data"]["children"][random.randrange(length-1)]["data"]["url"]
        split_url = selectedUrl.split("/")
        ID = split_url[len(split_url) - 1]
        twit = self.api.get_status(ID)
        return json.dumps({'body' :twit.text, 'author':self.person}) 

def main():
    jaden = Quote(sys.argv[1])
    if not (sys.argv[1] == 'Trump') and not(sys.argv[1] == 'Jaden'):
        raise Exception("arg was: "+ str(sys.argv) )
    print jaden.get()

if __name__ == '__main__':
    main()
