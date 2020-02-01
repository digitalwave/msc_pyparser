import pytest
import msc_pyparser

@pytest.fixture
def mparser():
    return msc_pyparser.MSCParser()

@pytest.fixture
def read_config_file():
    def _read_config_file(name):
        conffile = "tests/" + name
        with open(conffile) as file:
            data = file.read()
        return data

    return _read_config_file

def test_parser(mparser, read_config_file):

    mparser.parser.parse(read_config_file("comment.conf"))

    assert len(mparser.configlines) > 0
    assert mparser.secconfdir is not None
