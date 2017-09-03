from __future__ import unicode_literals
import argparse
import datetime
import logging
import os
import sys
import unicodedata
from cobe.brain import Brain
from stringutils import delta_time_to_string

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
    logger.info("Consolidating log files for easy learning...")
    try:
        consolidate_log_files(folder, "temp.txt")
    except Exception:
        logger.exception("Exception during file reading!")
    logger.info("File reading done, beginning brain batch learn...")
    with open("temp.txt") as temp_file:
        full_log_lines = temp_file.readlines()
        brain.start_batch_learning()
        for line in full_log_lines:
            brain.learn(line)
        brain.stop_batch_learning()
    logger.info("Brain learned {:,} lines.".format(len(full_log_lines)))
    logger.info("Execution time: {}".format(delta_time_to_string((datetime.datetime.now() - start_time), resolution="s")))

    return brain


def consolidate_log_files(folder, output_filename):
    for log_file in os.listdir(folder):
        try:
            with open(output_filename, b"a+") as output_file:
                with open(os.path.join(folder, log_file)) as current_log:
                    raw_lines = current_log.readlines()
                    filtered_lines = filter_log_lines(raw_lines)
                    for line in filtered_lines:
                        try:
                            output_file.write(line + "\n")
                        except Exception:
                            # this should only happen if we encounter weird chars, which we can probably skip
                            continue
        except Exception:
            raise
    return output_filename


def filter_log_lines(raw_lines):
    filtered_lines = []
    for line in raw_lines:
        decoded_line = line.decode("utf-8", errors="ignore")
        if "://" in decoded_line or "www." in decoded_line or ".com" in decoded_line:
            # let's try our damndest to ignore things that contain hyperlinks
            continue
        newline = decoded_line.split("]", 1)[1].strip()
        nick_start_index = newline.find("<")
        nick_end_index = newline.find(">")
        for char in newline:
            if unicodedata.category(char)[0] not in ["L", "M", "N", "P", "S", "Z"]:
                # if character isn't a letter, mark, number, punctuation, symbol, or separator, remove it
                newline = newline.replace(newline, "")
        if nick_start_index == 0 and nick_end_index != -1 and newline[nick_start_index:nick_end_index + 1].lower() not in bots:
            filtered_lines.append(newline[nick_end_index + 1:].lstrip())
    for line in filtered_lines:
        if line == "" or line == "\n":
            filtered_lines.remove(line)
        elif unicodedata.category(line[0])[0] != "L":
            filtered_lines.remove(line)
            # try to remove things that look like bot commands
    return filtered_lines


def consolidate_single_nick(folder, nick, filename):
    for log_file in os.listdir(folder):
        try:
            with open(filename, b"a+") as output_file:
                with open(os.path.join(folder, log_file)) as current_log:
                    raw_lines = current_log.readlines()
                    filtered_lines = []
                    for line in raw_lines:
                        decoded_line = line.decode("utf-8", errors="ignore")
                        if "://" in decoded_line:
                            continue
                        newline = decoded_line.split("]", 1)[1].strip()
                        nick_start_index = newline.find("<")
                        nick_end_index = newline.find(">")
                        for char in newline:
                            if unicodedata.category(char)[0] not in ["L", "M", "N", "P", "S", "Z"]:
                                # if character isn't a letter, mark, number, punctuation, symbol, or separator, remove it
                                newline = newline.replace(newline, "")
                        if nick_start_index == 0 and nick_end_index != -1 and nick in newline[nick_start_index:nick_end_index + 1].lower():
                            filtered_lines.append(newline[nick_end_index + 1:].lstrip())
                    for line in filtered_lines:
                        try:
                            output_file.write(line + "\n")
                        except Exception:
                            # this should only happen if we encounter weird chars, which we can probably skip
                            continue
        except Exception:
            raise
    return filename


def batch_learn_from_singlenick(folder, nick, brainfile):
    brain = Brain(brainfile)

    logger = logging.getLogger("markov_batch_learn")
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%H:%M:%S'))
    stream_handler.setLevel(logging.INFO)
    logger.addHandler(stream_handler)

    start_time = datetime.datetime.now()
    logger.info("Consolidating log files for easy learning...")
    try:
        consolidate_single_nick(folder, nick, "temp.txt")
    except Exception:
        logger.exception("Exception during file reading!")
    logger.info("File reading done, beginning brain batch learn...")
    with open("temp.txt") as temp_file:
        full_log_lines = temp_file.readlines()
        brain.start_batch_learning()
        for line in full_log_lines:
            brain.learn(line)
        brain.stop_batch_learning()
    logger.info("Brain learned {:,} lines.".format(len(full_log_lines)))
    logger.info(
        "Execution time: {}".format(delta_time_to_string((datetime.datetime.now() - start_time), resolution="s")))

    return brain


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script to quickly teach a new markov brain from a folder of text files.")
    parser.add_argument("target_folder", help="The folder to read through.", type=str)
    parser.add_argument("filename", help="The filename to use for output.", type=str)
    parser.add_argument("-s", "--singlenick", metavar="nick", help="Only use lines from this (and others like it) in the logs.", type=str)
    parser.add_argument("-p", "--parse", help="Don't train a brain, instead output logs as a file of newline-separated text.", action="store_true")
    options = parser.parse_args()

    if options.parse and not options.singlenick:
        consolidate_log_files(options.target_folder, options.filename)
    elif options.singlenick and not options.parse:
        batch_learn_from_singlenick(options.target_folder, options.singlenick, options.filename)
    elif options.singlenick and options.parse:
        consolidate_single_nick(options.target_folder, options.singlenick, options.filename)
    else:
        markov_batch = batch_learn(options.target_folder, options.filename)
