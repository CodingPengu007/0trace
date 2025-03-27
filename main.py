#################################################################################
# WELCOME TO 0trace
#################################################################################

import os
import sys
import time

import Otrace.sys.file_mngr as file_mngr
import Otrace.sys.venv_mngr as venv_mngr

#################################################################################
try:
    
    os.system("cls" if os.name == "nt" else "clear")
    skip_warning = False
    if file_mngr.check(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Otrace", "cache", "warning")):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Otrace", "cache", "warning"), "r") as file:
            skip_warning = bool(file.read(1) == "n")

    if skip_warning == True:
        print("--- Welcome to 0trace ---")
        print("")
        print("The program is automatically starting up and skipping the routine warning.")
        print("")
    else:
        print("--- Welcome to 0trace ---")
        print("")
        print("The program is about to start up,")
        print("please don't interrupt the process.")
        print("")
        answer = input("Should we warn you again next time? (y/n): ")
        if answer.lower() == "y":
            print("")
            print("(*) Warning enabled.")
            print("")
        if answer.lower() == "n":
            try:
                with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Otrace", "cache", "warning"), "w") as file:
                    file.write("n")
                print("")
                print("(*) Warning disabled.")
                print("")
            except FileNotFoundError:
                print("")
                print("(!) Warning not disabled. Error writing to cache.")
                print("(!) cache will get repaired during startup")
                print("")
                print("(*) Warning enabled by default.")
                print("")
                input("Press Enter to continue...")
        else:
            print("")
            print("(!) Invalid input. Warning enabled by default.")
            print("(*) Warning enabled.")
            print("")
            input("Press Enter to continue...")

    os.system("cls" if os.name == "nt" else "clear")
    print("Starting up...")
    print("")

    version = "0.01"
    author = "CodingPengu007"
    program = "0trace"
    publicity = "Closed Early Alpha"

    main_dir = os.path.dirname(os.path.abspath(__file__))
    venv_dir = os.path.join(main_dir, 'Otrace_venv')

    ### Virtual Environment Check ###
    print("")
    print("Checking virtual environment:")
    venv_exists = None
    if not venv_mngr.check(venv_dir):
        venv_exists = False
        print("(!) Virtual environment not found. (This is normal when starting for the first time)")
        print("")
        print("--------------------------------------------------------------------------------------")
        print("This is the first time you are running this program, thanks for that!")
        print("But please be aware that the first time will take a little bit longer than usual. :)")
        print("So please wait while the virtual environment is set up:")
        print("--------------------------------------------------------------------------------------")
        print("")
        print("Setting up virtual environment...")
        venv_mngr.setup(main_dir, venv_dir)
        print("Virtual environment setup complete.")
        venv_mngr.activate(venv_dir)
        print("Virtual environment activated.")
    else:
        venv_exists = True
        print("Virtual environment found.")
        print("Activating virtual environment...")
        venv_mngr.activate(venv_dir)
        print("Virtual environment activated.")
    print("")
    ### ------------------------ ###
    
    import Otrace as game

    ### Check for the cache directory ###
    print("")
    print("Checking for cache directory:")
    if not game.sys.file_mngr.check(os.path.join(main_dir, "Otrace", "cache")):
        print("(!) Cache directory not found.")
        print("Creating cache directory...")
        os.mkdir(os.path.join(main_dir, "Otrace", "cache"))
        print("Cache directory created.")
    else:
        print("Cache directory found.")
    print("")
    ### ------------------------ ###

    ### Remove __pycache__ directories ###
    if venv_exists == True:
        print("")
        print("Removing __pycache__ directories:")
        print("")
        game.sys.file_mngr.remove_pycache(main_dir)
        print("")
        print("Removed __pycache__ directories.")
        print("")
    ### ------------------------ ###

    ### Check if a hostname exists ###
    print("")
    print("Checking for hostname:")
    if game.sys.file_mngr.empty(os.path.join(main_dir, "Otrace", "local", "etc", "hostname")):
        print("(!) Hostname not found.")
        print("Starting hostname creation...")
        game.sys.accnt_mngr.create_hostname(main_dir)
        print("Hostname created successfully.")
    else:
        print("Hostname found.")
    print("")
    ### ------------------------ ###

    ### Check if an account exists ###
    print("")
    print("Checking for accounts:")
    if game.sys.accnt_mngr.check(main_dir):
        print("Account(s) found.")
    else:
        print("(!) No account found.")
        print("")
        print("Starting account creation...")
        game.sys.accnt_mngr.signup(main_dir)
        print("Account created successfully.")
    print("")
    ### ------------------------ ###

    ### Check for account directories directory ###
    print("")
    print("Checking for account directories:")
    username_file_path = os.path.join(main_dir, "Otrace", "local", "etc", "passwd")
    with open(username_file_path, "r") as user_file:
        usernames = [line.strip() for line in user_file.readlines()]
    for users in usernames:
        if not game.sys.file_mngr.check(os.path.join(main_dir, "Otrace", "local", "home", users)):
            print(f"(!) Directory for {users} not found.")
            print("Creating directory...")
            os.mkdir(os.path.join(main_dir, "Otrace", "local", "home", users))
            print("Directory created.")
        else:
            print(f"Directory for {users} found.")
    print("")
    ### ------------------------------------- ###

    ### Load account information ###
    print("")
    print("Loading account information:")
    print("(?) Login / Sign Up ...")
    print("")
    os.system("cls" if os.name == "nt" else "clear")
    if game.sys.accnt_mngr.login_or_signup() == "login":
        os.system("cls" if os.name == "nt" else "clear")
        print("Starting login...")
        print("Loading username...")
        os.system("cls" if os.name == "nt" else "clear")
        username = game.sys.accnt_mngr.login(main_dir)
        os.system("cls" if os.name == "nt" else "clear")
        print("Username loaded.")
        print("Login successful.")
    else:
        os.system("cls" if os.name == "nt" else "clear")
        print("Starting sign up...")
        os.system("cls" if os.name == "nt" else "clear")
        game.sys.accnt_mngr.signup(main_dir)
        os.system("cls" if os.name == "nt" else "clear")
        print("Sign up successful.")
        
        print("Starting login...")
        print("Loading username...")
        os.system("cls" if os.name == "nt" else "clear")
        username = game.sys.accnt_mngr.login(main_dir)
        os.system("cls" if os.name == "nt" else "clear")
        print("Username loaded.")
        print("Login successful.")
        
    print("Loading hostname...")
    hostname = game.sys.accnt_mngr.load_hostname(main_dir)
    print("Hostname loaded.")
    print("Loading local directory...")
    local_dir = main_dir + "/Otrace/local"
    print("Local directory loaded.")
    print("Loading current directory...")
    current_dir = f"{local_dir}/home/{username}"
    print("Current directory loaded.")
    print("")
    ### ------------------------ ###

    print("")

