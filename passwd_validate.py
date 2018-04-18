from getpass import getpass
from string import ascii_letters as lowercase
from string import ascii_uppercase as uppercase
from string import digits
from string import punctuation as special

# special = '!.*;$#@'  # These were specifically mentioned

ACTUAL_NAME = ''
USER_NAME = ''

CHAR_TYPES = [digits, lowercase, special, uppercase]
DICTIONARY = 'util/dictionary.txt'
PHPBB = 'util/phpbb.txt'
ROCKYOU = 'util/rockyou.txt'
DICTS = [DICTIONARY, PHPBB, ROCKYOU]


def read_file(filename):
    try:
        with open(filename) as file:
            for line in file:
                yield line.rstrip()
    except UnicodeDecodeError:
        # LOL, like my hack around this one??
        yield 'error'


def not_in_dict(password):
    for passwd_file in DICTS:
        dict_words = read_file(passwd_file)
        for word in dict_words:
            if 'dictionary' in passwd_file and len(word) < 5:
                break
            if password in word:
                return False
    return True


def check_length(password):
    return False if len(password) < 10 else True


def check_characters(password):
    found = [0] * len(CHAR_TYPES)
    count = 0

    for i, char_type in enumerate(CHAR_TYPES):
        for char in password:
            if found[i] == 0:
                if char in char_type:
                    count += 1
                    found[i] = 1
                    break
    return True if count >= 3 else False


def not_using_username(password):
    global USER_NAME
    if not USER_NAME:
        USER_NAME = input('username: ')

    return False if USER_NAME.lower() in password.lower() else True


def not_using_name(password):
    global ACTUAL_NAME
    if not ACTUAL_NAME:
        ACTUAL_NAME = input('First and last name: ')

    firstname = ACTUAL_NAME.split()[0]
    lastname = ACTUAL_NAME.split()[-1]

    for name in [firstname, lastname]:
        if name.lower() in password.lower():
            return False
    return True


def validate(password):
    checks = [
        not_in_dict,
        check_length,
        check_characters,
        not_using_username,
        not_using_name,
    ]

    for check in checks:
        valid = check(password)
        if not valid:
            return False
    return True


if __name__ == '__main__':
    while True:
        PASSWD = getpass('password: ')
        if validate(PASSWD):
            print('Your password is good!')
            break
        else:
            print(f'Your password is invalid! {PASSWD}')
