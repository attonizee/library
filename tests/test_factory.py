import os
import tempfile

import pytest

from library import create_app
from library.database import db

@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({'TESTING' : True, 'DATABASE' : db_path})

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

    os.close(db_fd)
    os.unlink(db_path)

def test_empty_db(client):
    '''Start with a blank database'''

    rv = client.get('/test')
    assert b'Your app is work' in rv.data
