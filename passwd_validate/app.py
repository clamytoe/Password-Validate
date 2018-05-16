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

from passwd_validate.account import Account, PASSWD_FILE


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
                    break
                else:
                    print("Ok, bye!")
                    break
            else:
                print("Sorry, the passwords did not match...")


def get_name():
    """
    Get's the users first and last name.
    :return: String, name of the user
    """
    while True:
        name = input("First and Last name: ")
        if len(name.split()) > 1:
            return name
        else:
            print("You're first and last name are required!")


def get_username():
    """
    Get's the users company's username.
    :return: String, account username
    """
    username = input("Username: ")
    return username


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

    try:
        if pw_file.is_file():
            user = load_data()
        else:
            name = get_name()
            username = get_username()
            user = Account(name, username)
            user.save()

        check_password(user)
    except KeyboardInterrupt:
        print("\n\nProgram aborted by user. Exiting...\n")
        exit()


if __name__ == "__main__":
    main()
