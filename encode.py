import yaml
import pprint
import time
import vp9
import x264
import os
import shutil
import sys
import subprocess
import copy

import png
import ocr
import slideshow

# Source resolution is relevant for the slideshow format,
# in addition to files that are not sourced from pixelFX (minimum 480p)
def getSourceResolution(filePath):
  ffprobe = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=s=x:p=0", filePath]

  # TODO: make this substring work with high res input files.
  # That would only be useful for content released after ~2006
  resolution = str(subprocess.check_output(ffprobe))[2:9]

  # Basic integrity check for the resolution string, quit when invalid.
  if resolution.index('x') == 3 and len(resolution) == 7:
    return resolution
  else:
    sys.exit("Aborting - Invalid resolution retrieved from ffprobe: " + resolution)

def encodeVideoBatch(modSettings,settings):

  sourcePath = settings["InputFileDir"] + settings["InputFilename"] + settings["InputExtension"];
  sourceRes = getSourceResolution(sourcePath)

  result = False
  filesEncoded = 0
  filesSkipped = 0

  if settings['Batch']:
    # Batch mode nests several loops over arrays in settings, and encodes one video for each intersection.
    for Codec in settings['BatchCodecs']:
      
      # Set the codec for these encodes.
      modSettings['OutputCodec'] = Codec

      for OutputResolution in settings['BatchOutputResolutions']:

        for PixelFormat in settings['PixelFormats']:
          modSettings['PixelFormat'] = PixelFormat

          # Update the current output resolution in settings for this batch
          modSettings['OutResolution'] = OutputResolution
          # Set flag for scaling, if the source file is not the same resolution as target
          modSettings["Scale"] = sourceRes != OutputResolution

          for crf in settings['CRF']:
            # time.sleep(0.4)

            # Skipping 480p/4:4:4 encodes for now.
            print(OutputResolution)
            print(PixelFormat)
            result = 0
            if settings['OutputCodec'] == 'libvpx-vp9':
              result = vp9.encodeVP9(crf, modSettings) # Pass in the modified settings.
            elif settings['OutputCodec'] == 'libx264':
              result = x264.encodex264(crf, modSettings) # Pass in the modified settings.
            if result == 1:
              print('Finished '+ Codec +' encode for crf '+crf)
              filesEncoded = filesEncoded+1
            elif result == 2:
              print('Skipped over '+ Codec +' encode for crf '+crf)
              filesSkipped = filesSkipped+1
            else:
              print("\nAn issue was encountered while encoding file with crf "+crf+". Stopping batch mode.")
              break
  else:
    # Pass a flag to the vp9 encoding function instead of a value
    result = vp9.encodeVP9("defaultCRF",settings)
    filesEncoded = filesEncoded+1


  if result == True:
    print('\n\nEncoded '+str(filesEncoded)+' files. Skipped '+str(filesSkipped)+'.'+' Press Enter to continue...')
  else:
    print('\n\nThere was an issue with encoding. Press Enter to continue...')

  return True



def main():  
  startTime = time.time()

  with open("settings.yaml", 'r') as stream:
    settings = yaml.safe_load(stream)

  # TODO: check if the source file exists and quit if not.

  wantedDir = settings['NewOutputFolder']
  newDir = wantedDir

  folderCount = 1
  
  while os.path.exists(settings["OutFileDir"] + newDir):
    newDir = wantedDir + "-" + str(folderCount)
    folderCount += 1

  settings["NewOutputFolder"] = newDir
  finalDir = settings["OutFileDir"]+settings["NewOutputFolder"]

  try:
    print('creating output folder '+settings['NewOutputFolder'])
    os.mkdir(finalDir)
  except FileExistsError:
    # TODO: add a sequential digit to the output folder instead of quitting.
    print("Output folder \""+ settings['NewOutputFolder'] +"\" already exists.\nPlease rename output directory to avoid losing work.")
    sys.exit("Exiting")

  # shutil.copyfile(os.path.dirname(os.path.realpath('settings.yaml')),settings['OutFileDir']+settings['NewOutputFolder']+"py_vp9.yaml")

  # Copy settings to new new directory
  shutil.copyfile('settings.yaml',finalDir+'/py_vp9.yaml')

  os.startfile(finalDir)

  # other method to export settings.. This does not preserve line order, but it does strip comments...
  # print(targetDir)
  # settingsDump = open(targetDir+'py_vp9.yaml','w')
  # yaml.dump(settings,settingsDump)
  # settingsDump.close()
  # with open()

  # settings copy that can be mutated to allow multiple results in single-encode context.
  modSettings = settings
  # deep copy isn't working for some reason.
  # modSettings = copy.deepcopy(settings)

  if settings['CreateImages']:
    os.mkdir(settings['OutFileDir']+settings['NewOutputFolder']+'/images')
    if png.createPngs(settings):
      print('Saved images.')
    if png.createMontages(settings):
      print('saved montages.')
    if settings['RunOCR']:
      # Run adjacent ocr script to remove duplicate frames from the video.
      os.mkdir(settings['OutFileDir']+settings['NewOutputFolder']+'/unique')
      os.mkdir(settings['OutFileDir']+settings['NewOutputFolder']+'/ss')
      os.mkdir(settings['OutFileDir']+settings['NewOutputFolder']+'/jpg')
      if ocr.readFolderInputs(settings['OutFileDir']+settings['NewOutputFolder']+'/images/*', settings['OutFileDir']+settings['NewOutputFolder']+'/unique/'):
        print('saved unique files.')
        # TODO: add a case here where the slideshow is still encoded from a sequence that was not deduped.
        if settings["EncodeSlideshow"]:
          slideshow.encodeLossless(modSettings)
        if png.createUniqueJPGs(settings['OutFileDir']+settings['NewOutputFolder']+'/unique/',settings['OutFileDir']+settings['NewOutputFolder']+'/jpg/'):
          print('saved unique jpgs.')

  if settings['Debug']:
    pp = pprint.PrettyPrinter(indent=2)
    print()
    pp.pprint(settings)

  # Encode quality options for traditional video
  encodeVideoBatch(modSettings,settings)


  if settings["RunOCR"] and settings["EncodeSlideshow"]:
    # Modify the settings further and
    # Create a new batch based on the /ss/lossless.webm file.

    modSettings["InputExtension"] = ".webm"
    modSettings["OutputExtension"] = ".webm"
    modSettings["InputFilename"] = "lossless"
    modSettings["InputFileDir"] = modSettings["OutFileDir"] + modSettings["NewOutputFolder"]+ "/ss/"
    modSettings["NewOutputFolder"] = modSettings["NewOutputFolder"] + "/ss/"
    modSettings["StripAudio"] = True
    modSettings["TrimVideo"] = False
    modSettings["TrimVideoEnd"] = False

    # Encode Slideshow videos
    encodeVideoBatch(modSettings,settings)

  print("--- %s minutes ---" % ((time.time() - startTime) / 60 ))

  # wait for user input. this makes it so the output doesn't
  # dissapear immediately when invoking outside the CLI.
  # input()

if __name__ == "__main__":
   main()