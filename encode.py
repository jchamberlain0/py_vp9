import json
import yaml
import pprint
import time
import vp9
import os

# TODO: write another script that strips audio instead of re-encoding a bunch of files in batch mode.


with open("settings.yaml", 'r') as stream:
    settings = yaml.safe_load(stream)

# settings copy that can be mutated to allow multiple results in single-encode context.
# likely unnecessary but is currently saving me a headache
modSettings = settings

if settings['Debug']:
  pp = pprint.PrettyPrinter(indent=2)
  print()
  pp.pprint(settings)


result = False
filesEncoded = 0

if settings['Batch']:
  # Batch mode nests several loops over arrays in settings, and encodes one video for each intersection.
  for Codec in settings['BatchCodecs']:
    
    # Set the codec for these encodes.
    modSettings['OutputCodec'] = Codec

    for OutputResolution in settings['BatchOutputResolutions']:
      
      # default output resolution means don't scale.
      if OutputResolution == 'default':
        modSettings['Scale'] = False
      else:
        # set the resolution for these encodes.
        modSettings['Scale'] = True
        modSettings['OutResolution'] = OutputResolution 

      for crf in settings['CRF']:
        time.sleep(1)
        result = vp9.encodeVP9(crf,modSettings) # Pass in the modified settings.
        if result == True:
          print('Finished encode for crf '+crf)
          filesEncoded = filesEncoded+1
        if result != True:
          print("\nAn issue was encountered while encoding file with crf "+crf+". Stopping batch mode.")
          break
else:
  # Pass a flag to the vp9 encoding function instead of a value
  result = vp9.encodeVP9("defaultCRF",settings)
  filesEncoded = filesEncoded+1


if result == True:
  print('\n\nSuccessfully encoded '+str(filesEncoded)+' file(s).'+' Press Enter to continue...')
else:
  print('\n\nThere was an issue with encoding. Press Enter to continue...')

# wait for user input. this makes it so the output doesn't
# dissapear immediately when invoking by clicking on the script.
input()