# C.f. https://docs.pytest.org/en/stable/getting-started.html#request-a-unique-temporary-directory-for-functional-tests

from pathlib import Path

def test_needsfiles(tmp_path: Path):
    p = tmp_path / "hello.txt"
    p.write_text("Hello")
    assert p.read_text() == "Hello"
