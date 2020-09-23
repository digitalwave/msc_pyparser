import pytest
import msc_pyparser

@pytest.fixture
def mlexer():
    return msc_pyparser.MSCLexer()

@pytest.fixture
def read_config_file():
    def _read_config_file(name):
        conffile = "tests/" + name
        with open(conffile) as file:
            data = file.read()
        return data

    return _read_config_file

def test_comment(mlexer, read_config_file):
    mlexer.lexer.input(read_config_file("comment.conf"))

    tok = mlexer.lexer.token()

    # Read Comment first
    print(tok.type)
    assert tok.type == "T_COMMENT"
    assert tok.lineno == 1

def test_secrule(mlexer, read_config_file):
    mlexer.lexer.input(read_config_file("basic.conf"))

    # Read SecRule now
    tok = mlexer.lexer.token()

    assert tok.type == "T_CONFIG_DIRECTIVE_SECRULE"
    assert tok.lineno == 1

    # Read Complex SecRule now
    tok = mlexer.lexer.token()

    assert tok.type == "T_SECRULE_VARIABLE"
