import pytest

from msgapp.app import messageApplication

@pytest.fixture
def app():
    app = messageApplication()
    app.debug = True
    return app

