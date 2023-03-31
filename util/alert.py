from util.tColors import tColors # Get tColors Class
import json # Reading JSON Files
import os # Running Batch Commands
os.path.normpath(os.getcwd() + os.sep + os.pardir) # Go back a directory (thank you https://stackoverflow.com/a/17726833)
config = json.load(open('config.json'))
if config["sounds"]:
  import winsound # Windows Sounds

def alert(type=-1, msg="N/A", sound=False, prefix=True):
  if prefix:
    if type == 1: # Success Alert
      print(f"{tColors.ACCEPTED}SUCCESS: " + msg + f"{tColors.DEFAULT}")
    elif type == 0: # Warning Alert
      print(f"{tColors.WARNING}WARNING: " + msg + f"{tColors.DEFAULT}")
    elif type == -1:
      print(f"{tColors.WARNING}ALERT: " + msg + f"{tColors.DEFAULT}")
    else: # Error/Unknown Alert
        print(f"{tColors.ERR}ERR: " + msg + f"{tColors.DEFAULT}")
  else: # Before, I was using prints. With this, I don't need to
    if type == 1: # Success Alert
      print(f"{tColors.ACCEPTED}" + msg + f"{tColors.DEFAULT}")
    elif type == (0 or -1): # Warning Alert
      print(f"{tColors.WARNING}" + msg + f"{tColors.DEFAULT}")
    else: # Error/Unknown Alert
      print(f"{tColors.ERR}" + msg + f"{tColors.DEFAULT}")
  if config["sounds"] and sound:
    msgBeep(type)

def msgBeep(type):
  if type == 1: # Success Beep
    winsound.Beep(1000, 300)
  elif type == 0 or -1: # Warning Beep
    winsound.Beep(1000, 200)
    winsound.Beep(300, 150)
  else: # Error/Unknown Beep
    winsound.Beep(300, 300)