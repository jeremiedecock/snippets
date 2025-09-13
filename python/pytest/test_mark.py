import pytest
import time

# pytest -m "not slow"
# pytest -m slow

@pytest.mark.slow
def test_foo1():
    time.sleep(3)
    assert True

@pytest.mark.slow
def test_foo2():
    time.sleep(3)
    assert True

def test_foo3():
    assert True

def test_foo4():
    assert True
