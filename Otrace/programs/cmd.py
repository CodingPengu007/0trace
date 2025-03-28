#################################################################################

import os
import Otrace as gm

#################################################################################

def line(username, hostname, current_dir, local_dir):
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
        
        else:
            get_command = True
            
        cmd = full_cmd[0]
            
        print("")
        
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
            elif len(full_cmd) != 3:
                print("Usage: alias <command> <new_alias> or alias show")
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
                    for item in os.listdir(target_dir):
                        print(item)
                except FileNotFoundError:
                    print(f"No such file or directory: '{target_dir}'")
        elif cmd == "cd":
            if len(full_cmd) != 2:
                print("Usage: cd <dir>")
            else:
                try:
                    new_dir = os.path.expanduser(full_cmd[1])
                    if new_dir == "..":
                        new_dir = os.path.dirname(current_dir)
                        if os.path.commonpath([new_dir, local_dir]) != local_dir:
                            print("Permission denied.")
                            print("")
                            continue
                    os.chdir(new_dir)
                    current_dir = os.getcwd()
                except FileNotFoundError:
                    print(f"No such file or directory: '{full_cmd[1]}'")
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
            if len(full_cmd) != 2:
                print("Usage: nano <file>")
            else:
                file_path = os.path.join(current_dir, full_cmd[1])
                try:
                    if not os.path.exists(file_path):
                        with open(file_path, 'w') as file:
                            pass
                    os.system('clear' if os.name == 'posix' else 'cls')
                    print(f"Editing file: {file_path}")
                    print("Enter your text below. Press Ctrl+D (EOF) to save and exit.")
                    print("")
                    with open(file_path, 'a') as file:
                        try:
                            lines = []
                            while True:
                                line = input()
                                lines.append(line + "\n")
                        except EOFError:
                            print("\nEnd of input detected. Saving file...")
                            file.writelines(lines)
                    print(f"File '{file_path}' saved.")
                    os.system('clear' if os.name == 'posix' else 'cls')
                except Exception as e:
                    print(f"Error editing file: {e}")
        elif cmd == "clear":
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
            if not len(full_cmd) == 3:
                print("Usage: apt <option> <program>")
            elif sudo == False:
                print("Permission denied.")
            else:
                if full_cmd[1] == "add":
                    author = full_cmd[2]
        else:
            print("Invalid command. Type 'help' for a list of commands.")
            
        print("")
        
#################################################################################