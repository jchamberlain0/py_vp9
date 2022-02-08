import json
import yaml
import pprint
import time
import vp9

# Python 	JSON

# dict 	Object
# list 	Array
# tuple 	Array
# str 	String
# int 	Number
# float 	Number
# True 	true
# False 	false
# None 	null

with open("settings.yaml", 'r') as stream:
    settings = yaml.safe_load(stream)


if settings['Debug']:
  pp = pprint.PrettyPrinter(indent=2)
  print()
  pp.pprint(settings)


result = False
filesEncoded = 0

if settings['Batch']:
  # Batch mode loops over CRF values in the settings and encodes one video for each quality level
  for crf in settings['CRF']:
    time.sleep(1)
    result = vp9.encodeVP9(crf,settings)
    if result == True:
      print('Finished encode for crf '+crf)
      filesEncoded = filesEncoded+1
    if result != True:
      print("\nAn issue was encountered while encoding file with crf "+crf+". Stopping batch mode.")
      break
  # result = True
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