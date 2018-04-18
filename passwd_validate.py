from getpass import getpass
from string import ascii_letters as lowercase
from string import ascii_uppercase as uppercase
from string import digits
from string import punctuation as special


# special = '!.*;$#@'  # These were specifically mentioned

class User:
    def __init__(self, fullname, username):
        self.first_name = fullname.split()[0]
        self.last_name = fullname.split()[-1]
        self.username = username


class ValidatePassword(User):
    CHAR_TYPES = [digits, lowercase, special, uppercase]
    DICTIONARY = 'util/dictionary.txt'
    PHPBB = 'util/phpbb.txt'
    ROCKYOU = 'util/rockyou.txt'
    DICTS = [DICTIONARY, PHPBB, ROCKYOU]

    def __init__(self, fullname, username, password):
        User.__init__(self, fullname, username)
        self.password = password

    @staticmethod
    def _read_file(filename):
        try:
            with open(filename) as file:
                for line in file:
                    yield line.rstrip()
        except UnicodeDecodeError:
            # LOL, like my hack around this one??
            yield 'error'

    def _not_in_dict(self):
        for passwd_file in self.DICTS:
            dict_words = self._read_file(passwd_file)
            for word in dict_words:
                if 'dictionary' in passwd_file and len(word) < 5:
                    break
                if self.password in word:
                    return False
        return True

    def _check_length(self):
        return False if len(self.password) < 10 else True

    def _check_characters(self):
        found = [0] * len(self.CHAR_TYPES)
        count = 0

        for i, char_type in enumerate(self.CHAR_TYPES):
            for char in self.password:
                if found[i] == 0:
                    if char in char_type:
                        count += 1
                        found[i] = 1
                        break
        return True if count >= 3 else False

    def _not_using_username(self):
        if self.username.lower() in self.password.lower():
            return False
        else:
            return True

    def _not_using_name(self):
        for name in [self.first_name, self.last_name]:
            if name.lower() in self.password.lower():
                return False
        return True

    @property
    def validate(self):
        checks = [
            self._not_in_dict,
            self._check_length,
            self._check_characters,
            self._not_using_username,
            self._not_using_name,
        ]

        for check in checks:
            valid = check()
            if not valid:
                return False
        return True


if __name__ == '__main__':
    try:
        name = input('First and Last name: ')
        account = input('Username: ')

        while True:
            password = getpass('Password: ')
            passwd = ValidatePassword(name, account, password)

            if passwd.validate:
                print(f'{password} is good!')
                break
            else:
                print(f'{password} is invalid!')
    except KeyboardInterrupt:
        print('\n\nProgram aborted by user. Exiting...\n')
        exit()
