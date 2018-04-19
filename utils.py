import hashlib

DICTIONARY = 'util/dictionary.txt'
PHPBB = 'util/phpbb.txt'
ROCKYOU = 'util/rockyou.txt'
DICTS = [DICTIONARY, PHPBB, ROCKYOU]


def hashit(password):
    h = hashlib.sha512()
    h.update(password.encode('utf-8'))
    return h.hexdigest()


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


def read_file(filename):
    try:
        with open(filename) as file:
            for line in file:
                yield line.rstrip()
    except UnicodeDecodeError:
        # LOL, like my hack around this one??
        yield 'error'
