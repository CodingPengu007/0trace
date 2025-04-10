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
    alias_file_path = os.path.join(local_dir, "home", username, "cache", "aliases")
    cache_path = os.path.join(local_dir, "home", username, "cache")
    sudo_file_path = os.path.join(local_dir, "etc", "sudoers")
    log_file_path = os.path.join(local_dir, "home", username, "cache", "local_logs")
    sources_file_path = os.path.join(main_dir, "Otrace", "programs", "apt", "sources")
    home_dir = os.path.join(local_dir, "home")

    # Load aliases from file if it exists
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
            # Check if the command is an alias
            if cmd in aliases:
                full_cmd = aliases[cmd].split() + full_cmd[1:]
                cmd = full_cmd[0]
            with open(log_file_path, 'a') as file:
                file.write(cmd + "\n")
        else:
            get_command = True
        
        cmd = full_cmd[0]
        skip_line = False
        
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
                
        elif cmd == "alias":
            if len(full_cmd) == 2 and full_cmd[1] == "show":
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
            elif len(full_cmd) != 3:
                print("Usage: alias <command> <new_alias>, alias show, or alias delete <alias_name>")
            else:
                command, alias = full_cmd[1], full_cmd[2]
                if full_cmd[2] == "echo":
                    print("Echo can not be aliased.")
                elif alias in aliases:
                    print(f"Alias {alias} already exists for command {aliases[alias]}.")
                elif command in aliases.values():
                    print(f"Command {command} is already aliased to {list(aliases.keys())[list(aliases.values()).index(command)]}.")
                else:
                    aliases[alias] = command
                    with open(alias_file_path, 'a') as file:
                        file.write(f"{alias}={command}\n")
                    print(f"Alias '{alias}' created for command '{command}'.")
        elif cmd == "ls":
            if len(full_cmd) > 2:
                print("Usage: ls [dir]")
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
            else:
                try:
                    new_dir = os.path.expanduser(full_cmd[1])
                    if not os.path.isabs(new_dir):
                        new_dir = os.path.normpath(os.path.join(current_dir, new_dir))
                    if new_dir == "..":
                        new_dir = os.path.dirname(current_dir)
                    try:
                        if os.path.commonpath([new_dir, home_dir]) != home_dir:
                            print("Permission denied.")
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
            else:
                try:
                    import texteditor
                    file_path = os.path.join(current_dir, full_cmd[1])
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
                    
        elif cmd == "rm":
            not_empty_detected = False
            if len(full_cmd) < 2 or len(full_cmd) > 3:
                print("Usage: rm <file> or rm -rf <folder>")
            elif len(full_cmd) == 2:
                try:
                    file_path = os.path.join(current_dir, full_cmd[1])
                    if os.path.isdir(file_path):
                        if not os.listdir(file_path):
                            os.rmdir(file_path)
                            print(f"Empty folder {full_cmd[1]} removed.")
                        else:
                            not_empty_detected = True
                            print(f"Folder {full_cmd[1]} is not empty. Use 'rm -rf <folder>' to remove with all contents.")
                    os.remove(file_path)
                    print(f"File {full_cmd[1]} removed.")
                except FileNotFoundError:
                    print(f"No such file or directory: '{full_cmd[1]}'")
                except Exception as e:
                    if not_empty_detected == False:
                        print(f"Error removing file or folder: {e}")
                    
            elif len(full_cmd) == 3 and full_cmd[1] == "-rf":
                try:
                    folder_path = os.path.join(current_dir, full_cmd[2])
                    if os.path.isdir(folder_path):
                        shutil.rmtree(folder_path)
                        print(f"Folder {full_cmd[2]} and all its contents removed.")
                    else:
                        print(f"'{full_cmd[2]}' is not a folder.")
                except FileNotFoundError:
                    print(f"No such folder: '{full_cmd[2]}'")
                except Exception as e:
                    print(f"Error force removing folder: {e}")
                    
        elif cmd == "clear" or cmd == "cls":
            os.system('clear' if os.name == 'posix' else 'cls')
        elif cmd == "exit":
            if len(full_cmd) > 1:
                print("Command doesn't take any arguments.")
            break
        elif cmd == "sudo":
            if len(full_cmd) < 2:
                print("Usage: sudo <command>")
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
            if not len(full_cmd) > 1 or len(full_cmd) > 3:
                print("Usage: apt <option> <program>")
            elif sudo == False:
                print("Permission denied.")
            else:
                if full_cmd[1] == "add":
                    author = full_cmd[2]
                    with open(sources_file_path, 'a') as file:
                        file.write(author + "\n")
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
                                response = requests.head(url, timeout=5)
                                if response.status_code == 200:
                                    print(f"[checked] {author}")
                                else:
                                    print("")
                                    print(f"[!] {author} is not reachable.")
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
                            for program in os.listdir(opt_dir):
                                program_path = os.path.join(opt_dir, program)
                                if os.path.isdir(program_path):
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
                                    found = True
                                    print(f"Cloning {program} from {repo_url}...")
                                    target_folder = os.path.join(local_dir, "opt", program)
                                    os.makedirs(target_folder, exist_ok=True)
                                    subprocess.run(["git", "clone", repo_url, target_folder], check=True)
                                    print(f"{program} installed successfully.")
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
                        
        elif cmd == "bash":
            if len(full_cmd) < 2:
                print("Usage: bash <file>")
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
                    print(f"No such file: '{full_cmd[1]}'")
                    
        elif cmd == "echo":
            if len(full_cmd) < 2:
                print("Usage: echo <text>")
            else:
                print(" ".join(full_cmd[1:]))
        
        else:
            print("Command not found.")
        
        if not skip_line == True:
            print("")
            
        if not sudo_protect == True:
            sudo = False
        else:
            sudo_protect = False
        
#################################################################################