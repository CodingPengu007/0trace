#################################################################################

import os
import shutil
import subprocess

import Otrace as gm

#################################################################################

def line(username, hostname, current_dir, local_dir, main_dir):
    script = []
    full_cmd = []
    cmd = ""

    aliases = {}
    
    etc_dir = os.path.join(local_dir, "etc")
    home_dir = os.path.join(local_dir, "home")
    
    alias_file_path = os.path.join(local_dir, "home", username, "Cache", "aliases")
    cache_path = os.path.join(local_dir, "home", username, "Cache")
    sudo_file_path = os.path.join(local_dir, "etc", "sudoers")
    log_file_path = os.path.join(local_dir, "home", username, "Cache", "local_logs")
    sources_file_path = os.path.join(main_dir, "Otrace", "programs", "apt", "sources")
    
    commands = ["ls", "cd", "cat", "mkdir", "clear", "alias", "nano", "exit", "rm", "bash", "echo", "visudo", "apt", "sudo"]

    if os.path.exists(alias_file_path):
        with open(alias_file_path, 'r') as file:
            for line in file:
                alias, command = line.strip().split("=", 1)
                aliases[alias] = command

    get_command = True
    sudo = False
    script_sudo = False
    script_active = False
    sudo_protect = False

    while True:
        show_dir = "/" + os.path.relpath(current_dir, local_dir)
        if show_dir == f"/home/{username}":
            show_dir = "~"
        elif show_dir == "/.":
            show_dir = "/"
        if script_active:
            if script_line <= script_lines:
                full_cmd = script[script_line].split()
                cmd = full_cmd[0]
                get_command = False
                skip_line = False
                script_line += 1
            else:
                script_active = False
                script_line = 0
                script_lines = 0
                script = []
                script_sudo = False
                get_command = True
        elif script_sudo == True:
            sudo = True
        if get_command == True:
            full_cmd = input(f"| ({username}@{hostname})-[{show_dir}]\n| $ ").split()
            print("")
            if not full_cmd:
                continue
            if not gm.sys.file_mngr.check(cache_path):
                os.makedirs(cache_path, exist_ok=True)
            if not gm.sys.file_mngr.check(alias_file_path):
                with open(alias_file_path, 'w') as file:
                    pass
            if not gm.sys.file_mngr.check(log_file_path):
                with open(log_file_path, 'w') as file:
                    pass
            if cmd in aliases:
                full_cmd = aliases[cmd].split() + full_cmd[1:]
                cmd = full_cmd[0]
            with open(log_file_path, 'a') as file:
                file.write(cmd + "\n")
        else:
            get_command = True
            
        cmd = full_cmd[0]
        skip_line = False
        just_removed = False
        
        if cmd == "help":
            if len(full_cmd) > 1:
                print("Command doesn't take any arguments.")
            else:
                print("Commands:")
                print("  help                           - Display this help message.")
                print("  ls [dir]                       - List files in current or specified directory.")
                print("  cd <dir>                       - Change directory.")
                print("  cat <file>                     - Print file contents.")
                print("  mkdir <dir>                    - Create a new directory.")
                print("  clear                          - Clear the terminal screen.")
                print("  alias <command> <new_alias>    - Create an alias for a command.")
                print("  nano <file>                    - Create or edit a file using a simple text editor.")
                print("  exit                           - Exit the shell.")
                print("  rm <file>                      - Remove a file.")
                print("  bash <file>                    - Run a script file with the file ending .sh")
                print("  echo <text>                    - Print text to the terminal.")
                print("  visudo                         - Edit the sudoers file.                                            (!) Requires sudo")
                print("  apt <option> <program>         - Package manager for installing, updating, and removing programs.  (!) Requires sudo")
                print("  sudo <command>                 - Execute a command with superuser privileges.                      (!) Requires sudo")
                #test
        elif cmd == "alias":
            if len(full_cmd) < 2 or len(full_cmd) > 3:
                print("Usage: alias <command> <new_alias>, alias show, or alias delete <alias_name>")
            elif full_cmd[1] == "-h":
                print("Command:")
                print("alias")
                print("")
                print("Description:")
                print("Create, show, or delete aiases for commands.")
                print("Aliases are stored in the cache directory.")
                print("")
                print("Usage:")
                print("alias <command> <new_alias>  - Create an alias for a command.")
                print("alias show                   - Show all defined aliases.")
                print("alias delete <alias_name>    - Delete an alias.")
                print("")
                print("Examples:")
                print("alias ls list")
                print("alias show")
                print("alias delete list")
            elif len(full_cmd) == 2 and full_cmd[1] == "show":
                if aliases:
                    print("Aliases:")
                    for alias, command in aliases.items():
                        print(f"  {alias} -> {command}")
                else:
                    print("No aliases defined.")
            elif len(full_cmd) == 3 and full_cmd[1] == "delete":
                alias_to_delete = full_cmd[2]
                if alias_to_delete in aliases:
                    del aliases[alias_to_delete]
                    with open(alias_file_path, 'w') as file:
                        for alias, command in aliases.items():
                            file.write(f"{alias}={command}\n")
                    print(f"Alias {alias_to_delete} deleted.")
                else:
                    print(f"Alias {alias_to_delete} does not exist.")
            else:
                command, alias = full_cmd[1], full_cmd[2]
                if full_cmd[2] == "echo":
                    print("Echo can not be aliased.")
                elif alias in aliases:
                    print(f"Alias {alias} already exists for command {aliases[alias]}.")
                elif alias in commands:
                    print(f"{alias} is a command and cannot be used as an alias.")
                elif command in aliases.values():
                    print(f"Command {command} is already aliased to {list(aliases.keys())[list(aliases.values()).index(command)]}.")
                else:
                    aliases[alias] = command
                    with open(alias_file_path, 'a') as file:
                        file.write(f"{alias}={command}\n")
                    print(f"Alias '{alias}' created for command '{command}'.")
                    
        elif cmd == "ls" or cmd == "dir":
            if len(full_cmd) > 2:
                print("Usage: ls [dir]")
            elif len(full_cmd) == "-h":
                print("Command:")
                print("ls, dir")
                print("")
                print("Description:")
                print("List files and directories in the current (without any arguments 'ls') or specified directory (with the directory specified 'ls directory').")
                print("")
                print("Usage:")
                print("ls <dir> - List files in the specified directory.")
                print("ls       - List files in the current directory.")
                print("")
                print("Examples:")
                print("ls")
                print("ls Documents")
            else:
                target_dir = current_dir if len(full_cmd) == 1 else full_cmd[1]
                if len(full_cmd) == 2:
                    target_dir = current_dir + "/" + target_dir
                try:
                    items = os.listdir(target_dir)
                    if not items:
                        skip_line = True
                    else:
                        for item in items:
                            print(item)
                except FileNotFoundError:
                    print(f"No such file or directory: '{target_dir}'")
                    
        elif cmd == "cd":
            if len(full_cmd) != 2:
                print("Usage: cd <dir>")
            elif full_cmd[1] == "-h":
                print("Command:")
                print("cd")
                print("")
                print("Description:")
                print("Change the current working directory.")
                print("")
                print("Usage:")
                print("cd <dir> - Change to the specified directory.")
                print("cd ..    - Change to the parent directory.")
                print("cd       - Change to the home directory.")
                print("")
                print("Examples:")
                print("cd /home/user/documents")
                print("cd ..")
                print("cd Downloads")
            else:
                try:
                    new_dir = os.path.expanduser(full_cmd[1])
                    if not os.path.isabs(new_dir):
                        new_dir = os.path.normpath(os.path.join(current_dir, new_dir))
                    if new_dir == "..":
                        new_dir = os.path.dirname(current_dir)
                    try:
                        if not os.path.commonpath([new_dir, local_dir]).startswith(local_dir):
                            print("Permission denied.")
                            print("")
                            continue
                        if new_dir == etc_dir:
                            print("Permission denied.")
                            print("")
                            continue
                        if current_dir == home_dir and os.path.commonpath([new_dir, home_dir]) == home_dir:
                            users = []
                            try:
                                users = gm.sys.file_mngr.list_load(os.path.join(etc_dir, "passwd"))
                            except FileNotFoundError:
                                print(f"No such file or directory: '{full_cmd[1]}'")
                            except Exception as e:
                                print(f"An error occurred: {e}")
                            if new_dir in users and new_dir != username and sudo != True:
                                print("Permission denied")
                                print("")
                                continue
                    except ValueError:
                        print("Invalid path comparison.")
                        print("")
                        continue
                    try:
                        os.chdir(new_dir)
                        current_dir = os.getcwd()
                    except FileNotFoundError:
                        print(f"No such file or directory: '{full_cmd[1]}'")
                except FileNotFoundError:
                    print(f"No such file or directory: '{full_cmd[1]}'")
                except Exception as e:
                    print(f"An error occurred: {e}")
                skip_line = True
                
        elif cmd == "cat":
            if len(full_cmd) != 2:
                print("Usage: cat <file>")
            elif full_cmd[1] == "-h":
                print("Command:")
                print("cat")
                print("")
                print("Description:")
                print("Print the contents of a file.")
                print("")
                print("Usage:")
                print("cat <file>   - Print the contents of the specified file.")
                print("")
                print("Examples:")
                print("cat file.txt")
            else:
                try:
                    file_path = os.path.join(current_dir, full_cmd[1])
                    if os.path.isdir(file_path):
                        print(f"'{full_cmd[1]}' is a directory, not a file.")
                    else:
                        with open(file_path, 'r') as file:
                            print(file.read())
                except FileNotFoundError:
                    print(f"No such file: '{full_cmd[1]}'")
                    
        elif cmd == "mkdir":
            if len(full_cmd) != 2:
                print("Usage: mkdir <dir>")
            elif full_cmd[1] == "-h":
                print("Command:")
                print("mkdir")
                print("")
                print("Description:")
                print("Create a new directory.")
                print("")
                print("Usage:")
                print("mkdir <dir>  - Create a new directory with the specified name.")
                print("")
                print("Examples:")
                print("mkdir new_folder")
            else:
                try:
                    target_dir = os.path.join(current_dir, full_cmd[1])
                    dir_name = full_cmd[1]
                    os.makedirs(target_dir, exist_ok=True)
                    print(f"Directory {dir_name} created.")
                except Exception as e:
                    print(f"Error creating directory: {e}")
                    
        elif cmd == "nano":
            if len(full_cmd) != 2:
                print("Usage: nano <file>")
            elif full_cmd[1] == "-h":
                print("Command:")
                print("nano")
                print("")
                print("Description:")
                print("Create or edit a file using a simple text editor.")
                print("")
                print("Usage:")
                print("nano <file>  - Create or edit the specified file.")
                print("")
                print("Examples:")
                print("nano file.txt")
            else:
                file_path = os.path.join(current_dir, full_cmd[1])
                if os.path.isdir(file_path):
                    print(f"{full_cmd[1]} is a directory, not a file.")
                elif file_path == alias_file_path:
                    print("Please use 'alias' command to edit aliases.")
                else:
                    try:
                        import texteditor
                        if not os.path.exists(file_path):
                            with open(file_path, 'w') as file:
                                pass
                        edited_content = texteditor.open(filename=file_path)
                        with open(file_path, 'w') as file:
                            file.write(edited_content)
                        skip_line = True
                    except FileNotFoundError:
                        print(f"No such file: '{full_cmd[1]}'")
                    except Exception as e:
                        print(f"Error using texteditor: {e}")
                    
        elif cmd in ["rm", "del", "delete", "remove"]:
            not_empty_detected = False
            if len(full_cmd) < 2 or len(full_cmd) > 3:
                print("Usage: rm <file> or rm -rf <folder>")
            elif full_cmd[1] == "-h":
                print("Command:")
                print("rm, remove, del, delete")
                print("")
                print("Description:")
                print("Remove a file or directory.")
                print("")
                print("Usage:")
                print("rm <file>        - Remove the specified file.")
                print("rm -rf <folder>  - Remove the specified folder and all its contents.")
                print("")
                print("Examples:")
                print("rm file.txt")
                print("rm -rf folder")
            elif len(full_cmd) == 2:
                try:
                    file_path = os.path.join(current_dir, full_cmd[1])
                    if os.path.isdir(file_path):
                        if not os.listdir(file_path):
                            just_removed = True
                            os.rmdir(file_path)
                            print(f"Empty folder {full_cmd[1]} removed.")
                        else:
                            not_empty_detected = True
                            print(f"Folder {full_cmd[1]} is not empty. Use 'rm -rf {full_cmd[1]}' to remove it with all contents.")
                    else:
                        os.remove(file_path)
                        print(f"File {full_cmd[1]} removed.")
                except FileNotFoundError:
                    if not just_removed:
                        print(f"No such file or directory: '{full_cmd[1]}'")
                except PermissionError:
                    print(f"Permission denied: Unable to remove '{full_cmd[1]}'.")
                except Exception as e:
                    if not_empty_detected == False:
                        print(f"Error removing file or folder: {e}")
            elif len(full_cmd) == 3 and full_cmd[1] == "-rf":
                folder_path = os.path.join(current_dir, full_cmd[2])
                try:
                    if os.path.isdir(folder_path):
                        shutil.rmtree(folder_path)  # This should remove the folder and all its contents
                        print(f"Folder {full_cmd[2]} and all its contents removed.")
                    else:
                        print(f"'{full_cmd[2]}' is not a folder.")
                except FileNotFoundError:
                    print(f"No such folder: '{full_cmd[2]}'")
                except PermissionError:
                    print(f"Permission denied: Unable to remove '{full_cmd[2]}'.")
                except Exception as e:
                    print(f"Error force removing folder: {e}")
            else:
                print(f"Unknown argument: {full_cmd[1]}")
                    
        elif cmd == "clear" or cmd == "cls":
            if len(full_cmd) > 1:
                print("Usage: clear")
            elif len(full_cmd) == 1:
                os.system('clear' if os.name == 'posix' else 'cls')
            else:
                print(f"Unknown argument: {full_cmd[1]}")
                
        elif cmd == "exit":
            if len(full_cmd) > 2:
                print("Usage: exit or exit -h")
            elif len(full_cmd) == 1:
                break
            elif full_cmd[1] == "-h":
                print("Command:")
                print("exit")
                print("")
                print("Description:")
                print("Exit the shell.")
                print("")
                print("Usage:")
                print("exit")
                print("")
                print("Examples:")
                print("exit")
            else:
                print(f"Unknown argument: {full_cmd[1]}")
        
        elif cmd == "sudo":
            if len(full_cmd) < 2:
                print("Usage: sudo <command>")
            elif full_cmd[1] == "-h":
                print("Command:")
                print("sudo")
                print("")
                print("Description:")
                print("Execute a command with superuser privileges.")
                print("")
                print("Usage:")
                print("sudo <command>   - Execute the specified command with superuser privileges.")
                print("")
                print("Examples:")
                print("sudo apt update")
            else:
                sudoers = [username.strip() for username in gm.sys.file_mngr.list_load(sudo_file_path)]
                if username in sudoers:
                    get_command = False
                    sudo = True
                    full_cmd.pop(0)
                    skip_line = True
                    sudo_protect = True
                else:
                    print(f"{username} is not in the sudoers file.")
    
        elif cmd == "apt":
            if not len(full_cmd) > 1 or len(full_cmd) > 4:
                print("Usage: apt <option> <program> or apt source <option> <option>")
            elif full_cmd[1] == "-h":
                print("Command:")
                print("apt")
                print("")
                print("Description:")
                print("Package manager for installing, updating, and removing programs.")
                print("(!) This command requires superuser privileges.")
                print("")
                print("Usage:")
                print("apt source add <author>      - Add an author to the sources.")
                print("apt source remove <author>   - Remove an author from the sources.")
                print("apt source list              - List all authors in the sources.")
                print("--- or ---")
                print("apt src add <author>         - Add an author to the sources.")
                print("apt src rm <author>          - Remove an author from the sources.")
                print("apt src ls                   - List all authors in the sources.")
                print("")
                print("apt update                   - Update the sources and check if the authors exist.")
                print("apt upgrade                  - Upgrade all installed programs.")
                print("")
                print("apt install <program>        - Install a program from the sources.")
                print("apt remove <program>         - Remove a program.")
                print("")
                print("Examples:")
                print("sudo apt source add CodingPengu007")
                print("sudo apt source remove CodingPengu007")
                print("apt source list")
                print("--- or ---")
                print("sudo apt src add CodingPengu007")
                print("sudo apt src rm CodingPengu007")
                print("apt src ls")
                print("")
                print("sudo apt update")
                print("sudo apt upgrade")
                print("")
                print("sudo apt install pencrypt")
                print("sudo apt remove pencrypt")

            elif (full_cmd[1] == "source" or full_cmd[1] == "src") and (full_cmd[2] == "list" or full_cmd[2] == "ls"):
                try:
                    with open(sources_file_path, 'r') as file:
                        authors = [author.strip() for author in file.readlines()]
                    if authors:
                        print("Authors in sources:")
                        for author in authors:
                            print(f"  {author}")
                    else:
                        print("No authors found in sources.")
                except FileNotFoundError:
                    print("Sources file not found.")

            elif sudo == False:
                print("Permission denied.")
                
            else:
                if (full_cmd[1] == "source" or full_cmd[1] == "src") and full_cmd[2] == "add":
                    author = full_cmd[3]
                    with open(sources_file_path, 'a') as file:
                        file.write(author + "\n")
                    skip_line = False
                
                elif (full_cmd[1] == "source" or full_cmd[1] == "src") and (full_cmd[2] == "remove" or full_cmd[2] == "rm"):
                    author = full_cmd[2]
                    with open(sources_file_path, 'r') as file:
                        lines = file.readlines()
                    with open(sources_file_path, 'w') as file:
                        for line in lines:
                            if line.strip() != author:
                                file.write(line)
                    skip_line = False
                        
                elif full_cmd[1] == "update":
                    try:
                        import requests
                        with open(sources_file_path, 'r') as file:
                            urls = ["https://github.com/" + line.strip() for line in file.readlines()]
                            authors = [author.strip() for author in gm.sys.file_mngr.list_load(sources_file_path)]
                        for url, author in zip(urls, authors):
                            url = url.strip()
                            try:
                                response = requests.head(url, timeout=10)
                                if response.status_code == 200:
                                    print(f"[checked] {author}")
                                else:
                                    print("")
                                    print(f"[!] {author} does not exist.")
                                    print(f"Account URL: {url}")
                                    print(f"Status code: {response.status_code}")
                                    print("")
                            except requests.RequestException as e:
                                print(f"Error checking {url}: {e}")
                    except FileNotFoundError:
                        print("Sources file not found.")
                    except Exception as e:
                        print(f"Error checking URLs: {e}")
                
                elif full_cmd[1] == "upgrade":
                    try:
                        opt_dir = os.path.join(local_dir, "opt")
                        if not os.path.exists(opt_dir):
                            print("No programs installed to upgrade.")
                        else:
                            programs = [program for program in os.listdir(opt_dir) if os.path.isdir(os.path.join(opt_dir, program))]
                            for program in programs:
                                program_path = os.path.join(opt_dir, program)
                                print(f"Updating {program}...")
                                subprocess.run(["git", "-C", program_path, "pull"], check=True)
                                print(f"{program} updated successfully.")
                    except Exception as e:
                        print(f"Error upgrading programs: {e}")
                    try:
                        print(f"Updating {program}...")
                        subprocess.run(["git", "-C", main_dir, "pull"], check=True)
                        print(f"0trace updated successfully.")
                    except Exception as e:
                        print(f"Error upgrading 0trace")
                        
                elif full_cmd[1] == "install":
                    import requests
                    program = full_cmd[2]
                    try:
                        with open(sources_file_path, 'r') as file:
                            authors = [author.strip() for author in file.readlines()]
                        found = False
                        for author in authors:
                            repo_url = f"https://github.com/{author}/{program}.git"
                            print(f"Checking repository: {repo_url}")  # Log the URL being checked
                            try:
                                response = requests.head(repo_url, allow_redirects=True, timeout=5)
                                if response.status_code == 200:
                                    target_folder = os.path.join(local_dir, "opt", program)
                                    if os.path.exists(target_folder):
                                        print(f"Program {program} is already installed.")
                                        found = True
                                        break
                                    print(f"Cloning {program} from {repo_url}...")
                                    os.makedirs(target_folder, exist_ok=True)
                                    subprocess.run(["git", "clone", repo_url, target_folder], check=True)
                                    print(f"{program} installed successfully.")
                                    found = True
                                    break
                                else:
                                    print(f"Repository {repo_url} returned status code {response.status_code}.")
                            except requests.RequestException as e:
                                print(f"Error checking {repo_url}: {e}")
                        if not found:
                            print(f"Program {program} not found in sources. Ensure the program name and author are correct.")
                    except FileNotFoundError:
                        print("Sources file not found. Ensure the sources contain valid authors.")
                    except Exception as e:
                        print(f"Error installing program: {e}")
                
                elif full_cmd[1] == "remove":
                    program = full_cmd[2]
                    target_folder = os.path.join(local_dir, "opt", program)
                    if os.path.exists(target_folder):
                        shutil.rmtree(target_folder)
                        print(f"{program} removed successfully.")
                    else:
                        print(f"No such program: {program}")
                else:
                    print(f"Unknown argument: {full_cmd[1]}")
                        
        elif cmd == "bash":
            if len(full_cmd) < 2:
                print("Usage: bash <file>")
            elif full_cmd[1] == "-h":
                print("Command:")
                print("bash")
                print("")
                print("Description:")
                print("Run a script file with the file ending .sh")
                print("")
                print("Usage:")
                print("bash <file>  - Run the specified script file.")
                print("")
                print("Examples:")
                print("bash script.sh")
            elif not full_cmd[1].endswith(".sh"):
                print("File must have a .sh extension.")
            elif len(full_cmd) >= 2:
                file_path = os.path.join(current_dir, full_cmd[1])
                if os.path.exists(file_path):
                    try:
                        with open(file_path, 'r') as file:
                            script_active = True
                            script = file.readlines()
                            script_lines = len(script) - 1
                            script_line = 0
                            get_command = False
                            skip_line = False
                            if sudo == True:
                                script_sudo = True
                    except Exception as e:
                        print(f"Error reading script: {e}")
                else:
                    print(f"No such file: {full_cmd[1]}")
            else:
                print(f"Unknown argument: {full_cmd[1]}")
                    
        elif cmd == "echo":
            if len(full_cmd) < 2:
                print("Usage: echo <text>")
            elif full_cmd[1] == "-h":
                print("Command:")
                print("echo")
                print("")
                print("Description:")
                print("Print text to the terminal.")
                print("")
                print("Usage:")
                print("echo <text>  - Print the specified text to the terminal.")
                print("")
                print("Examples:")
                print("echo Hello World!")
            else:
                print(" ".join(full_cmd[1:]))

        elif cmd == "visudo":
            if len(full_cmd) > 1:
                print("Usage: visudo")
            elif sudo == False:
                print("Permission denied.")
            else:
                cmd = "nano"
                full_cmd = [cmd, sudo_file_path]
                
        elif cmd == "mv":
            if len(full_cmd) != 3:
                print("Usage: mv <source> <destination>")
            elif full_cmd[1] == "-h":
                print("Command:")
                print("mv")
                print("")
                print("Description:")
                print("Move or rename a file or directory.")
                print("")
                print("Usage:")
                print("mv <source> <destination>  - Move or rename the specified file or directory.")
                print("")
                print("Examples:")
                print("mv file.txt new_file.txt")
                print("mv folder /path/to/new_location")
            else:
                source = os.path.join(current_dir, full_cmd[1])
                destination = os.path.join(current_dir, full_cmd[2])
            try:
                shutil.move(source, destination)
                print(f"Moved '{full_cmd[1]}' to '{full_cmd[2]}'.")
            except FileNotFoundError:
                print(f"No such file or directory: '{full_cmd[1]}'")
            except Exception as e:
                print(f"Error moving file or directory: {e}")

        elif cmd == "cp":
            if len(full_cmd) != 3:
                print("Usage: cp <source> <destination>")
            elif full_cmd[1] == "-h":
                print("Command:")
                print("cp")
                print("")
                print("Description:")
                print("Copy a file or directory.")
                print("")
                print("Usage:")
                print("cp <source> <destination>  - Copy the specified file or directory.")
                print("")
                print("Examples:")
                print("cp file.txt copy_of_file.txt")
                print("cp -r folder /path/to/new_location")
            else:
                source = os.path.join(current_dir, full_cmd[1])
                destination = os.path.join(current_dir, full_cmd[2])
            try:
                if os.path.isdir(source):
                    shutil.copytree(source, destination)
                else:
                    shutil.copy2(source, destination)
                    print(f"Copied {full_cmd[1]} to {full_cmd[2]}.")
            except FileNotFoundError:
                print(f"No such file or directory: {full_cmd[1]}")
            except FileExistsError:
                print(f"Destination {full_cmd[2]} already exists.")
            except Exception as e:
                print(f"Error copying file or directory: {e}")

        else:
            if len(full_cmd) == 1 and gm.sys.file_mngr.check(os.path.join(local_dir, "opt", cmd)):
                target_folder = os.path.join(local_dir, "opt", cmd)
                if os.path.isdir(target_folder):
                    os.chdir(target_folder)
                    try:
                        if os.name == 'nt':
                            subprocess.run(["python", "-m", "main.py"], check=True)
                        else:
                            subprocess.run(["python3", "-m", "main.py"], check=True)
                    except subprocess.CalledProcessError as e:
                        print(f"(!) An error occurred: {e}")
                    except Exception as e:
                        print(f"(!) Unexpected error: {e}")
                    except KeyboardInterrupt:
                        print("\n----------------------------------------\n")
                        print(f"\nExiting {cmd}...")
                    except Exception as e:
                        print(f"An error occurred: {e}")
                    finally:
                        os.chdir(current_dir)
                else:
                    print(f"'{cmd}' is not a directory.")
            else:
                print("Command not found.")
                        
        if not skip_line == True:
            print("")
            
        if not sudo_protect == True:
            sudo = False
        else:
            sudo_protect = False
        
#################################################################################