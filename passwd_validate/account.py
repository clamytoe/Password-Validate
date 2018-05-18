# _*_ coding: utf-8 _*_
import datetime
import json

from string import ascii_letters as lowercase
from string import ascii_uppercase as uppercase
from string import digits
from string import punctuation as special

from passwd_validate.utils import hashit, not_in_dict

PASSWD_FILE = ".pval_db"


class Account:
    """
    Account object that is used to store your name, username, and previously
    used password hashes. Storing this information makes using the program a
    lot easier since you won't have to repeatedly enter your information each
    time that you use it.

    No passwords are stored and are only in memory while the program is being
    used.
    """
    CHAR_TYPES = [digits, lowercase, special, uppercase]

    def __init__(self, fullname, username):
        self.first_name = fullname.split()[0]
        self.last_name = fullname.split()[-1]
        self.username = username
        self.used_passwords = {}

    def __len__(self):
        return len(self.used_passwords)

    def __repr__(self):
        desc = f"Account(firstname='{self.first_name} {self.last_name}', " \
               f"username='{self.username})'"
        return desc

    def _check_characters(self, password):
        """
        Verifies that at least three different types of characters in the
        policy are met.
        :param password: String of the password to check
        :return: Boolean, True if it passes the check, False otherwise
        """
        return sum(any(char in char_type for char in password)
                   for char_type in self.CHAR_TYPES) >= 3

    def _check_used(self, password):
        """
        Checks to see if the password has already been used. If it has, it will
        check and see how long ago it was used, if that length of time is less
        than 365 days, it will Fail.
        :param password: String of the password to check
        :return: Boolean, True if it passes the check, False otherwise
        """
        hashed = hashit(password)
        if hashed in self.used_passwords:
            today = datetime.datetime.today()
            stored = self.used_passwords[hashed]
            age = (today - stored).days
            return age >= 365
        return True

    @staticmethod
    def _check_length(password):
        """
        Checks to see if the password meets the minimum length policy.
        :param password: String of the password
        :return: Boolean, True if it meets the requirement, False otherwise
        """
        return len(password) >= 10

    def _not_using_username(self, password):
        """
        Checks to see if the username is being used in the password.
        :param password: String of the password to check
        :return: Boolean, True if it passes the check, False otherwise
        """
        return self.username.lower() not in password.lower()

    def _not_using_name(self, password):
        """
        Checks to see if the first or last name of the user is used in the
        password.
        :param password: String of the password to check
        :return: Boolean, True if it passes the check, False otherwise
        """
        for name in [self.first_name, self.last_name]:
            if name.lower() in password.lower():
                return False
        return True

    def save(self):
        """
        Saves the Account object to disk.
        :return: None
        """
        data = {
            "name": f"{self.first_name} {self.last_name}",
            "username": self.username,
            "passwords": self.used_passwords,
        }
        with open(PASSWD_FILE, "w") as file:
            json.dump(data, file, default=str)

    def store(self, password):
        """
        Stores the password hash.
        :param password: String of password to hash and store
        :return: None
        """
        valid = self._check_used(password)
        if valid:
            hashed = hashit(password)
            self.used_passwords[hashed] = datetime.datetime.today()
            self.save()
            print("The password has been stored.")
        else:
            print("Password not saved, already in use.")

    def validate(self, password):
        """
        Runs all of the necessary checks to validate the password.
        :param password: String of the password to validate
        :return: Boolean, True if it passes all checks and False otherwise
        """
        msg = "The password"
        checks = [
            self._check_length,
            self._check_characters,
            self._not_using_name,
            self._not_using_username,
            self._check_used,
            not_in_dict,
        ]
        messages = [
            f"{msg} is not long enough.",
            f"{msg} does not contain 3 of the 4 required character types.",
            f"{msg} is using part of your name.",
            f"{msg} is using your username.",
            f"{msg} was used less than a year ago.",
            f"{msg} is a commonly used one.",
        ]

        for i, check in enumerate(checks):
            valid = check(password)
            if not valid:
                # statement indicating which test failed
                print(messages[i])
                return False
        return True
