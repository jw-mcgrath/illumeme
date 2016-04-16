#! /usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, time, sys
from secrets import Secrets

print 'BOT STARTED!'

argfile = str(sys.argv[1])

auth = tweepy.OAuthHandler(Secrets['CONSUMER_KEY'], Secrets['CONSUMER_SECRET'])
auth.set_access_token(Secrets['ACCESS_KEY'], Secrets['ACCESS_SECRET'])
api = tweepy.API(auth)

with open(argfile, 'r') as file:
  lines = file.readlines()

for line in lines:
  print 'TWEETING: ' + line
  api.update_status(line)
  time.sleep(60 * 1)

