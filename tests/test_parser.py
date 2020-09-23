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


def test_parser_regession(mparser, read_config_file):
    """ make sure that we can parse the regression rules
    """
    modsec_rules = read_config_file("regression.conf")
    mparser.parser.parse(modsec_rules)
    parsed = mparser.configlines

    rules = [entry for entry in parsed if entry.get("type") == "SecRule"]

    assert len(rules) == 13, "we ecpect 13 rules"
    assert rules[10]["chained"], "rule 11 (position 10) should be chained"
