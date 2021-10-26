import json
import yaml
import pprint
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

# with open('settings.json') as settings_file:
#   settings = json.load(settings_file)

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
    result = vp9.encodeVP9(crf,settings)
    filesEncoded = filesEncoded+1
    if result != True:
      print("\nAn issue was detected while encoding file with crf "+crf+". Stopping batch mode.")
      break
  result = True
else:
  result = vp9.encodeVP9("defaultCRF",settings)
  filesEncoded = filesEncoded+1


if result == True:
  print('\n\nSuccessfully encoded '+str(filesEncoded)+' file(s).'+' Exiting...')
else:
  print('\n\nThere was an issue with encoding. Exiting...')

input()