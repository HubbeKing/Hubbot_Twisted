Hubbot_Twisted
==============

A mostly modular IRC bot written using the Twisted library.

While there should not be much in the bot that will not function under Windows, it has only been properly tested on Linux systems.

Please be aware that the default behaviour of the bot is to load all existing modules on startup.
This can be changed in the config file.

HOW TO USE:

1. Create a config from `hubbot.toml.example`
2. Create a `docker-compose.yml` file from `docker-compose.example.yml`
3. Run the bot using `docker-compose` -Note the volume mounts for the `data` and `logs` folders.
4. ???
5. Profit?


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