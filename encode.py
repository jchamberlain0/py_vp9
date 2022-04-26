import json
import yaml
import pprint
import time
import vp9
import x264
import os
import shutil
import sys
import png

with open("settings.yaml", 'r') as stream:
  settings = yaml.safe_load(stream)

targetDir = settings['OutFileDir']+settings['NewOutputFolder']


try:
  print('creating output folder '+settings['NewOutputFolder'])
  os.mkdir(targetDir)
except FileExistsError:
  print("Output folder \""+ settings['NewOutputFolder'] +"\" already exists. Please rename output directory to avoid losing work.")
  sys.exit("Exiting")

# shutil.copyfile(os.path.dirname(os.path.realpath('settings.yaml')),settings['OutFileDir']+settings['NewOutputFolder']+"py_vp9.yaml")

# Copy settings to new target dir
shutil.copyfile('settings.yaml',targetDir+'/py_vp9.yaml')

# other method to export settings.. This does not preserve line order, but it does strip comments...
# print(targetDir)
# settingsDump = open(targetDir+'py_vp9.yaml','w')
# yaml.dump(settings,settingsDump)
# settingsDump.close()
# with open()



# settings copy that can be mutated to allow multiple results in single-encode context.
modSettings = settings

if settings['CreateImages']:
  os.mkdir(settings['OutFileDir']+settings['NewOutputFolder']+'/images')
  if png.createPngs(settings):
    print('Saved images.. Maybe.')

if settings['Debug']:
  pp = pprint.PrettyPrinter(indent=2)
  print()
  pp.pprint(settings)


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
      
        # default output resolution means don't scale.
        if OutputResolution == 'default':
          modSettings['Scale'] = False
        else:
          # set the resolution for these encodes.
          modSettings['Scale'] = True
          modSettings['OutResolution'] = OutputResolution 

        for crf in settings['CRF']:
          time.sleep(0.4)

          # Skipping 480p/4:4:4 encodes for now.
          print(OutputResolution)
          print(PixelFormat)
          if (OutputResolution == 'default' and PixelFormat == 'yuv444p' ):
            print('Skipping out on 480p/4:4:4 encode.')
            filesSkipped = filesSkipped + 1
            # continue
          else:
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

# wait for user input. this makes it so the output doesn't
# dissapear immediately when invoking outside the CLI.
input()