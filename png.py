import subprocess
import time
import glob

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

def createPngs(settings):
  # Output a png file for every frame in the source video.

  command = ['ffmpeg','-i']

  command.append(settings['InputFileDir']+settings['InputFilename']+settings['InputExtension'])
  command.append('-vf')
  command.append('fps=60')
  # command.append('-vf')
  # command.append('format=gray')

  command.append('-vf')
  command.append('scale=320x240')
  command.append('-sws_flags')
  command.append('neighbor')
  command.append(settings['OutFileDir']+settings['NewOutputFolder']+'/images/'+'zgv%04d.png')

  for arg in command:
    # Print the args without the brackets and commas
    print(arg, end=" ", flush=True)

  if settings['SkipImages']:
    return True
  
  t1 = time.localtime()
  print("\nRunning jpeg extraction: "+ time.strftime("%H:%M:%S", t1))

  commandResult = subprocess.run(command, capture_output=True)
  print(commandResult)

  return True

def createMontage(settings,imageOffset,gridWidth):

  # Take the number of output images, divide by X+1
  # find a screenshot corresponding to a multiple of X
  # Create a montage using those images
  # given a folder of 3000 images, and x=12, you would divide that by 13 and gather images at 1(3000/13), 2(3000/13), 3(3000x13), etc.

  divisor = imageOffset + 1

  # files = glob.glob("C:/video/lostwoods-megaflip480/images/crop")
  files = glob.glob(settings['OutFileDir']+settings['NewOutputFolder']+'/images/*')
  command = ['magick','montage']

  # // is the "floor" divisor

  # get an array of values
  frequency = len(files)//divisor
  images = []

  for i in range(imageOffset):
    images.append((i*frequency)+frequency)

  # print(f)
  print(frequency)
  print(images)
  # return False


  # for i in range(len(files)):
  #   command.append(files[i])

  for i in range(len(images)):
    command.append(files[images[i]])


  command.append('-geometry')
  command.append('+0+0')
  command.append('-tile')
  # command.append('2x')
  command.append(str(gridWidth)+'x')

  command.append(settings['OutFileDir']+settings['NewOutputFolder']+'/montage'+str(gridWidth)+'.png')

  # montage zgv0392.png zgv0394.png zgv0397.png zgv0400.png zgv0403.png zgv0405.png zgv0408.png zgv0411.png zgv0415.png zgv0418.png zgv0422.png zgv0424.png -geometry +0+0 montage_geom2.png



  # for arg in command:
  #   # Print the args without the brackets and commas
  #   print(arg, end=" ", flush=True)


  t1 = time.localtime()
  print("\nMaking montage...: "+ time.strftime("%H:%M:%S", t1))

  print(command)

  commandResult = subprocess.run(command, capture_output=True)
  print(commandResult)

  return True

def createMontages(settings):

  imageOffsets = [4,12,108]
  gridWidths = [2,4,12]

  for i in range(len(imageOffsets)):
    createMontage(settings,imageOffsets[i],gridWidths[i])