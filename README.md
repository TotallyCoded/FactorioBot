# Factorio Discord Bot

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

![Header Image][header-image.png]


We are coding this bot as far of the Discord Hack Week. It allows a server to play and control a character in factorio from a discord channel as a collaborative experience. 

A large group of users should be able to each send commands to a factorio character and together build the world.

This bot is a bit of a hack.

# Features
## Factorio Interactions
- [x] Player movement
- [x] Craft items
- [x] Place items
- [x] Pick up items
- [x] Send chat message
- [x] Set research
- [x] View inventory and tech tree GUI's 
## Additional features
- [x] Take screenshots  
- [x] Customisable command cooldowns
- [x] Tasks executed in a queue
- [x] Order of the queue displayed upon request
- [x] Help commands where item/tech names are required
    
# Setup
## Dependencies
- `python 3.6 or higher`
- `discord.py`
- `pyautogui`
- `watchdog`

## Install
```commandline
git clone https://github.com/TotallyCoded/FactorioBot.git
cd FactorioBot\FactorioBot
pip install requirements.txt
```

# Usage
1. Create an application and bot at https://discordapp.com/developers/applications/
2. Create a `config.py` file with:

    ```py
    token = "token-here"
    factorio_user_data='%Appdata%\Factorio-or-your-folder-here'
    ```
3. Run setup.py (this will install the supplied bridge mod)
4. Start up a factorio fullscreen and open/create a save.
5. Run main.py (FactorioBot directory)
6. Enjoy!

# Technical
![Component Diagram][technical-diagram.png]

## Journey
We originally looked at having the bot communicate directly with a mod over a internet connection similar to here [Clusterio](https://github.com/Danielv123/factorioClusterio) and the concept in this [reddit](https://www.reddit.com/r/factorio/comments/5g3qiz/modding_how_to_make_internet_connected_mods_like/) post.

They work through RCON and writing to a log file. 
However we quickly found that movement through the factorio lua api would be extremely difficult to implement. To solve this challenge, we decided to make python act as a macro controlling the keyboard and mouse into factorio allow us to implement walking very easily.

A fun challenge we encountered was that commands to control factorio were running at the same time and conflicting with each other. To solve this we designed a command queue which queue the commands from users asynchronously until all previous commands have been run.

Next we started work on a lua mod as that was required to allow us to craft items and complete other task in the game such as setting research and placing items. We had some initial challenges learning the api and how to interact with it. Initially we again explored RCON to communicate with the lua api and also hacking on_console_chat however both options were messy. On further research we discovered that we could add custom commands which we could trigger from pyautogui.  

To return data back to the python bot we use a method seen in [Clusterio](https://github.com/Danielv123/factorioClusterio) of logging output to `script-output/` and then reading it from our code. Here we had to implement a file watch using the library `watchdog` to fix a race condition where discord read the log file before our mod wrote it.

[header-image.png]: https://i.imgur.com/ZW2V92t.png
[technical-diagram.png]: https://i.imgur.com/cyJ808U.png


