#! /usr/bin/env python
# -*- coding: utf-8 -*-

# vaporize example:
# expects 5 pictures
# make clip.mp4 slideshow of 3 sec long shots using image001.jpg, image002.jpg, ...
# `ffmpeg -framerate 1/3 -i image%03d.jpg -c:v libx264 -pix_fmt yuv420p clip.mp4`
# export slideshow to final.mp4 video using short-macplus.mp3 (15 sec long)
# `ffmpeg -i clip.mp4 -i short-macplus.mp3 -vcodec copy final.mp4`

import tweepy, time, sys
from secrets import Secrets
from subprocess import call
from os import listdir
from string import Template

def vaporize(image_dir, audio_file='short-macplus.mp3'):
  # first get image type
  dir_contents = listdir(image_dir)
  image_type = None

  TYPES = ['jpg', 'jpeg', 'png', 'tiff']

  for filename in dir_contents:
    for some_type in TYPES:
      if filename.endswith(some_type):
        image_type = some_type
        break

  slideshow_cmd = Template('ffmpeg -framerate 1/3 -i $idr/image%03d.$itp -c:v libx264 -pix_fmt yuv420p $idr/show.mp4')
  movie_cmd = Template('ffmpeg -i $idr/show.mp4 -i ./short-macplus.mp3 -vcodec copy $idr/final.mp4')

  slideshow_cmd = slideshow_cmd.substitute(idr = image_dir, itp = image_type)
  movie_cmd = movie_cmd.substitute(idr = image_dir)

  print '\n\n\t' + slideshow_cmd + '\n\n\t' + movie_cmd + '\n\n'

  call(slideshow_cmd.split(' '))
  call(movie_cmd.split(' '))

  return (image_dir + '/final.mp4')

def get_image_urls(tweet):
  if 'media' not in tweet.entities:
    return []

  urls = []

  for media in tweet.entities.get('media', [{}]):
    if media.get('type', None) == 'photo':
      urls.append(media['media_url'])
  return urls

def process_status(status):
  print status.text
  print status.user.screen_name
  # print status.entities
  print (get_image_urls(status) or 'No images')
  print '\n'

if __name__ == '__main__':
  print 'BOT STARTED!\n'

  auth = tweepy.OAuthHandler(Secrets['CONSUMER_KEY'], Secrets['CONSUMER_SECRET'])
  auth.set_access_token(Secrets['ACCESS_KEY'], Secrets['ACCESS_SECRET'])
  api = tweepy.API(auth)

  for status in tweepy.Cursor(api.mentions_timeline).items():
    process_status(status)
