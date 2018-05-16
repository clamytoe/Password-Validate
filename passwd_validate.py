# _*_ coding: utf-8 _*_
"""
password_validate
-----------------
Little program to help with the creation of passwords that meet my company
password policy guidelines.

* characters >= 10
* 3 or more of the following: [uppercase, lowercase, number, '!.*;$#@']
* No common dictionary words (5 >= letters)
* Not in common password dictionary
* Not contain username
* Not contain any part of first name
* Not contain any part of last name
* Not reused within a year
"""
import datetime
import json
from getpass import getpass
from pathlib import Path
from string import ascii_letters as lowercase
from string import ascii_uppercase as uppercase
from string import digits
from string import punctuation as special

from utils import hashit, not_in_dict

# special = '!.*;$#@'  # These were specifically mentioned

PASSWD_FILE = ".validated_passwords"


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

    def _check_characters(self, password):
        """
        Verifies that at least three different types of characters in the
        policy are met.
        :param password: String of the password to check
        :return: Boolean, True if it passes the check, False otherwise
        """
        return sum(any(char in type for char in password)
                   for type in self.CHAR_TYPES) >= 3

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
        return False
    
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


def check_password(user):
    """
    CLI interaction with the user.
    :param user: Account object with the user's information
    :return: None
    """
    while True:
        password = getpass("Password: ")

        if user.validate(password):
            password2 = getpass("Confirm it: ")
            if password == password2:
                choice = input("Would you like to store it? ([y]/n)")
                if not choice or choice.lower().startswith("y"):
                    user.store(password)
                    # print(user.used_passwords)
                    break
                else:
                    print("Ok, bye!")
                    break
            else:
                print("Sorry, the passwords did not match...")


def load_data():
    """
    Loads the JSON data with the user's account information if found.
    :return: Account object with the user's information
    """
    with open(PASSWD_FILE, "r") as file:
        data = json.load(file)
    name = data["name"]
    username = data["username"]
    user = Account(name, username)

    # convert the timestamps into datetime objects
    if data["passwords"]:
        user.used_passwords = data["passwords"]
        for key, value in data["passwords"].items():
            date = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
            user.used_passwords[key] = date
    return user


def main():
    """
    Entry point into the program.

    It will check to see if data has been previously saved. If one is found, it
    will load it and create an Account object from it. If not, it will prompt
    the user for their full name and company username. With that it will create
    an Account.

    The Account object is then passed along to the check_password() function
    which will do the rest.
    :return: None
    """
    pw_file = Path(PASSWD_FILE)

    if pw_file.is_file():
        user = load_data()
    else:
        name = input("First and Last name: ")
        username = input("Username: ")
        user = Account(name, username)
        user.save()

    try:
        check_password(user)
    except KeyboardInterrupt:
        print("\n\nProgram aborted by user. Exiting...\n")
        exit()


if __name__ == "__main__":
    main()
