# _*_ coding: utf-8 _*_
"""
test_passwd_validate
"""
import pytest
from pathlib import Path

from passwd_validate.account import Account, PASSWD_FILE
from passwd_validate.app import get_name, get_username, load_data
from passwd_validate.utils import hashit, not_in_dict, read_file

NAME = "John Doe"
USERNAME = "e7654321"
BAD_PASSWD = "Password1234"
GOOD_PASSWD = "C0d3J@ck3r!"


@pytest.fixture
def dummy_account():
    return Account(NAME, USERNAME)


def test_get_name(capfd, monkeypatch):
    values = ["John", NAME]
    values_gen = (i for i in values)
    monkeypatch.setitem(__builtins__, "input", lambda prompt: next(values_gen))
    name = get_name()
    output = capfd.readouterr()[0]
    assert "Your first and last name are required!" in output
    assert name == NAME


def test_get_username(monkeypatch):
    monkeypatch.setitem(__builtins__, "input", lambda prompt: USERNAME)
    username = get_username()
    assert username == USERNAME


def test_hashit():
    hashed = "20b0747eefcdc16fa4fb06bbf9284303645ecc3d2c43927878bd513f06853" \
             "191c104aebae6d7fca6291f1e296c6af99ebf8a137cbd7a0d34f2e27b31cb" \
             "4fecdb"
    hashed_passwd = hashit(BAD_PASSWD)
    assert hashed_passwd == hashed


def test_not_in_dict_false():
    result = not_in_dict(BAD_PASSWD)
    assert result is False


def test_not_in_dict_true():
    result = not_in_dict(GOOD_PASSWD)
    assert result is True


def test_failed_account_creation():
    with pytest.raises(TypeError):
        Account()


def test_account_creation(dummy_account):
    assert isinstance(dummy_account, Account)
    assert dummy_account.first_name == "John"
    assert dummy_account.last_name == "Doe"
    assert dummy_account.username == "e7654321"
    assert len(dummy_account.used_passwords) == 0


def test_validate(dummy_account):
    valid = dummy_account.validate(BAD_PASSWD)
    assert valid is False
    valid = dummy_account.validate(GOOD_PASSWD)
    assert valid is True


def test_read_file():
    file = read_file("dictionary.txt")
    assert type(file).__qualname__ == "generator"
    assert next(file) == "A"
    assert next(file) == "a"


def test_load_data():
    pw_file = Path(PASSWD_FILE)
    assert PASSWD_FILE == ".pval_db"
    if pw_file.exists():
        user = load_data()
        assert isinstance(user, Account)


def test_str_method(dummy_account):
    fullname = f"{dummy_account.first_name} {dummy_account.last_name}"
    assert "Account(" in str(dummy_account)
    assert fullname in str(dummy_account)
    assert dummy_account.username in str(dummy_account)

