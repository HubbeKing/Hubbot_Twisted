Hubbot_Twisted
==============

A mostly modular IRC bot written using the Twisted library.

Because of Twisted, Windows users will most likely need to install the Microsoft Visual C++ Compiler for Python 2.7
(http://www.microsoft.com/en-us/download/details.aspx?id=44266)

While there should not be much in the bot that will not function under Windows, it has only been properly tested on Linux systems.

Please be aware that the default behaviour of the bot is to load all existing modules on startup.
This can be changed in the config file.

HOW TO USE:

1. Install your preferred version of Python 2.7
2. Install a virtualenv and activate it
3. Run `pip install -r requirements.txt`. inside said virtualenv
4. Create a config file from hubbot.yaml.example
5. Use said virtualenv to run `python app.py -c configFileName`


MODULE SYSTEM:

The module system for the bot works like this:
- Modules are loaded by the ModuleHandler class, from the Modules directory.
- The directory is, for the moment, hardcoded. It also does not support subdirectories.
- The ModuleHandler considers anything inheriting from ModuleInterface to be a module
- Further info on how to write modules can be gleaned from the ModuleInterface and ModuleHandler classes


ERROR LOGGING:

By default, INFO level logging is done in the `hubbot/logs` folder, using the server name as the filename.
These server logs are kept for 7 days on a `rotatingFileHandler`.

In addition, any errors and exceptions are logged in `hubbot.log` in the root directory.
This filename can be changed with the optional `app.py -l logFileName` command line argument