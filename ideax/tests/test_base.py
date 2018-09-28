from pytest import fixture


class TestBase(object):
    @fixture
    def setup(self):
        pass

    def test_add(self, ideax):
        assert 2 == ideax
