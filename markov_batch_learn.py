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

    for log_file in os.listdir(folder):
        file_start_time = datetime.datetime.now()
        brain.start_batch_learning()
        logger.info("Parsing {!r}".format(log_file))
        try:
            with open(os.path.join(folder, log_file)) as current_log:
                raw_lines = current_log.readlines()
                filtered_lines = filter_log_lines(raw_lines)
                for line in filtered_lines:
                    brain.learn(line)
        except:
            logger.exception("Error when processing file {!r}".format(log_file))
        finally:
            brain.stop_batch_learning()
        logger.info("Done, {} elapsed".format(delta_time_to_string((datetime.datetime.now() - file_start_time), resolution="s")))
    logger.info("All done, total execution time: {}".format(delta_time_to_string((datetime.datetime.now() - start_time), resolution="s")))
    return brain


def filter_log_lines(raw_lines):
    filtered_lines = []
    for line in raw_lines:
        decoded_line = line.decode("utf-8", errors="ignore")
        if "://" in decoded_line:
            continue
        newline = decoded_line.split("]", 1)[1].strip()
        nick_start_index = newline.find("<")
        nick_end_index = newline.find(">")
        if nick_start_index == 0 and nick_end_index != -1 and newline[nick_start_index:nick_end_index + 1].lower() not in bots:
            filtered_lines.append(newline[nick_end_index + 1:].lstrip())
    return filtered_lines


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script to quickly teach a new markov brain from a folder of text files.")
    parser.add_argument("-t", "--target_folder", help="The folder to read through.", type=str)
    parser.add_argument("-f", "--filename", help="The filename to use for output.", type=str, default="output")
    parser.add_argument("-p", "--parse", help="Don't train a brain, instead output logs as a file of newline-separated text.", action="store_true")
    options = parser.parse_args()

    if options.parse:
        with open(options.filename, "w") as output:
            for filename in os.listdir(options.target_folder):
                with open(os.path.join(options.target_folder, filename)) as current_file:
                    lines = current_file.readlines()
                    parsed_lines = filter_log_lines(lines)
                    for parsed_line in parsed_lines:
                        output.write(parsed_line + "\n")

    else:
        markov_batch = batch_learn(options.target_folder, options.filename)
