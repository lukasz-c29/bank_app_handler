from bank_app_handler import BankDataBaseHandler

import pytest 

from decimal import Decimal

def test_get_user():
    bdb_handler=BankDataBaseHandler(host="localhost", database="postgres", user="postgres", password="root")
    user = bdb_handler.get_user("ccc@gmail.com")
    assert user == [(3, 'ccc@gmail.com', Decimal('200.00'))]

def test_add_user():
    bdb_handler=BankDataBaseHandler(host="localhost", database="postgres", user="postgres", password="root")

    user_exist = bdb_handler.get_user("kkk@gmail.com")

    assert user_exist == []

    bdb_handler.add_user(user_email="kkk@gmail.com", amount= 2500)

    user_exist = bdb_handler.get_user("kkk@gmail.com")

    assert user_exist[0][1:] == ('kkk@gmail.com', Decimal('2500.00'))

    bdb_handler.delete_user(user_email="kkk@gmail.com")
