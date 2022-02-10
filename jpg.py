import subprocess
import time

# Output a single frame from the video into an image file:
# ffmpeg -i input.mov -ss 00:00:14.435 -vframes 1 out.png

# Output one image every second, named out1.png, out2.png, out3.png, etc.
# The %01d dictates that the ordinal number of each output image will be formatted using 1 digits.
# ffmpeg -i input.mov -vf fps=1 out%d.png

# Output one image every minute, named out001.jpg, out002.jpg, out003.jpg, etc. 
# The %02d dictates that the ordinal number of each output image will be formatted using 2 digits.
# ffmpeg -i input.mov -vf fps=1/60 out%02d.jpg

# Extract all frames from a 24 fps movie using ffmpeg
# The %03d dictates that the ordinal number of each output image will be formatted using 3 digits.
# ffmpeg -i input.mov -r 24/1 out%03d.jpg

# Output one image every ten minutes:
# ffmpeg -i input.mov -vf fps=1/600 out%04d.jpg


def createJpgs(settings):

# ffmpeg -i input.mov -r 60/1 out%04d.jpg
  jpg = ['ffmpeg','i',settings['InputFileDir']+settings['InputFilename']+settings['InputExtension'],'-r','zgv%04d.jpg']

  for arg in jpg:
    # Print the args without the brackets and commas
    print(arg, end=" ", flush=True)

  if settings['SkipEncoding']:
    print('skipping image extraction.')
    return True
  
  t1 = time.localtime()
  # current_time = time.strftime("%H:%M:%S", t)
  # print(current_time)
  print("\nRunning jpeg extraction: "+ time.strftime("%H:%M:%S", t1))

  if not settings['SkipEncoding']:
    commandResult = subprocess.run(jpg, capture_output=True)
  print(commandResult)

  return True