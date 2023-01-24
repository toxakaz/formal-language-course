import pytest
from project.grammar.parser import generate_dot
from antlr4.error.Errors import ParseCancellationException


def test_write_dot():
    text = """
    gg = load("bzip");
    ff = set_finals(get_vertices(gg), set_starts({13, 42}, gg));
    qq = r"(l . r*)*";
    res = ff & qq;
    print(res);
    """
    path = generate_dot(text, "tests/data/test_grammar.dot")
    assert path == "tests/data/test_grammar.dot"


def test_incorrect_text():
    text = """
    g = load("bzip");
    g1 = set_finals(get_vertices(g), set_starts({13, 42}, g));
    q = r"(l . r*)*"
    res = g1 & q;
    print res
    """
    with pytest.raises(ParseCancellationException):
        generate_dot(text, "test")
