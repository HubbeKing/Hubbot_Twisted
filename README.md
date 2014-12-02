Hubbot_Twisted
==============

A rewrite of NopeBot in Twisted, using PyMoronBot as a starting point.

If you want to use this, you'll need Python 2.
Some of the functions (hugs/headcanon) rely on a sqlite3 data/data.db file.

A function for generating a blank file for these is included (newDB.py)

The bot can be started using app.py, the default config file used is hubbot.yaml

This can be easily created from hubbot.yaml.example, or another one can be used with the -c argument

Some of the bot (the update module) relies on the bot being run from a virtualenv present in env/
