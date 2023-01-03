# Imports
import time # Sleeping
import os # Running Batch Commands
import getpass # Password
import winsound # Windows Sounds
import json # Reading JSON Files
# Classes
class tColors: # Text Colors
    ACCEPTED = '\033[92m' # Green
    WARNING = '\033[93m' # Yellow
    ERR = '\033[91m' # Red
    DEFAULT = '\033[0m' # White
    DEBUG = '\033[0;35m' # Purple
def main():
    # Variables
    loggedOut = True
    config = json.load(open('config.json'))
    username = ""
    changed = False
    # Defines
    def alert(type=-1, msg="N/A"):
        if type == 1: # Success Alert
            print(f"{tColors.ACCEPTED}SUCCESS: " + msg + f"{tColors.DEFAULT}")
        elif type == 0: # Warning Alert
            print(f"{tColors.WARNING}WARNING: " + msg + f"{tColors.DEFAULT}")
        elif type == -1:
            print(f"{tColors.WARNING}ALERT: " + msg + f"{tColors.DEFAULT}")
        else: # Error/Unknown Alert
            print(f"{tColors.ERR}ERR: " + msg + f"{tColors.DEFAULT}")
        msgBeep(type)
    
    def msgBeep(type):
        if type == 1: # Success Beep
            winsound.Beep(1000, 300)
        elif type == 0 or -1: # Warning Beep
            winsound.Beep(1000, 200)
            winsound.Beep(300, 150)
        else: # Error/Unknown Beep
            winsound.Beep(300, 300)

    def cls(vers=0): # Simple Screen Clear
        print(f"{tColors.DEBUG}~ !Screen Clear! ~{tColors.DEFAULT}")
        os.system('cls' if os.name=='nt' else 'clear')
        if vers == 0:
            if loggedOut == False and config['loginSys']:
                print("Welcome, " + username + "!\n")
            print(config['name'])
            if config['copyright']:
                print(config['copyrightTxt'])

    def shutdownApp(): # Exit App
        cls(1)
        print(f"{tColors.WARNING}Shutting Down...{tColors.DEFAULT}")
        winsound.Beep(500,600)
        cls(1)
        exit()

    def loginCheck():
        if changed == True:
            cls()
            print("   Type 'HELP' for a list of commands!")

    def login(loggedOutState): # Login System
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
                os.path.normpath(os.getcwd() + os.sep + os.pardir) # Go back a directory (thank you https://stackoverflow.com/a/17726833)
                usr = input("Username: ")
                try:
                    user = json.load(open("./users/" + usr + "/user.json", "r"))
                except:
                    alert(-2, "Invalid Username.")
                    continue
                else:

                    password = user["Password"]

                    pas = getpass.getpass()

                    alert(-1, "Checking...")
                    time.sleep(1.0)

                    if pas == password:
                        alert(-1, "Logging in...")
                        time.sleep(1.0)
                        alert(1, "Login Accepted.")
                        loggedOutState = False
                    else:
                        alert(-2, "Invalid Password.")
                        continue
            else:
                usr = input("Username: ")
                pas = getpass.getpass()

                alert(-1, "Logging in...")
                time.sleep(1.0)
                alert(1, "Login Accepted.")
                loggedOutState = False
                continue
            return loggedOutState, usr, True

    # Main Program
    os.system("title LOADING...")
    print(f"{tColors.WARNING}Loading!{tColors.DEFAULT}")
    time.sleep(1.0)
    os.system("title " + config['name'])
    cls()
    winsound.Beep(500,600)
    if config['loginSys']:
        loggedOut, username, changed = login(loggedOut)
    else:
        loggedOut = False
    loginCheck()

        # Command System
    while not loggedOut:
        cmd = input("> ") # Get command and arguments
        args = cmd.split(" ") # Split the command and different arguments
        cmd = cmd.lower() # Convert to lowercase
        cmd = args[0] # Make sure it only checks the command, not the arguments
        del args[0] # Remove command from arguments
        if args == []: # Make sure args isn't nothing
            args.append("") # If it is, make it an empty string
        
        #print(f"{tColors.DEBUG}DEBUG: COMMAND: " + cmd) # Debug arguments
        #print("DEBUG: ARGUMENTS: " + str(args) + f'{tColors.DEFAULT}') # Debug arguments
        match cmd.lower():
            case "cls": # Clear
                cls(1)
            case "clear":
                cls(1)
            case "restart": # Restart App
                cmd = input(f"{tColors.ERR}Are you sure? (Y/N) {tColors.DEFAULT}").lower()
                if cmd == "y":
                    main()
                else:
                    print(f"{tColors.WARNING}Restart Canceled.{tColors.DEFAULT}")
            case "exit": # Exit the application
                if args[0].lower() == '-y':
                    shutdownApp()
                else:
                    cmd = input(f"{tColors.ERR}Are you sure? (Y/N) {tColors.DEFAULT}").lower()
                    if cmd == "y":
                        shutdownApp()
                    else:
                        print(f"{tColors.WARNING}Shutdown Canceled.{tColors.DEFAULT}")
            case "logout":
                if config['loginSys']:
                    loggedOut, username, changed = login(loggedOut)
                    loginCheck()
                else:
                    print(f"{tColors.ERR}ERR: Unkown Command 'LOGOUT'{tColors.DEFAULT}")
            case "help": # Display Commands
                print("List of Commands:")
                print("   ~ System ~")
                if config['loginSys']:
                    print("   LOGOUT        : Logs out of current account.")
                print("   EXIT          : Closes app.")
                print("   RESTART       : Restarts app.")
                print("   ~ Screen ~")
                print("   CLS/CLEAR     : Clears the screen.")
                print("   ECHO          : Echos what you put back into the console.")
            case "echo":
                print(' '.join(args))
            case _: # Default
                if cmd != "":
                    print(f"{tColors.ERR}ERR: Unkown Command '" + cmd.upper() + f"'{tColors.DEFAULT}")

main() # Start the app
# This worked better than expected, I'm honestly kinda surprised!
# This is also my first semi-big project that I put a lot of effort in, I'd love any constructive criticism.
# Well, that's it for me. See you later, love you all! ♥
