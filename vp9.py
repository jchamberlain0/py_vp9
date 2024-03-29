import subprocess
import time

# Encode a single video to VP9 with fixed settings provided by the colling function.
# This function is hard coded to use two-pass because there's no use case not to.
# For simplicity's sake, the second pass is added in sequence,
#   rather than trying to modify the first pass arg list or something fancy like that.
def encodeVP9(crf, settings):

  if (settings['OutResolution'] == '640x480' and settings['PixelFormat'] == 'yuv444p' ):
    print('vp9: Skipping out on 480p/4:4:4 encode.')
    return 2
  
  # List of arguments to pass to ffmpeg
  firstPass = ['ffmpeg']
  secondPass = ['ffmpeg']

  # Get the number after the x for filename and optional scaling.
  resString = settings['OutResolution']
  charX = resString.index('x')
  horizontalLines = resString[charX+1:len(resString)]

  # Check if a CRF value was passed in - this will be used by batch mode.
  if crf == "defaultCRF":
    # Single encode mode uses the CRF from settings.
    # If a value was passed in, that will be used instead.
    crf = settings['CRFDefault']



  # Build first pass
  firstPass.append("-y")

  if settings['TrimVideo']:
    if settings['TrimStart']:
      firstPass.append("-ss")
      firstPass.append(str(settings['TrimStart']))
    if settings['TrimVideoEnd']:
      firstPass.append("-to")
      firstPass.append(str(settings['TrimEnd']))

  firstPass.append("-i")
  firstPass.append(settings['InputFileDir']+settings['InputFilename']+settings['InputExtension'])

  if settings['UseDeadline']:
    firstPass.append("-deadline")
    firstPass.append(settings['Deadline'])

  if settings['SetPixelFormat']:
    firstPass.append('-pix_fmt')
    firstPass.append(settings['PixelFormat'])


  if settings['Scale']:
    firstPass.append("-vf")
    firstPass.append("scale="+settings['OutResolution'])
    firstPass.append("-sws_flags")
    firstPass.append(settings['ScaleMode'])
  


  firstPass.append("-c:v")
  # firstPass.append("libvpx-vp9")
  firstPass.append(settings['OutputCodec'])
  firstPass.append("-b:v")
  firstPass.append("0")
  firstPass.append("-crf")
  firstPass.append(crf)

  # firstPass.append('-profile:v')
  # firstPass.append('1')

  firstPass.append("-pass")
  firstPass.append("1")
  firstPass.append("-f")
  firstPass.append("webm")

  # TODO: add operating system check so this works on Linux.
  firstPass.append("NUL")
  # firstPass.append("temp/t")
  # firstPass.append("temp")


  if settings['TrimVideo']:
    if settings['TrimStart']:
      secondPass.append("-ss")
      secondPass.append(str(settings['TrimStart']))
    if settings['TrimVideoEnd']:
      secondPass.append("-to")
      secondPass.append(str(settings['TrimEnd']))

  # Build Second Pass
  secondPass.append("-i")
  secondPass.append(settings['InputFileDir']+settings['InputFilename']+settings['InputExtension'])

  if settings['UseDeadline']:
    secondPass.append("-deadline")
    secondPass.append(settings['Deadline'])
  

  if settings['SetPixelFormat']:
    secondPass.append('-pix_fmt')
    secondPass.append(settings['PixelFormat'])
  

  if settings['Scale']:
    secondPass.append("-vf")
    secondPass.append("scale="+settings['OutResolution'])
    secondPass.append("-sws_flags")
    secondPass.append(settings['ScaleMode'])
  
  secondPass.append("-c:v")
  secondPass.append(settings['OutputCodec'])
  secondPass.append("-b:v")
  secondPass.append("0")
  secondPass.append("-crf")

  # Check if a CRF value was passed in - this will be used by batch mode.
  # TODO: this block is redundant!!
  if crf == "defaultCRF":
    # Single encode mode uses the CRF from settings.
    secondPass.append(settings['CRFDefault'])
  else:
    # Batch mode passes CRF in.
    secondPass.append(crf)
  
  # secondPass.append('-profile:v')
  # secondPass.append('1')
  
  secondPass.append("-pass")
  secondPass.append("2")
  secondPass.append("-c:a")
  secondPass.append("libopus")
  # secondPass.append("-acodec")
  # secondPass.append("copy")

  if settings['StripAudio']:
    secondPass.append("-an")
  # secondPass.append(settings['OutFileDir']+settings['NewOutputFolder']+"/"+settings['InputFilename']+"_"+settings['OutputCodec']+"_crf"+crf+"_"+horizontalLines+settings['OutputExtension'])

  
  succinctCodec = settings['OutputCodec']
  if settings['OutputCodec'] == 'libvpx-vp9':
    succinctCodec = 'vp9'
  
  succinctPxFmt = '_420'
  if settings['PixelFormat'] == 'yuv444p':
    succinctPxFmt = '_444'
  if settings['PixelFormat'] == 'yuv420p':
    succinctPxFmt = '_420'


  secondPass.append(settings['OutFileDir']+settings['NewOutputFolder']+"/zgv_n64_"+succinctCodec+"_"+horizontalLines+succinctPxFmt+"_crf"+crf+settings['OutputExtension'])
  

  commandResult = ''


  t1 = time.localtime()
  # current_time = time.strftime("%H:%M:%S", t)
  # print(current_time)
  print("\nRunning first pass: "+ time.strftime("%H:%M:%S", t1))

  # print(current_time)
  for arg in firstPass:
    # Print the args without the brackets and commas
    print(arg, end=" ", flush=True)
  if not settings['SkipEncoding']:
    commandResult = subprocess.run(firstPass, capture_output=True)
  print(commandResult)

  t2 = time.localtime()
  # current_time = time.strftime("%H:%M:%S", t2)
  print("\nRunning second pass. "+ time.strftime("%H:%M:%S", t2))
  # print(current_time)
  # Print the command as it would normally read, without brackets and commas
  for arg in secondPass:
    print(arg, end=" ", flush=True)
  if not settings['SkipEncoding']:
    commandResult = subprocess.run(secondPass, capture_output=True)
  print(commandResult)

  print

  return 1