except KeyboardInterrupt:
    print("Exiting...")
    game.sys.venv_mngr.deactivate(venv_dir)
    os.system("cls" if os.name == "nt" else "clear")
    sys.exit(0)
except Exception as e:
    print("The Startup of 0trace failed.")
    print("")
    print("Error report:")
    print("----------------------------")
    print(f"ERROR: {e}")
    print("----------------------------")
    print("")
    print("")
    print("(!) Please report this issue to the developer.")
    print("")
    print("--> You can reach out to the dev on Github:")
    print("--> https://github.com/CodingPengu007")
    print("")
    print("")
    input("Press Enter to exit...")
    os.system("cls" if os.name == "nt" else "clear")
    game.sys.venv_mngr.deactivate(venv_dir)
    sys.exit(1)

print("Startup complete.")
os.system("cls" if os.name == "nt" else "clear")

print(f"Welcome to {program}!")
print("")
print(f"Version: {version}")
print(f"Author: {author}")
print(f"Publicity: {publicity}")
print("")

os.system("cls" if os.name == "nt" else "clear")

#################################################################################

try:
    game.prgms.cmd.line(username, hostname, current_dir, local_dir)
except KeyboardInterrupt:
    print("Exiting...")
    game.sys.venv_mngr.deactivate(venv_dir)
    os.system("cls" if os.name == "nt" else "clear")
    sys.exit(0)
except Exception as e:
    print(f"An error occurred: {e}")
    game.sys.venv_mngr.deactivate(venv_dir)
    
#################################################################################