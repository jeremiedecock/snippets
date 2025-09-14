from pathlib import Path

from hello_monkeypatch_function import getssh


# Mocked return function to replace Path.home. Always return '/home/foo'.
def mock_path_home():
    return Path("/home/foo")


def test_getssh(monkeypatch):
    # Application of the monkeypatch to replace Path.home
    # with the behavior of mock_path_home defined above.
    monkeypatch.setattr(Path, "home", mock_path_home)

    # Calling getssh() will use mock_path_home in place of Path.home
    # for this test with the monkeypatch.
    x = getssh()
    assert x == Path("/home/foo/.ssh")
