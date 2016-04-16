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
from subprocess import call
from os import listdir
from string import Template
from random import choice as choose

def vaporize(image_dir, make_mp4_instead_of_gif, audio_file='short-macplus.mp3'):
  # first get image type
  dir_contents = listdir(image_dir)
  image_type = None

  TYPES = ['jpg', 'jpeg', 'png', 'tiff']

  for filename in dir_contents:
    for some_type in TYPES:
      if filename.endswith(some_type):
        image_type = some_type
        break

  if image_type is None:
    print 'UNKNOWN IMAGE TYPE!'

  slideshow_cmd = Template('ffmpeg -framerate 1/3 -i $idr/image%03d.$itp -c:v libx264 -pix_fmt yuv420p $idr/show.mp4')
  # TODO: pipe `yes` for overwriting?
  slideshow_cmd = '' + slideshow_cmd.substitute(idr = image_dir, itp = image_type)

  result_cmd = None
  result_path = None

  if make_mp4_instead_of_gif:
    result_cmd = Template('ffmpeg -i $idr/show.mp4 -i ./short-macplus.mp3 -vcodec copy $idr/final.mp4')
    result_path = image_dir + '/final.mp4'
  else:
    result_cmd = Template('ffmpeg -i $idr/show.mp4 $idr/final.gif')
    result_path = image_dir + '/final.gif'

  # TODO: pipe `yes` for overwriting?
  result_cmd = '' + result_cmd.substitute(idr = image_dir)

  call(slideshow_cmd.split(' '))
  call(result_cmd.split(' '))

  return result_path

def get_image_urls(tweet):
  if 'media' not in tweet.entities:
    return []

  urls = []

  for media in tweet.entities.get('media', [{}]):
    if media.get('type', None) == 'photo':
      urls.append(media['media_url'])
  return urls


RESPONSES = [
    'Ｍ∆ＫＥ ＴＨＥ ＰＬ∆Ｚ∆ ＧＲＥ∆Ｔ ∆Ｇ∆ＩＮ #uncommonhacks',
    'отдых в Припяти #uncommonhacks',
    'ＤＡＮＫ#uncommonhacks',
    'ｗｈｅｒｅ＇ｓ ｔｈｅ ｂｉｒｔｈ ｃｅｒｔｉｆｉｃａｔｅ ｔｈｏ#uncommonhacks',
    'ＡＬＯＨＡ#uncommonhacks',
    'ＴＲＵＳＴ ＴＨＥ ＢＲ∆ＮＤ#uncommonhacks',
    'Do you drink @FIJIWater? #uncommonhacks',
    'Have you eaten your daily ration of celery today? #uncommonhacks',
    'Make ∆merica Great Again™ @realDonaldTrump #uncommonhacks'
]

def tag_reply(uname, msg):
  return '@' + uname + ': ' + msg

def process_status(status):
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
    result_file_name = vaporize('pics', USE_MP4)
    api.update_with_media(result_file_name, tag_reply(uname, 'ＩＴ ＩＳ ＣＯＭＰＬＥＴＥ'), status.id)
    api.create_favorite(status.id)
  # reply with the phrase is image is empty
  elif image_urls == []:
    resp = tag_reply(uname, choose(RESPONSES))
    print '\t' + resp
    api.update_status(resp, status.id)
    api.create_favorite(status.id)

  print '\n'

if __name__ == '__main__':
  print 'BOT STARTED!\n'

  reload(sys)
  sys.setdefaultencoding('utf8')

  auth = tweepy.OAuthHandler(Secrets['CONSUMER_KEY'], Secrets['CONSUMER_SECRET'])
  auth.set_access_token(Secrets['ACCESS_KEY'], Secrets['ACCESS_SECRET'])
  api = tweepy.API(auth)

  for status in tweepy.Cursor(api.mentions_timeline).items():
    process_status(status)
