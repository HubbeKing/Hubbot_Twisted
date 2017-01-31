from __future__ import unicode_literals
import argparse
import datetime
import logging
import os
import sys
from cobe.brain import Brain
from hubbot.Utils.stringutils import delta_time_to_string

bots = ["ames", "bojii", "diderobot", "ekimbot", "harbot", "hubbot", "nopebot", "memebot", "pyheufybot",
        "re_heufybot", "heufybot", "pymoronbot", "moronbot", "robobo", "safebot", "unsafebot"]


def batch_learn(folder, brainfile):
    """
    @type folder: unicode
    @type brainfile: unicode

    Processes all files in the folder directory and teaches the brainfile accordingly.
    Files in the directory must be IRC logs in the following format:
    [HH:MM:ss] <nick> line
    [HH:MM:ss] <othernick> otherline

    Tries to avoid learning from bots by using a list of botnames used in the DBCommunity IRC.
    Returns the taught brain.

    @return: cobe.brain.Brain
    """

    brain = Brain(brainfile)

    logger = logging.getLogger("markov_batch_learn")
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%H:%M:%S'))
    stream_handler.setLevel(logging.INFO)
    logger.addHandler(stream_handler)

    start_time = datetime.datetime.now()

    for filename in os.listdir(folder):
        file_start_time = datetime.datetime.now()
        brain.start_batch_learning()
        logger.info("Parsing {!r}".format(filename))
        try:
            with open(os.path.join(folder, filename)) as current_file:
                lines = current_file.readlines()
                parsed_lines = filter_log_lines(lines)
                for line in parsed_lines:
                    brain.learn(line)
        except:
            logger.exception("Error when processing file {!r}".format(filename))
        finally:
            brain.stop_batch_learning()
        logger.info("Done, {} elapsed".format(delta_time_to_string((datetime.datetime.now() - file_start_time), resolution="s")))
    logger.info("All done, total execution time: {}".format(delta_time_to_string((datetime.datetime.now() - start_time), resolution="s")))
    return brain


def filter_log_lines(raw_lines):
    parsed_lines = []
    for line in raw_lines:
        templine = line.decode("utf-8", errors="ignore")
        newline = templine.split("]", 1)[1].strip()
        nick_start_index = newline.find("<")
        nick_end_index = newline.find(">")
        if "://" not in newline and nick_start_index == 0 and nick_end_index != -1 and newline[nick_start_index:nick_end_index + 1].lower() not in bots:
            parsed_lines.append(newline[nick_end_index + 1:].lstrip())
    return parsed_lines


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script to quickly teach a new markov brain from a folder of text files.")
    parser.add_argument("-f", "--folder", help="The folder to read through.", type=str)
    parser.add_argument("-b", "--brainfile", help="The filename to use for the brain.", type=str)
    options = parser.parse_args()

    markov_batch = batch_learn(options.folder, options.brainfile)
