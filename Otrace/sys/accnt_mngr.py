#################################################################################

import os
import Otrace as game
import getpass

#################################################################################

def check(main_dir):
    if game.sys.file_mngr.empty(os.path.join(main_dir, "Otrace", "local", "etc", "shadow")) and game.sys.file_mngr.check(os.path.join(main_dir, "Otrace", "local", "etc", "passwd")):
        return False
    else:
        return True

def login_or_signup():
    print("| Do you want to login or sign up?")
    print("| 1. Login")
    print("| 2. Sign Up")
    print("")
    while True:
        choice = input("| > ")
        if choice == "1":
            return "login"
        elif choice == "2":
            return "signup"
        else:
            print("")
            print("| (!) Invalid choice. Please try again.")
            print("")
    
def signup(main_dir, sudo):
    
    import bcrypt
    
    password_file_path = os.path.join(main_dir, "Otrace", "local", "etc", "shadow")
    username_file_path = os.path.join(main_dir, "Otrace", "local", "etc", "passwd")
    sudo_file_path = os.path.join(main_dir, "Otrace", "local", "etc", "sudoers")
    
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("")
        print("| Sign Up")
        print("|")
        username = input("| Username: ")
        
        existing_usernames = [username.strip() for username in game.sys.file_mngr.list_load(username_file_path)]
        if username in existing_usernames:
            print("")
            input("| (!) This username is already taken, please try another one. Press Enter to try again.")
            continue
                    
        pw1 = getpass.getpass("| Password: ", stream=None)
        print("|")
        pw2 = getpass.getpass("| Confirm Password: ", stream=None)
        print("")
        
        if pw1 == pw2:
            # Generate hash with salt
            pw_hash = bcrypt.hashpw(pw1.encode('utf-8'), bcrypt.gensalt())
            
            # Write the username and hashed password to files
            try:
                with open(username_file_path, "a") as user_file:  # Append mode for usernames
                    user_file.write(username + "\n")
                
                with open(password_file_path, "ab") as pw_file:  # Append binary mode for passwords
                    pw_file.write(pw_hash + b"\n")
                
                os.mkdir(os.path.join(main_dir, "Otrace", "local", "home", username))
                
                if sudo:
                    print("| Created new SUDO Account (admin)")
                    with open(sudo_file_path, "w") as sudo_file:
                        sudo_file.write(username + "\n")
                
                input("| Account created successfully. Press Enter to continue.")
            except Exception as e:
                print(f"| (!) An error occurred: {e}")
            
            break
        else:
            input("| (!) Passwords do not match. Press Enter to try again.")
    
    os.system("cls" if os.name == "nt" else "clear")

    
def login(main_dir):
    
    import bcrypt
    
    password_file_path = os.path.join(main_dir, "Otrace", "local", "etc", "shadow")
    username_file_path = os.path.join(main_dir, "Otrace", "local", "etc", "passwd")
    
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("")
        print("| Login")
        print("|")
        username = input("| Username: ")
        pw = getpass.getpass("| Password: ", stream=None)
        print("")
        
        with open(username_file_path, "r") as user_file:
            usernames = [line.strip() for line in user_file.readlines()]
            user = None
            user_index = None
            for i, user_in_file in enumerate(usernames):
                if username == user_in_file:
                    user = user_in_file
                    user_index = i
                    break
        
        with open(password_file_path, "rb") as pw_file:
            passwords = [line.strip() for line in pw_file.readlines()]

        if user is not None and user_index is not None and user_index < len(passwords):
            if bcrypt.checkpw(pw.encode('utf-8'), passwords[user_index]):
                input("| Login successful. Press Enter to continue.")
                username = usernames[user_index]
                break
            else:
                input("| (!) Incorrect password or username. Press Enter to try again.")
        else:
            input("| (!) Incorrect password or username. Press Enter to try again.")
    os.system("cls" if os.name == "nt" else "clear")
    return username

def create_hostname(main_dir):
    hostname_file_path = os.path.join(main_dir, "Otrace", "local",
                                      "etc", "hostname")
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("")
        print("| Hostname Creation")
        print("|")
        hostname = input("| Hostname: ")
        print("")
        with open(hostname_file_path, "w") as file:
            file.write(hostname)
        input("| Hostname created successfully. Press Enter to continue.")
        break
    os.system("cls" if os.name == "nt" else "clear")
    
def load_hostname(main_dir):
    hostname_file_path = os.path.join(main_dir, "Otrace", "local",
                                      "etc", "hostname")
    with open(hostname_file_path, "r") as file:
        hostname = file.read()
    return hostname

#################################################################################