# _*_ coding: utf-8 _*_
"""
password-validate.utils
-----------------------
This module provides utility functions that are used within password_validate
that are also useful for external consumption.
"""
import hashlib

from os.path import abspath, dirname, join

DICTIONARY_LOC = "dictionary_files"
DICTIONARY = "dictionary.txt"
PHPBB = "phpbb.txt"
ROCKYOU = "rockyou.txt"
DICTS = [
    DICTIONARY,
    PHPBB,
]


def hashit(password):
    """
    Hashes any string sent to it with sha512.
    :param password: String to hash
    :return: String with a hexdigest of the hashed string.
    """
    hash_object = hashlib.sha512()
    hash_object.update(password.encode("utf-8"))
    return hash_object.hexdigest()


def not_in_dict(password):
    """
    Parses several dictionary files to see if the provided password is included
    within them.

    If the dictionary file contains any words that are under five characters in
    length, they are skipped. If the string is found, this is considered to be
    a failed check and therefore not a valid password.
    :param password: String to check
    :return: Boolean, True if not found, False if it is
    """
    for passwd_file in DICTS:
        dict_words = read_file(passwd_file)
        for word in dict_words:
            if "dictionary" in passwd_file and len(word) < 5:
                # skip common words under 5 characters long
                break
            if password in word:
                return False
    return True


def read_file(filename):
    """
    Helper function that simple iterates over the dictionary files.
    :param filename: String with the path and filename of the dictionary
    :return: String generator with each line of the dictionary
    """
    file_loc = dirname(abspath(__file__))
    data_loc = join(file_loc, DICTIONARY_LOC, filename)
    try:
        with open(data_loc) as file:
            for line in file:
                yield line.rstrip()
    except UnicodeDecodeError:
        # LOL, like my hack around this one??
        yield "error"
