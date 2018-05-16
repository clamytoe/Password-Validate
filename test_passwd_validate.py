# _*_ coding: utf-8 _*_
"""
test_passwd_validate
"""
from pathlib import Path
from passwd_validate import Account, check_password, check_length, load_data
from utils import hashit, not_in_dict, check_length, read_file

TEST_FILE = ".test_file"
test_file = Path(TEST_FILE)
if test_file.is_file():
    user = load_data()
else:
    name = input("First and Last name: ")
    username = input("Username: ")
    user = Account(name, username)
    user.save()
