# 🚀 0trace

**0trace** is an immersive hacking simulation game where players navigate a virtual Linux-based operating system to hack NPCs or other players. The game combines strategy, problem-solving, and technical skills to create a realistic and engaging experience.

---

## 🌟 Features

- 🖥️ **Realistic OS Simulation**: Interact with a Linux-like environment to execute commands and scripts.
- 🧩 **Hacking Challenges**: Solve puzzles and exploit vulnerabilities to achieve objectives.
- 🤝 **Multiplayer Mode**: Compete or collaborate with other players in real-time.
- 🤖 **Dynamic NPCs**: Hack AI-driven characters with unique behaviors and defenses.
- 🛠️ **Customizable Tools**: Build and upgrade your hacking arsenal to suit your playstyle.
- 🌐 **Cross-Platform**: Works on Linux, macOS, and Windows.
- ⚡ **Lightweight and Fast**: Minimal dependencies and optimized for performance.

---

## 📋 Requirements

To run **0trace**, ensure your system meets the following requirements:

- **Python**: Version 3.8 or higher
- **Python PIP**: Version 25.0.1 or higher
- **Git**: Version 2.49.0 or higher 
- **Dependencies**: Install required Python packages using `pip install -r requirements.txt`
- **Memory**: At least 2GB of RAM
- **Storage**: At least 500MB of free disk space

---

## ⬇️ Installation Guide for required software
#### ⚡ Install Git

##### 🪟 Windows (via Winget)
```bash
winget install --id Git.Git -e --source winget
```

This will install the latest Git version and make it available in Command Prompt and PowerShell.

##### 🍎 macOS (via Homebrew)
First, install Homebrew if it’s not already installed:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then install Git:
```bash
brew install git
```

##### 🐧 Linux

###### Ubuntu / Debian
```bash
sudo apt update
sudo apt install git
```

###### Fedora
```bash
sudo dnf install git
```

###### Arch / Manjaro
```bash
sudo pacman -S git
```

#### ⚡ Install Python 3.13 and Python PIP

##### 🪟 Windows (via Winget)
```bash
winget install --id Python.Python.3 -e --source winget
```

This installs the latest stable Python 3 and adds it to your system PATH.

##### 🍎 macOS (via Homebrew)
First, install Homebrew if it’s not already installed:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then install Python 3:
```bash
brew install python
```

##### 🐧 Linux

###### Ubuntu / Debian
```bash
sudo apt update
sudo apt install python3
```

###### Fedora
```bash
sudo dnf install python3
```

###### Arch / Manjaro
```bash
sudo pacman -S python
```

---

## 🔄 Upate required software

##### 🪟 Windows (via Winget)
```bash
winget upgrade --id Git.Git -e --source winget
winget upgrade --id Python.Python.3 -e --source winget
```

##### 🍎 macOS (via Homebrew)
```bash
brew upgrade git
brew upgrade python
```

##### 🐧 Linux

###### Ubuntu / Debian
```bash
sudo apt update
sudo apt install --only-upgrade git
sudo apt install --only-upgrade python3
```

> 💡 To get the very latest Python versions on Ubuntu, consider using the [deadsnakes PPA](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa) or compiling from source.

###### Fedora
```bash
sudo dnf upgrade git
sudo dnf upgrade python3
```

###### Arch / Manjaro
```bash
sudo pacman -Syu git python
```

---

## 🛠️ Installation of the program

### Step 1: Clone the Repository
```bash
git clone https://github.com/CodingPengu007/0trace.git
cd 0trace
```

### Step 2: Start the Program

#### On Linux / macOS
```bash
python3 main.py
```

#### On Windows
Run the program with Python:
```bash
python main.py
```

### Step 3: Activate the venv and start the program again

#### On Linux / macOS
```bash
source Otrace_venv/bin/activate
python3 main.py
```

#### On Windows
Run the program with Python:
```bash
Otrace_venv/Scripts/activate
python main.py
```

---

## 🎮 Gameplay

Launch the game with the following command:

#### On Linux / macOS
```bash
python3 main.py
```

#### On Windows
Run the program with Python:
```bash
python main.py
```

---

## 🤝 Contributing

Contributions are welcome! Follow these steps to get started:

1. **Fork** the repository.
2. **Create a new branch** for your feature or bug fix.
3. **Submit a pull request** with a detailed description.

---

## 📜 License

This project is licensed under the [GNU General Public License v3.0](LICENSE).  
The GNU GPL v3.0 ensures that this project remains open source. Any modifications or derivative works must also be open source and distributed under the same license.

### **Third-Party Dependencies and Licenses:**

- The graphical elements in this program were generated by the **Tkinter Designer** by [Parth Jadhav](https://github.com/ParthJadhav/Tkinter-Designer).

- **Tkinter Designer License (BSD 3-Clause License)**:

```
BSD 3-Clause License

Copyright (c) 2021, Parth Jadhav
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
```

---

## ⚠️ Disclaimer

This game is for **entertainment purposes only**. Any resemblance to real-world hacking scenarios is purely coincidental.

---

## 🙌 Credits

Special thanks to the following:

- **Parth Jadhav** for creating the **Tkinter Designer** we used to create graphical elements in this project.
- The **open-source community** for providing invaluable libraries and resources.
- **Beta Testers** for their feedback and support during development.

### Team Members:

- **CodingPengu007** - Lead Developer
- **lionbaum**       - Junior Software Engineer
- **DonerKebab1231** - UI/UX Designer

---

## 📬 Contact

For questions or support, please open an issue on the [GitHub repository](https://github.com/CodingPengu007/0trace).

---
