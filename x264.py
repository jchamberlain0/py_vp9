import subprocess
import time

# Encode a single video to x264 with fixed settings provided by the colling function.
def encodex264(crf, settings):


  if settings['PixelFormat'] == 'yuv444p':
    print('x264: 4:4:4 chroma unsupported - skipping file')
    return 2
  if settings['Scale']:
    print('x264: Skipping 240p encodes.')
    return 2

  # List of arguments to pass to ffmpeg
  x264 = ['ffmpeg']

  # Used to denote scaled resolution in output file
  horizontalLines = "480"
  if settings['Scale']:
    # These args will be omitted entirely if Scale is false.
    # TODO: make the horizontallines logic more robust, it will fail on 4-digit resolutions.
    horizontalLines = settings['OutResolution'][4:7]

  # Check if a CRF value was passed in - this will be used by batch mode.
  if crf == "defaultCRF":
    # Single encode mode uses the CRF from settings.
    # If a value was passed in, that will be used instead.
    crf = settings['CRFDefault']



  # Build first pass
  x264.append("-y")

  if settings['TrimVideo']:
    if settings['TrimStart']:
      x264.append("-ss")
      x264.append(str(settings['TrimStart']))
    if settings['TrimVideoEnd']:
      x264.append("-to")
      x264.append(str(settings['TrimEnd']))

  x264.append("-i")
  x264.append(settings['InputFileDir']+settings['InputFilename']+settings['InputExtension'])

  if settings['UseDeadline']:
    x264.append("-deadline")
    x264.append(settings['Deadline'])

  if settings['SetPixelFormat']:
    x264.append('-pix_fmt')
    x264.append(settings['PixelFormat'])


  if settings['Scale']:
    x264.append("-vf")
    x264.append("scale="+settings['OutResolution'])
    x264.append("-sws_flags")
    x264.append(settings['ScaleMode'])
  


  x264.append("-c:v")
  x264.append(settings['OutputCodec'])
  # x264.append("-b:v")
  # x264.append("0")

  x264.append("-preset")
  x264.append("slower")

  x264.append("-crf")
  x264.append(crf)
  
  succinctCodec = settings['OutputCodec']
  if settings['OutputCodec'] == 'libvpx-vp9':
    succinctCodec = 'vp9'
  elif settings['OutputCodec'] == 'libx264':
    succinctCodec = 'x264'
  
  succinctPxFmt = '_420'
  if settings['PixelFormat'] == 'yuv444p':
    succinctPxFmt = '_444'
  if settings['PixelFormat'] == 'yuv420p':
    succinctPxFmt = '_420'

  x264.append(settings['OutFileDir']+settings['NewOutputFolder']+"/zgv_n64_"+succinctCodec+"_"+horizontalLines+succinctPxFmt+"_crf"+crf+'.mp4')
  

  commandResult = ''


  t1 = time.localtime()
  # current_time = time.strftime("%H:%M:%S", t)
  # print(current_time)
  print("\nEncoding x264: "+ time.strftime("%H:%M:%S", t1))

  # print(current_time)
  for arg in x264:
    # Print the args without the brackets and commas
    print(arg, end=" ", flush=True)
  if not settings['SkipEncoding']:
    commandResult = subprocess.run(x264, capture_output=True)
  print(commandResult)

  print('x264 finished')

  return 1
