class TestPositive:

    def test_true(self):
        assert True

    def test_one(self):
        assert 1 == 1

    def test_str(self):
        assert '1' == '1'


class TestNegative:
    def test_false(self):
        assert False

    def test_two(self):
        assert 1 == 2
