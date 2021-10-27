import subprocess
import time

# Encode a single video to VP9 with a fixed constant rate factor.
# This function is hard coded to use two-pass because there's no use case not to.
# For simplicity's sake, the second pass is added in sequence,
#   rather than trying to modify the first pass arg list or something fancy.
def encodeVP9(crf, settings):

  # List of arguments to pass to ffmpeg
  firstPass = ['ffmpeg']
  secondPass = ['ffmpeg']

  # Used to denote scaled resolution in output file
  horizontalLines = "noscale"

  # Check if a CRF value was passed in - this will be used by batch mode.
  if crf == "defaultCRF":
    # Single encode mode uses the CRF from settings.
    # If a value was passed in, that will be used instead.
    crf = settings['CRFDefault']



  # Build first pass
  firstPass.append("-y")
  firstPass.append("-i")
  firstPass.append(settings['InputFileDir']+settings['InputFilename']+settings['InputExtension'])

  if settings['Scale']:
    # These args will be omitted entirely if Scale is false.
    # TODO: make the horizontallines logic more robust, it will fail on 4-digit resolutions.
    horizontalLines = settings['OutResolution'][4:7]
    firstPass.append("-vf")
    firstPass.append("scale="+settings['OutResolution'])
    firstPass.append("-sws_flags")
    firstPass.append(settings['ScaleMode'])
  
  firstPass.append("-c:v")
  firstPass.append("libvpx-vp9")
  firstPass.append("-b:v")
  firstPass.append("0")
  firstPass.append("-crf")
  firstPass.append(crf)
  firstPass.append("-pass")
  firstPass.append("1")
  firstPass.append("-f")
  firstPass.append("webm")

  # TODO: add operating system check so this works on Linux.
  firstPass.append("NUL")


  # Build Second Pass
  secondPass.append("-i")
  secondPass.append(settings['InputFileDir']+settings['InputFilename']+settings['InputExtension'])

  if settings['Scale']:
    secondPass.append("-vf")
    secondPass.append("scale="+settings['OutResolution'])
    secondPass.append("-sws_flags")
    secondPass.append(settings['ScaleMode'])
  
  secondPass.append("-c:v")
  secondPass.append("libvpx-vp9")
  secondPass.append("-b:v")
  secondPass.append("0")
  secondPass.append("-crf")

  # Check if a CRF value was passed in - this will be used by batch mode.
  if crf == "defaultCRF":
    # Single encode mode uses the CRF from settings.
    secondPass.append(settings['CRFDefault'])
  else:
    # Batch mode passes CRF in.
    secondPass.append(crf)
  
  secondPass.append("-pass")
  secondPass.append("2")
  secondPass.append("-c:a")
  secondPass.append("libopus")
  secondPass.append(settings['OutFileDir']+settings['InputFilename']+"_crf"+crf+"_"+horizontalLines+settings['OutputExtension'])
  

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

  return True

  # commandResult = subprocess.run(['ls','-l'], capture_output=True)
  # print(commandResult)