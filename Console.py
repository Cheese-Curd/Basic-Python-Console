# Imports
import time  # Sleeping
import os  # Running Batch Commands
import getpass  # Password
import json  # Reading JSON Files

from datetime import date # Get date

from util.alert import alert  # Alerts
from util.tColors import tColors  # Import Colors
config = json.load(open('config.json')) # Config
if config["sounds"]:
  import winsound # Windows Sounds

def sleepCheck(Time):
  if config["sleeps"]:
    time.sleep(Time)

def main():
    # Variables
    loggedOut = True
    config = json.load(open('config.json'))
    username = ""
    changed = False
    # Defines

    def cls(vers=0):  # Simple Screen Clear
        print(f"{tColors.DEBUG}~ !Screen Clear! ~{tColors.DEFAULT}")
        os.system('cls' if os.name == 'nt' else 'clear')
        if vers == 0:
            if loggedOut == False and config['loginSys']:
                print(f"Welcome, {username}!\n")
            if config["showVer"]:
                print(f"{config['name']} Version: {config['version']}")
            else:
                print(config["name"])
            if config['copyright']:
                print(config['copyrightTxt'])

    def shutdownApp():  # Exit App
        cls(1)
        alert(0, "Shutting Down...", False, False)
        if config["sounds"]:
            winsound.Beep(500, 600)
        cls(1)
        exit()

    def loginCheck():
        if changed == True:
            cls()
            print("   Type 'HELP' for a list of commands!")

    def login(loggedOutState):  # Login System
        while True:
            if loggedOutState == False:
                if input(f"{tColors.ERR}Are you sure? (Y/N) {tColors.DEFAULT}").lower() == 'y':
                    loggedOutState = True
                    break
                else:
                    alert(-1, "Logout Canceled.")
                    return loggedOutState, username, False
            else:
                break
        while loggedOutState:
            if config['userSys']:
                # Go back a directory (thank you https://stackoverflow.com/a/17726833)
                os.path.normpath(os.getcwd() + os.sep + os.pardir)
                usr = input("Username: ")
                try:
                    user = json.load(
                        open("./users/" + usr + "/user.json", "r"))
                except:
                    alert(-2, "Invalid Username.")
                    continue
                else:

                    password = user["Password"]

                    pas = getpass.getpass()

                    alert(-1, "Checking...")
                    sleepCheck(1.0)

                    if pas == password:
                        alert(-1, "Logging in...")
                        sleepCheck(1.0)
                        alert(1, "Login Accepted.")
                        loggedOutState = False
                    else:
                        alert(-2, "Invalid Password.")
                        continue
            else:
                usr = input("Username: ")
                pas = getpass.getpass()

                alert(-1, "Logging in...")
                sleepCheck(1.0)
                alert(1, "Login Accepted.")
                loggedOutState = False
                continue
            return loggedOutState, usr, True

    # Main Program
    os.system("title LOADING...")
    alert(0, "Loading!", False, False)
    sleepCheck(1.0)
    os.system("title " + config['name'])
    cls()
    if config["sounds"]:
        winsound.Beep(500, 600)
    if config['loginSys']:
        loggedOut, username, changed = login(loggedOut)
    else:
        loggedOut = False
    loginCheck()

    # Command System
    while not loggedOut:
        cmd = input(f"{config['prefix']} ")  # Get command and arguments
        args = cmd.split(" ")  # Split the command and different arguments
        cmd = cmd.lower()  # Convert to lowercase
        # Make sure it only checks the command, not the arguments
        cmd = args[0]
        del args[0]  # Remove command from arguments
        if args == []:  # Make sure args isn't nothing
            args.append("")  # If it is, make it an empty string

        # print(f"{tColors.DEBUG}DEBUG: COMMAND: " + cmd) # Debug arguments
        # print("DEBUG: ARGUMENTS: " + str(args) + f'{tColors.DEFAULT}') # Debug arguments
        match cmd.lower():
            case "cls":  # Clear
                cls(1)
            case "clear":
                cls(1)
            case "restart":  # Restart App
                cmd = input(
                    f"{tColors.ERR}Are you sure? (Y/N) {tColors.DEFAULT}").lower()
                if cmd == "y":
                    main()
                else:
                    alert(2, "Restart Canceled.", False, False)
            case "exit":  # Exit the application
                if args[0].lower() == '-y':
                    shutdownApp()
                else:
                    cmd = input(
                        f"{tColors.ERR}Are you sure? (Y/N) {tColors.DEFAULT}").lower()
                    if cmd == "y":
                        shutdownApp()
                    else:
                        alert(0, "Shutdown Canceled.", False, False)
            case "logout":
                if config['loginSys']:
                    loggedOut, username, changed = login(loggedOut)
                    loginCheck()
                else:
                    alert(-2, "Unkown Command 'LOGOUT'")
            case "help":  # Display Commands
                print("List of Commands:")
                print("   ~ System ~")
                if config['loginSys']:
                    print("   LOGOUT        : Logs out of current account.")
                print("   EXIT          : Closes app.")
                print("   RESTART       : Restarts app.")
                print("   DATE          : Shows current date.")
                print("   ~ Screen ~")
                print("   CLS/CLEAR     : Clears the screen.")
                print("   ECHO          : Echos what you put back into the console.")
                print("   ~ Other ~")
                if config["changelog"]:
                  print("   CHANGELOG     : Shows the latest change log.")
                if config["license"]:
                  print("   LICENSE     : Shows the copyright license.")
            case "echo":
                print(' '.join(args))
            case "date":
              Date = date.today().strftime("%a %D")
              print(f"The current date is: {Date}")
            case "changelog":
              if config["changelog"]:
                if args[0] == "":
                  args[0] = config["version"]
                try:
                  log = open(f'changelogs/{args[0]}.txt', 'r')
                except:
                  print(f"Could not find changelog for version {args[0]}, try {config['version']}.")
                else:
                  print(f"UPDATE {args[0]}")
                  print(log.read())
              else:
                alert(-2, "Unkown Command 'CHANGELOG'")
            case "license":
                if config['license']:
                    if input("Are you sure? (Y/N) ").lower() == "y":
                      print(open('LICENSE', 'r').read())
                    else:
                      alert(0, "Canceled.", False, False)
                else:
                    alert(-2, "Unkown Command 'LICENSE'")
            case _:  # Default
                if cmd != "":
                    alert(-2, "Unknown Command '" + cmd + "'")


if __name__ == "__main__":  # Make sure this is running itself
  main()  # Start the app
# This worked better than expected, I'm honestly kinda surprised!
# This is also my first semi-big project that I put a lot of effort in, I'd love any constructive criticism.
# Well, that's it for me. See you later, love you all! ♥
