Hubbot_Twisted
==============

A mostly modular IRC bot written using the Twisted library.

Because of Twisted, Windows users will most likely need to install the Microsoft Visual C++ Compiler for Python 2.7
(http://www.microsoft.com/en-us/download/details.aspx?id=44266)

Please be aware that the default behaviour of Hubbot is to load all existing modules on startup.
This can be changed in the config file.

HOW TO USE:

1. Install your preferred version of Python 2
2. Install a virtualenv and activate it
3. Run `pip install -r requirements.txt`. inside said virtualenv
4. Create a config file from hubbot.yaml.example
5. Use said virtualenv to run `python app.py -c configFileName`


MODULE SYSTEM:

The module system for Hubbot works like this:
- Modules are loaded by the ModuleHandler class, from the Modules directory.
- The directory is, for the moment, hardcoded. It also doesn't support subdirectories.
