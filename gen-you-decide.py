import os
from subprocess import call

orig_files = os.listdir('./you-decide')

print 'Original files: ' + str(orig_files)

NEW_TYPES = ['jpg', 'jpeg', 'tiff']

for png_file in orig_files:
  for img_type in NEW_TYPES:
    file_name = os.path.splitext(png_file)[0]
    cmd = 'ffmpeg -loglevel panic -i ./you-decide/%s ./you-decide/%s.%s' % (png_file, file_name, img_type)
    # print cmd
    call(cmd.split(' '))
