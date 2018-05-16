# _*_ coding: utf-8 _*_
"""
test_passwd_validate
"""
import pytest
from pathlib import Path

from passwd_validate.account import Account, PASSWD_FILE
from passwd_validate.app import (
    check_password, get_name, get_username, load_data)
from passwd_validate.utils import hashit, not_in_dict, read_file

TEST_FILE = Path(".test_file")
NAME = "John Doe"
USERNAME = "e7654321"


@pytest.fixture
def dummy_account():
    return Account(NAME, USERNAME)


def test_failed_account_creation():
    with pytest.raises(TypeError):
        Account()


def test_account_creation(dummy_account):
    assert isinstance(dummy_account, Account)
    assert dummy_account.first_name == "John"
    assert dummy_account.last_name == "Doe"
    assert dummy_account.username == "e7654321"
    assert len(dummy_account.used_passwords) == 0
