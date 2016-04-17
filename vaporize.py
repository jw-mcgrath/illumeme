from os import listdir
from string import Template
from subprocess import call

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