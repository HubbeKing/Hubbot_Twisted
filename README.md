Hubbot_Twisted
==============

A rewrite of NopeBot in Twisted, using PyMoronBot as a starting point.

If you want to use this, you'll need Python 2.
Some of the functions (hugs/headcanon) rely on a sqlite3 data/data.db file.

A function for generating a blank file for these is included (newDB.py)

The bot can be started using app.py, the default config file used is hubbot.yaml

This can be easily created from hubbot.yaml.example, or another one can be used with the -c argument

HOW TO USE:

1: Install your preferred version of Python 2
2: Install a virtualenv and activate it
3: Run pip install -r requirements.txt inside said virtualenv
4: Create a config file from hubbot.yaml.example
5: Use said virtualenv to run app.py -c <configfilename>