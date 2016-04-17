#! /usr/bin/env python
# encoding=utf8
# -*- coding: utf-8 -*-

# vaporize example:
# expects 5 pictures
# make clip.mp4 slideshow of 3 sec long shots using image001.jpg, image002.jpg, ...
# `ffmpeg -framerate 1/3 -i image%03d.jpg -c:v libx264 -pix_fmt yuv420p clip.mp4`
# export slideshow to final.mp4 video using short-macplus.mp3 (15 sec long)
# `ffmpeg -i clip.mp4 -i short-macplus.mp3 -vcodec copy final.mp4`

import tweepy, time, sys
from secrets import Secrets
from os import mkdir
from random import choice as choose
from set_interval import set_interval
from urllib import urlretrieve
from vaporize import vaporize

IMG_TYPES = ['jpg', 'jpeg', 'png', 'tiff']

def get_image_urls(tweet):
  if 'media' not in tweet.entities:
    return []

  urls = []

  for media in tweet.entities.get('media', [{}]):
    if media.get('type', None) == 'photo':
      urls.append(media['media_url'])
  return urls

def tag_reply(uname, msg):
  return '@' + uname + ': ' + msg

def prepare_image(url, tid):
  # first create the directory
  dir_path = './img-' + str(tid)
  mkdir(dir_path)
  # then download the image into it
  img_type = None

  for type in IMG_TYPES:
    if url.endswith(type):
      img_type = type

  if img_type is None:
    print 'NO IMAGE TYPE!'
    return None

  orig_img_path = dir_path + '/orig.' + img_type
  urlretrieve(url, orig_img_path)

  return orig_img_path

def process_status(status, responses):
  if status.retweeted or status.favorited:
    return

  USE_MP4 = False

  uname = status.user.screen_name
  image_urls = get_image_urls(status)

  print '\t' + str(status.id)
  print '\t' + status.text
  print '\t' + uname

  if uname == 'L0Z0RD' and 'test video' in status.text:
    print 'VAPORIZE TEST!'
    result_file_name = vaporize('pics', USE_MP4, IMG_TYPES)
    api.update_with_media(result_file_name, tag_reply(uname, 'ＩＴ ＩＳ ＣＯＭＰＬＥＴＥ'), status.id)
    api.create_favorite(status.id)
  # reply with the phrase is image is empty
  elif image_urls == []:
    resp = tag_reply(uname, choose(responses))
    print '\t' + resp
    api.update_status(resp, status.id)
    api.create_favorite(status.id)
  elif uname == 'L0Z0RD' and len(image_urls) > 0:
    for url in image_urls:
      prepare_image(url, status.id)
      # TODO: find_illuminati...
      # TODO: send response...
      # XXX: THIS IS TEMPORARY
      api.update_status('@LOZORD: it likely worked my dude', status.id)
      api.create_favorite(status.id)

  print '\n'

def handle_mentions(api, responses):
  for status in tweepy.Cursor(api.mentions_timeline).items():
    process_status(status, responses)

if __name__ == '__main__':
  print 'BOT STARTED! Use Ctrl-Z to "kill"\n'

  reload(sys)
  sys.setdefaultencoding('utf8')

  responses = None

  with open('responses.txt', 'r') as response_file:
    responses = response_file.readlines()

  auth = tweepy.OAuthHandler(Secrets['CONSUMER_KEY'], Secrets['CONSUMER_SECRET'])
  auth.set_access_token(Secrets['ACCESS_KEY'], Secrets['ACCESS_SECRET'])
  api = tweepy.API(auth)

  def interval_func():
    handle_mentions(api, responses)

  INTERVAL_TIME = 60 * 2 # two minutes

  interval_func()

  si_ret = set_interval(interval_func, INTERVAL_TIME)
