#! /usr/bin/env python
# encoding=utf8
# -*- coding: utf-8 -*-

import tweepy, time, sys
from secrets import Secrets
from os import mkdir
from random import choice as choose
from set_interval import set_interval
from urllib import urlretrieve
from vaporize import vaporize
from buildsequence import build

IMG_TYPES = ['jpg', 'jpeg', 'png', 'tiff']
KEYWORDS = ['vapor', 'vape', 'dank', 'meme', 'uncommon']

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

  # TODO: remove lozord checks
  '''
  if uname == 'L0Z0RD' and 'test video' in status.text:
    print 'VAPORIZE TEST!'
    result_file_name = vaporize('pics', USE_MP4, IMG_TYPES)
    api.update_with_media(result_file_name, tag_reply(uname, 'ＩＴ ＩＳ ＣＯＭＰＬＥＴＥ'), status.id)
    api.create_favorite(status.id)
  '''
  # reply with the phrase is image is empty and no kws
  if image_urls == []:

    if status.text in KEYWORDS:
      # pull a photo from reddit
      dir_path = './img-%s' % status.id
      mkdir(dir_path)
      build(dir_path)
      # make gif
      result_path = vaporize(dir_path, False, IMG_TYPES)
      resp = tag_reply(uname, '4 u, fam #uncommonhacks')
      api.update_with_media(result_path, resp, status.id)
    else:
      resp = tag_reply(uname, choose(responses))
      print '\t' + resp
      api.update_status(resp, status.id)

    api.create_favorite(status.id)

  else:
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
