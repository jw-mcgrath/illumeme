from os import listdir
from string import Template
from subprocess import call
from random import choice as choose

# vaporize example:
# expects 5 pictures
# make clip.mp4 slideshow of 3 sec long shots using image001.jpg, image002.jpg, ...
# `ffmpeg -framerate 1/3 -i image%03d.jpg -c:v libx264 -pix_fmt yuv420p clip.mp4`
# export slideshow to final.mp4 video using short-macplus.mp3 (15 sec long)
# `ffmpeg -i clip.mp4 -i short-macplus.mp3 -vcodec copy final.mp4`

def vaporize(image_dir, make_mp4_instead_of_gif, img_types, audio_file='short-macplus.mp3'):
  # first get image type
  dir_contents = listdir(image_dir)
  image_type = None

  for filename in dir_contents:
    for some_type in img_types:
      if filename.endswith(some_type):
        image_type = some_type
        break

  if image_type is None:
    print 'UNKNOWN IMAGE TYPE!'
    return None

  # add the `you decide` feature
  # link a random yd[1-5] to image099.type to the proper directory
  YOU_DECIDES = ['yd1', 'yd2', 'yd3', 'yd4', 'yd5']
  yd_cmd = Template('ln ./you-decide/$ydn.$itp $idr/image00$l.$itp')
  img_files = filter(lambda file: file.endswith(image_type), dir_contents)
  yd_cmd = yd_cmd.substitute(ydn = choose(YOU_DECIDES), itp = image_type, idr = image_dir, l = str(len(img_files) + 1))
  print yd_cmd
  call(yd_cmd.split(' '))

  slideshow_cmd = Template('ffmpeg -loglevel panic -framerate 1/2 -i $idr/image%03d.$itp -c:v libx264 -pix_fmt yuv420p $idr/show.mp4')
  # TODO: pipe `yes` for overwriting?
  slideshow_cmd = '' + slideshow_cmd.substitute(idr = image_dir, itp = image_type)

  result_cmd = None
  result_path = None

  if make_mp4_instead_of_gif:
    result_cmd = Template('ffmpeg -loglevel panic -i $idr/show.mp4 -i ./$adf -strict -2 -vcodec copy $idr/final.mp4')
    # result_path = image_dir + '/' + image_dir + '-' + 'final.mp4'
    result_path = 'final.mp4'
  else:
    result_cmd = Template('ffmpeg -loglevel panic -i $idr/show.mp4 $idr/final.gif')
    # result_path = image_dir + '/' + image_dir + '-' + 'final.gif'
    result_path = 'final.gif'

  # TODO: pipe `yes` for overwriting?
  result_cmd = '' + result_cmd.substitute(idr = image_dir, adf = audio_file)

  call(slideshow_cmd.split(' '))
  call(result_cmd.split(' '))

  return result_path
