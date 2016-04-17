import requests
import json
import random
import yaml
import tweepy

class JaidenQuote:
    def __init__(self):
        self.res = requests.get("https://www.reddit.com/r/ShitJadenSays/search.json?q=site%3Atwitter.com&restrict_sr=on&sort=relevance&t=all",headers ={"user-agent":"Bot by /u/joshmcgrath"} )
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
        print ID
        twit = self.api.get_status(ID)
        #f = open('jaiden.json','w')
        return twit.text


