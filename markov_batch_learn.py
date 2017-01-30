from __future__ import unicode_literals
import argparse
import os
from cobe.brain import Brain

if __name__ == "__main__":

    bots = ["ames", "bojii", "diderobot", "ekimbot", "harbot", "hubbot", "nopebot", "memebot",
            "pyheufybot", "re_heufybot", "heufybot", "pymoronbot", "moronbot", "robobo", "safebot", "unsafebot"]

    parser = argparse.ArgumentParser(description="A script to quickly teach a new markov brain from a folder of text files.")
    parser.add_argument("-f", "--folder", help="The folder to read through.", type=str)
    parser.add_argument("-b", "--brainfile", help="The filename to use for the brain.", type=str)
    options = parser.parse_args()

    brain = Brain(options.brainfile)

    brain.start_batch_learning()
    for filename in os.listdir(options.folder):
        print os.path.join(options.folder, filename)
        with open(os.path.join(options.folder, filename)) as current_file:
            lines = current_file.readlines()
            for line in lines:
                templine = line.decode("utf-8")
                if templine[templine.find("]")+1:].lstrip().startswith("<"):
                    newline = templine[templine.find("]")+1:].lstrip()
                    if newline[newline.find("<"):newline.find(">")+1].lower() not in bots:
                        if newline.find(">") != -1:
                            brain.learn(newline[newline.find(">")+1:])

    brain.stop_batch_learning()
