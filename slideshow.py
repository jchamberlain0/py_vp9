import subprocess
import time
import sys

# Encode a single lossless vp9 video from the unique png file sequence output by the OCR script.
# This file can be encoded again to create another set of quality options in the "slideshow video" format.
# ffmpeg -framerate 20 -i %05d.png -pix_fmt yuv444p -c:v libvpx-vp9 -lossless 1 lossless-p.webm
def encodeLossless(settings):

  # if not settings["RunOCR"]:
  #   print('OCR is disabled. Creating video at ')

  framerate = "20"


  # If ocr mode is not turned on, a slideshow may still be created from the frame dump.
  # Is there a point in doing this?
  if settings["RunOCR"]:
    # If OCR mode is on, create a 20fps slideshow from the unique images.
    uniqueDirectory = settings['OutFileDir']+settings['NewOutputFolder']+"/unique/"
    framerate = "20"
  else:
    # If OCR is off, create a 60fps slideshow from the non-unique images.
    # This format is for native 60fps recordings and will not have great results for low framerate games.
    uniqueDirectory = settings['OutFileDir']+settings['NewOutputFolder']+"/images/"
    framerate = "60"
  
  slideshowDirectory = settings['OutFileDir']+settings['NewOutputFolder']+"/ss/"
  outputFile = slideshowDirectory+"lossless.webm"

  # List of arguments to pass to ffmpeg
  slideshow = ['ffmpeg']
  slideshow.append("-y")
  slideshow.append("-framerate")
  slideshow.append(framerate)
  slideshow.append("-i")
  slideshow.append(uniqueDirectory+"%05d.png")
  slideshow.append("-pix_fmt")
  slideshow.append("yuv444p")
  slideshow.append("-c:v")
  slideshow.append("libvpx-vp9")
  slideshow.append("-lossless")
  slideshow.append("1")
  slideshow.append(outputFile)

  commandResult = ''

  t1 = time.localtime()
  print("\nCreating lossless slideshow VP9: "+ time.strftime("%H:%M:%S", t1))

  for arg in slideshow:
    # Print the args without the brackets and commas
    print(arg, end=" ", flush=True)
  # TODO: rest of script will fail if this lossless file isn't here,
  # due to ffprobe trying to find it. Turn back on "skipencoding" check
  # commandResult = subprocess.run(slideshow, capture_output=True)

  process = subprocess.Popen(slideshow, shell = True,bufsize = 1,
                           stdout=subprocess.PIPE, stderr = subprocess.STDOUT,encoding='utf-8', errors = 'replace' ) 
  while True:
    realtime_output = process.stdout.readline()
    if realtime_output == '' and process.poll() is not None:
      break
    if realtime_output:
      print(realtime_output.strip(), flush=False)
      sys.stdout.flush()
  
  print(commandResult)
  # if not settings['SkipEncoding']:
  #   commandResult = subprocess.run(slideshow, capture_output=True)
  # print(commandResult)

  return 1
