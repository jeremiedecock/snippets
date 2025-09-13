# C.f. https://docs.pytest.org/en/stable/getting-started.html#request-a-unique-temporary-directory-for-functional-tests

from pathlib import Path

def test_needsfiles(tmp_path: Path):
    print(tmp_path)
    assert 0
