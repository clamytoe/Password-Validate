import datetime
import json
from getpass import getpass
from pathlib import Path
from string import ascii_letters as lowercase
from string import ascii_uppercase as uppercase
from string import digits
from string import punctuation as special

from utils import check_length, hashit, not_in_dict

# special = '!.*;$#@'  # These were specifically mentioned

PASSWD_FILE = '.validated_passwords'


class Account:
    CHAR_TYPES = [digits, lowercase, special, uppercase]

    def __init__(self, fullname, username):
        self.first_name = fullname.split()[0]
        self.last_name = fullname.split()[-1]
        self.username = username
        self.used_passwords = {}

    def _check_characters(self, password):
        found = [0] * len(self.CHAR_TYPES)
        count = 0

        for i, char_type in enumerate(self.CHAR_TYPES):
            for char in password:
                if found[i] == 0:
                    if char in char_type:
                        count += 1
                        found[i] = 1
                        break
        return True if count >= 3 else False

    def _check_used(self, password):
        age = None
        hashed = hashit(password)
        used = True if hashed in self.used_passwords else False
        if used:
            today = datetime.datetime.today()
            stored = self.used_passwords[hashed]
            age = (today - stored).days

        return True if age is None or age >= 365 else False

    def _not_using_username(self, password):
        if self.username.lower() in password.lower():
            return False
        return True

    def _not_using_name(self, password):
        for name in [self.first_name, self.last_name]:
            if name.lower() in password.lower():
                return False
        return True

    def store(self, password):
        valid = self._check_used(password)
        if valid:
            hashed = hashit(password)
            self.used_passwords[hashed] = datetime.datetime.today()
            data = {
                'name': f'{self.first_name} {self.last_name}',
                'username': self.username,
                'passwords': self.used_passwords,
            }
            with open(PASSWD_FILE, 'w') as file:
                json.dump(data, file, default=str)
            print('The password has been stored. Bye!')
        else:
            print('Password not saved, already in use.')

    def validate(self, password):
        msg = 'The password'
        checks = [
            check_length,
            not_in_dict,
            self._check_characters,
            self._not_using_name,
            self._not_using_username,
            self._check_used,
        ]
        messages = [
            f'{msg} is not long enough.',
            f'{msg} is a commonly used one.',
            f'{msg} does not contain 3 of the 4 required character types.',
            f'{msg} is using part of your name.',
            f'{msg} is using your username.',
            f'{msg} was used less than a year ago.'
        ]

        for i, check in enumerate(checks):
            valid = check(password)
            if not valid:
                print(messages[i])
                return False
        return True


def check_password(user):
    while True:
        password = getpass('Password: ')

        if user.validate(password):
            password2 = getpass('Confirm it: ')
            if password == password2:
                choice = input('Would you like to store it? ([y]/n)')
                if not choice or choice.lower().startswith('y'):
                    user.store(password)
                    # print(user.used_passwords)
                    break
                else:
                    print('Ok, bye!')
                    break
            else:
                print('Sorry, the passwords did not match...')


def load_data():
    with open(PASSWD_FILE, 'r') as file:
        data = json.load(file)
    name = data['name']
    username = data['username']
    user = Account(name, username)
    if data['passwords']:
        user.used_passwords = data['passwords']
        for key, value in data['passwords'].items():
            date = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')
            user.used_passwords[key] = date
    return user


def main():
    pw_file = Path(PASSWD_FILE)

    if pw_file.is_file():
        user = load_data()
    else:
        name = input('First and Last name: ')
        username = input('Username: ')
        user = Account(name, username)

    try:
        check_password(user)
    except KeyboardInterrupt:
        print('\n\nProgram aborted by user. Exiting...\n')
        exit()


if __name__ == '__main__':
    main()
