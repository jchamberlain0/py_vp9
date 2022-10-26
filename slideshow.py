import subprocess
import time

# Encode a single lossless vp9 video from the unique png file output from the OCR script.
# This can then be used to create another set of quality options in the "perfect video" format.
# ffmpeg -framerate 20 -i %05d.png -pix_fmt yuv444p -c:v libvpx-vp9 -lossless 1 lossless-p.webm
def encodeLossless(settings):




  uniqueDirectory = settings['OutFileDir']+settings['NewOutputFolder']+"/unique/"
  slideshowDirectory = settings['OutFileDir']+settings['NewOutputFolder']+"/ss/"
  outputFile = slideshowDirectory+"lossless.webm"


  # List of arguments to pass to ffmpeg
  slideshow = ['ffmpeg']
  slideshow.append("-y")
  slideshow.append("-framerate")
  slideshow.append("20")
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
  if not settings['SkipEncoding']:
    commandResult = subprocess.run(slideshow, capture_output=True)
  print(commandResult)

  print

  return 1
