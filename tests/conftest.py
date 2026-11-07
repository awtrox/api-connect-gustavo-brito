import pytest
from app import app as flask_app

@pytest.fixture
def client(tmp_path, monkeypatch):
    (tmp_path / "data").mkdir()
    monkeypatch.chdir(tmp_path)
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c