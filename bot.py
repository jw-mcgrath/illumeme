#! /usr/bin/env python
# -*- coding: utf-8 -*-

# expects 5 pictures
# make clip.mp4 slideshow of 3 sec long shots using image001.jpg, image002.jpg, ...
# `ffmpeg -framerate 1/3 -i image%03d.jpg -c:v libx264 -pix_fmt yuv420p clip.mp4`
# export slideshow to final.mp4 video using short-macplus.mp3 (15 sec long)
# `ffmpeg -i clip.mp4 -i short-macplus.mp3 -vcodec copy final.mp4`

import tweepy, time, sys
from secrets import Secrets

print 'BOT STARTED!\n'

def vaporize(image_dir, audio_file='short-macplus.mp3'):
  pass

def process_status(status):
  print status.text
  print status.user.screen_name
  print '\n'

auth = tweepy.OAuthHandler(Secrets['CONSUMER_KEY'], Secrets['CONSUMER_SECRET'])
auth.set_access_token(Secrets['ACCESS_KEY'], Secrets['ACCESS_SECRET'])
api = tweepy.API(auth)

for status in tweepy.Cursor(api.mentions_timeline).items():
  process_status(status)
