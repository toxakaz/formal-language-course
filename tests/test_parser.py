import pytest
from project.grammar.parser import parse


def check_parser(text, token: str) -> bool:
    parser = parse(text)

    parser.removeErrorListeners()
    getattr(parser, token)()
    return not parser.getNumberOfSyntaxErrors()


@pytest.mark.parametrize(
    "text, accept",
    [
        ("_123", True),
        ("123", False),
        ("graph", True),
        ("", False),
        ("GRAPH", True),
        ("__main__", True),
        ("_", True),
    ],
)
def test_var(text, accept):
    assert check_parser(text, "var") == accept


@pytest.mark.parametrize(
    "text, accept",
    [
        ("123", True),
        ("-123", True),
        ('"hello world"', True),
        ("true", True),
        ("{11, 22, 33}", True),
    ],
)
def test_var(text, accept):
    assert check_parser(text, "val") == accept


@pytest.mark.parametrize(
    "text, accept",
    [
        ("lambda _ : 42", True),
        ("lambda _ : gg", True),
        ("lambda _ : true", True),
        ("lambda vv : vv in ss", True),
        ("lambda vv, uu : u_g", True),
        ("lambda vv, label, uu : 11", True),
        ("lambda 11, 22, 33 : 11", False),
    ],
)
def test_lambda(text, accept):
    assert check_parser(text, "lambda_") == accept


@pytest.mark.parametrize(
    "text, accept",
    [
        ("print g2", False),
        ("prnt g2", False),
        ("print(11)", True),
        ("print", False),
        ('gg = load("wine")', True),
        ("gg = 42", True),
        ("new_g = set_starts({13, -7, 42}, gg)", True),
        ("g_labels = get_labels(new_g)", True),
        ('common_labels = g_labels & (load("pizza"))', True),
        ("print(common_labels)", True),
        ("result = filter((lambda vv : vv in start), gg)", True),
        ("gg = set_starts({10, 100}, set_finals(get_vertices(tmp), tmp))", True),
        ('ll = "ll" | "kk"', True),
        ('qq = ("kk" | ll)*', True),
        ('qq = "ll" . "kk"', True),
        ("start = get_start(gg)", True),
    ],
)
def test_stmt(text, accept):
    assert check_parser(text, "stmt") == accept
