import sqlite3
from urllib import request

import pytest
import os
from app import create_database
from tests.click_test import runner

def test_create_database():
    response = runner.invoke(create_database)
    assert response.exit_code == 0
    location = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(location, '../database')
    assert os.path.exists(path) == True