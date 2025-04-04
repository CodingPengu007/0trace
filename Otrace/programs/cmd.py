#################################################################################

import os
import shutil

import Otrace as gm

#################################################################################

def line(username, hostname, current_dir, local_dir, main_dir):
    full_cmd = []
    cmd = ""

    aliases = {}
    alias_file_path = os.path.join(local_dir, "home", username, "cache", "aliases")
    cache_path = os.path.join(local_dir, "home", username, "cache")
    sudo_file_path = os.path.join(local_dir, "etc", "sudoers")
    
    if not gm.sys.file_mngr.check(cache_path):
        os.makedirs(cache_path, exist_ok=True)
    
    if not gm.sys.file_mngr.check(alias_file_path):
        with open(alias_file_path, 'w') as file:
            pass

    # Load aliases from file if it exists
    if os.path.exists(alias_file_path):
        with open(alias_file_path, 'r') as file:
            for line in file:
                alias, command = line.strip().split("=", 1)
                aliases[alias] = command

    get_command = True
    sudo = False

    while True:
        show_dir = "/" + os.path.relpath(current_dir, local_dir)
        if show_dir == f"/home/{username}":
            show_dir = "~"
        elif show_dir == "/.":
            show_dir = "/"
            
        if get_command == True:
            full_cmd = input(f"| ({username}@{hostname})-[{show_dir}]\n| $ ").split()
            if not full_cmd:
                continue

            # Check if the command is an alias
            if cmd in aliases:
                full_cmd = aliases[cmd].split() + full_cmd[1:]
                cmd = full_cmd[0]
        
            print("")
            
        else:
            get_command = True
            
        
        cmd = full_cmd[0]
        skip_line = False
        
        if cmd == "help":
            if len(full_cmd) > 1:
                print("Command doesn't take any arguments.")
            else:
                print("Commands:")
                print("  help - Display this help message.")
                print("  ls [dir] - List files in current or specified directory.")
                print("  cd <dir> - Change directory.")
                print("  cat <file> - Print file contents.")
                print("  mkdir <dir> - Create a new directory.")
                print("  clear - Clear the terminal screen.")
                print("  alias <command> <new_alias> - Create an alias for a command.")
                print("  nano <file> - Create or edit a file using a simple text editor.")
                print("  exit - Exit the shell.")
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
                    print(f"Alias '{alias_to_delete}' deleted.")
                else:
                    print(f"Alias '{alias_to_delete}' does not exist.")
            elif len(full_cmd) != 3:
                print("Usage: alias <command> <new_alias>, alias show, or alias delete <alias_name>")
            else:
                command, alias = full_cmd[1], full_cmd[2]
                if alias in aliases:
                    print(f"Alias '{alias}' already exists for command '{aliases[alias]}'.")
                elif command in aliases.values():
                    print(f"Command '{command}' is already aliased to '{list(aliases.keys())[list(aliases.values()).index(command)]}'.")
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
                        if os.path.commonpath([new_dir, local_dir]) != local_dir:
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
                    with open(full_cmd[1], 'r') as file:
                        print(file.read())
                except FileNotFoundError:
                    print(f"No such file: '{full_cmd[1]}'")
        elif cmd == "mkdir":
            if len(full_cmd) != 2:
                print("Usage: mkdir <dir>")
            else:
                try:
                    target_dir = os.path.join(current_dir, full_cmd[1])
                    os.makedirs(target_dir, exist_ok=True)
                    print(f"Directory '{target_dir}' created.")
                except Exception as e:
                    print(f"Error creating directory: {e}")
        elif cmd == "nano":
            import texteditor

            if len(full_cmd) != 2:
                print("Usage: nano <file>")
            else:
                try:
                    file_path = os.path.join(current_dir, full_cmd[1])
                    
                    if not os.path.exists(file_path):
                        with open(file_path, 'w') as file:
                            pass
                    
                    edited_content = texteditor.open(filename=file_path)
                    
                    # If you want to write content programmatically (optional):
                    # with open(file_path, 'w') as file:
                    #     file.write(edited_content)
                    
                except FileNotFoundError:
                    print(f"No such file: '{full_cmd[1]}'")
                except Exception as e:
                    print(f"Error using texteditor: {e}")
                    
        elif cmd == "rm":
            if len(full_cmd) < 2 or len(full_cmd) > 3:
                print("Usage: rm <file> or rm -rf <folder>")
            elif len(full_cmd) == 2:
                try:
                    file_path = os.path.join(current_dir, full_cmd[1])
                    if os.path.isdir(file_path):
                        if not os.listdir(file_path):
                            os.rmdir(file_path)
                            print(f"Empty folder '{full_cmd[1]}' removed.")
                        else:
                            print(f"Folder '{full_cmd[1]}' is not empty. Use 'rm -rf <folder>' to remove with all contents.")
                    os.remove(file_path)
                    print(f"File '{full_cmd[1]}' removed.")
                except FileNotFoundError:
                    print(f"No such file or directory: '{full_cmd[1]}'")
                except Exception as e:
                    print(f"Error removing file or folder: {e}")
                    
            elif len(full_cmd) == 3 and full_cmd[1] == "-rf":
                try:
                    folder_path = os.path.join(current_dir, full_cmd[2])
                    if os.path.isdir(folder_path):
                        shutil.rmtree(folder_path)
                        print(f"Folder '{full_cmd[2]}' and its contents removed.")
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
                else:
                    print(f"{username} is not in the sudoers file.")
        elif cmd == "apt":
            sources_file_path = os.path.join(main_dir, "Otrace", "programs", "apt", "sources")
            
            if not len(full_cmd) == 3:
                print("Usage: apt <option> <program>")
            elif sudo == False:
                print("Permission denied.")
            else:
                if full_cmd[1] == "add":
                    author = full_cmd[2]
                    with open(sources_file_path, 'a') as file:
                        file.write(author = "\n")
        else:
            print("Invalid command. Type 'help' for a list of commands.")
            
        if not skip_line == True:
            print("")
        
#################################################################################