# C.f. https://docs.pytest.org/en/stable/getting-started.html#group-multiple-tests-in-a-class

class TestClass:           # 👈 Must be named "Test*"
    def test_one(self):    # 👈 Must be named "test_*"
        x = "this"
        assert "h" in x

    def test_two(self):    # 👈 Must be named "test_*"
        x = "hello"
        assert "h" in x
