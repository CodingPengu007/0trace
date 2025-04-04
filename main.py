#################################################################################
# WELCOME TO 0trace
#################################################################################

import os
import sys
import subprocess

import Otrace.sys.file_mngr as file_mngr

#################################################################################
try:
    
    os.system("cls" if os.name == "nt" else "clear")
    skip_warning = False
    if file_mngr.check(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Otrace", "cache", "warning")):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Otrace", "cache", "warning"), "r") as file:
            skip_warning = bool(file.read(1) == "n")
    else:
        file_mngr.create(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Otrace", "cache", "warning"))

    if skip_warning == True:
        print("--- Welcome to 0trace ---")
        print("")
        print("The program is automatically starting up and skipping the routine warning.")
        print("")
    elif skip_warning == False:
        print("--- Welcome to 0trace ---")
        print("")
        print("The program is about to start up,")
        print("please don't interrupt the process.")
        print("")
        input("Press enter to continue...")
        print("")
    else:
        print("--- Welcome to 0trace ---")
        print("")
        print("The program is about to start up,")
        print("please don't interrupt the process.")
        print("")
        answer = input("Should we warn you again next time? (y/n): ")
        if answer.lower() == "y":
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Otrace", "cache", "warning"), "w") as file:
                file.write("y")
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
            print("-> We will ask you again at the next start")
            print("")
            input("Press Enter to continue...")

    os.system("cls" if os.name == "nt" else "clear")

    delete_pycache = False
    if file_mngr.check(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Otrace", "cache", "del_pycache")):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Otrace", "cache", "del_pycache"), "r") as file:
            delete_pycache = bool(file.read(1) == "y")
    else:
        file_mngr.create(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Otrace", "cache", "del_pycache"))

    empty = file_mngr.empty(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Otrace", "cache", "del_pycache"))
    if empty == True:
        print("")
        print("The __pycache__ directory is used by Python to store compiled bytecode files, which help speed up program execution.")
        print("Would you like the program to automatically delete the __pycache__ directory on startup?")
        print("")
        print("Pro:")
        print("- Ensures a clean environment by removing potentially outdated or corrupted bytecode files.")
        print("- Useful during development to avoid issues caused by stale cache.")
        print("")
        print("Contra:")
        print("- Slower startup time as Python will need to recompile bytecode files.")
        print("- May not be necessary in production environments where stability is prioritized.")
        print("")
        print("(!) We recommend to disable it to prioritize faster startup times. (n)")
        print("")
        answer = input("Do you want to automaticly delete the __pycache__ when the program starts up? (y/n): ")
        if answer.lower() == "y":
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Otrace", "cache", "del_pycache"), "w") as file:
                file.write("y")
            print("")
            print("(*) Automatic deletion of the __pycache__ enabled.")
            print("")
        if answer.lower() == "n":
            try:
                with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Otrace", "cache", "del_pycache"), "w") as file:
                    file.write("n")
                print("")
                print("(*) Automatic deletion of the __pycache__ disabled.")
                print("")
            except FileNotFoundError:
                print("")
                print("(!) Deletion not disabled. Error writing to cache.")
                print("(!) cache will get repaired during startup")
                print("")
                print("(*) Deletion disabled by default.")
                print("")
                input("Press Enter to continue...")

    if delete_pycache == True:
        print("")
        print("Deleting __pycache__ as the user configured")
        print("")
    elif delete_pycache == False:
        print("")
        print("Won't delete __pycache__ as the user configured")
        print("")
    else:
        print("")
        print("The __pycache__ directory is used by Python to store compiled bytecode files, which help speed up program execution.")
        print("Would you like the program to automatically delete the __pycache__ directory on startup?")
        print("")
        print("Pro:")
        print("- Ensures a clean environment by removing potentially outdated or corrupted bytecode files.")
        print("- Useful during development to avoid issues caused by stale cache.")
        print("")
        print("Contra:")
        print("- Slower startup time as Python will need to recompile bytecode files.")
        print("- May not be necessary in production environments where stability is prioritized.")
        print("")
        print("(!) We recommend to disable it to prioritize faster startup times. (n)")
        print("")
        answer = input("Do you want to automaticly delete the __pycache__ when the program starts up? (y/n): ")
        if answer.lower() == "y":
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Otrace", "cache", "del_pycache"), "w") as file:
                file.write("y")
            print("")
            print("(*) Automatic deletion of the __pycache__ enabled.")
            print("")
        if answer.lower() == "n":
            try:
                with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Otrace", "cache", "del_pycache"), "w") as file:
                    file.write("n")
                print("")
                print("(*) Automatic deletion of the __pycache__ disabled.")
                print("")
            except FileNotFoundError:
                print("")
                print("(!) Deletion not disabled. Error writing to cache.")
                print("(!) cache will get repaired during startup")
                print("")
                print("(*) Deletion disabled by default.")
                print("")
                input("Press Enter to continue...")
        else:
            print("")
            print("(!) Invalid input. Deletion disabled by default.")
            print("(*) Deletion disabled.")
            print("")
            print("-> We will ask you again at the next start")
            print("")
            input("Press Enter to continue...")

    os.system("cls" if os.name == "nt" else "clear")
    print("Starting up...")
    print("")
    
    os_name = sys.platform
    if os_name.startswith('win'):
        client_os = "Windows"
        script_file_ending = "bat"
    elif os_name.startswith('darwin'):
        client_os = "MacOS"
        script_file_ending = "sh"
    elif os_name.startswith('linux'):
        client_os = "Linux"
        script_file_ending = "sh"
    else:
        client_os = "Unknown"
        script_file_ending = "unknown"
        
    version = "0.01"
    author = "CodingPengu007"
    program = "0trace"
    publicity = "Closed Early Alpha"

    main_dir = os.path.dirname(os.path.abspath(__file__))
    venv_dir = os.path.join(main_dir, 'Otrace_venv')
    
    shell_script_path = os.path.join(main_dir, "Otrace", "scripts", f"start_{client_os.lower()}.{script_file_ending}")
    home_dir_path = os.path.join(main_dir, "Otrace", "local", "home")
    passwd_path = os.path.join(main_dir, "Otrace", "etc", "passwd")
    shadow_path = os.path.join(main_dir, "Otrace", "etc", "shadow")
    hostname_path = os.path.join(main_dir, "Otrace", "etc", "hostname")
    
    print(f"Detected operating system: {client_os}")

    ### Virtual Environment Management ###
    print("")
    print("Checking virtual environment:")
    if not file_mngr.check(venv_dir):
        print("(!) Virtual environment not found. (This is normal when starting for the first time)")
        print("")
        print("--------------------------------------------------------------------------------------")
        print("This is the first time you are running this program, thanks for that!")
        print("But please be aware that the first time will take a little bit longer than usual. :)")
        print("So please wait while the virtual environment is set up:")
        print("--------------------------------------------------------------------------------------")
        print("")
        
        print("(!) Program starting up for the first time! Removing saves of developers...")
        print("Removing user directories...")
        file_mngr.remove_lower(home_dir_path)
        print("User directories removed.")
        print("Flushing all files storing user data...")
        with open(passwd_path, 'w') as file:
            file.flush
        with open(shadow_path, 'w') as file:
            file.flush        
        with open(hostname_path, 'w') as file:
            file.flush
        print("Flushed all files!")
        
        print("")
    else:
        print("The virtual environment exists and has been found!")
    print("")
    print(f"Running shell script for: {client_os}")
    print(f"-> start_{client_os.lower()}.{script_file_ending}")
    try:
        result = subprocess.run(["bash", shell_script_path], capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)
        if result.returncode != 0:
            print(f"Shell script exited with non-zero status: {result.returncode}")
            print("Please check the script for errors.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the shell script: {e}")
        print(f"Script output: {e.output}")
        print(f"Script error: {e.stderr}")
    print("")
    ### ----------------------------- ###
    
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
    if delete_pycache == True:
        print("")
        print("Removing __pycache__ directories:")
        print("")
        game.sys.file_mngr.remove_pycache(main_dir)
        print("")
        print("Removed __pycache__ directories.")
        print("")
    ### ------------------------ ###
    
    ### Check if essential system files exist ###
    print("")
    print("Checking if essential system files exist:")
    print("")
    
    files_to_check = [
        ("hostname", os.path.join(main_dir, "Otrace", "local", "etc", "hostname")),
        ("username", os.path.join(main_dir, "Otrace", "local", "etc", "passwd")),
        ("password", os.path.join(main_dir, "Otrace", "local", "etc", "shadow")),
        ("sudoers", os.path.join(main_dir, "Otrace", "local", "etc", "sudoers")),
    ]
    
    for file_desc, file_path in files_to_check:
        print(f"Checking for {file_desc} file")
        if not game.sys.file_mngr.check(file_path):
            print(f"(!) {file_desc} file not found")
            print(f"Creating {file_desc} file...")
            game.sys.file_mngr.create(file_path)
            print(f"{file_desc} file created successfully.")
        else:
            print(f"{file_desc} file found.")
        
    print("")
    ### ------------------------------------ ###

    ### Check if apt sources file exists ###
    print("")
    print("Checking for apt sources file:")
    if not game.sys.file_mngr.check(os.path.join(main_dir, "Otrace", "programs", "apt", "sources")):
        print("(!) apt sources file not found.")
        print("sources file created successfully.")
    else:
        print("apt sources file found.")
    print("")
    ### ----------------------------------- ###

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
        game.sys.accnt_mngr.signup(main_dir, "sudo")
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
    game.prgms.cmd.line(username, hostname, current_dir, local_dir, main_dir)
except KeyboardInterrupt:
    print("Exiting...")
    os.system("cls" if os.name == "nt" else "clear")
    sys.exit(0)
except Exception as e:
    print(f"An error occurred: {e}")
    
#################################################################################