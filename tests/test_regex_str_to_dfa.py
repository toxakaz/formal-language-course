from project import *
from test_graphs import *
import pytest
from pyformlang.regular_expression import MisformedRegexError


def test_regex_str_to_dfa_wrong():
    with pytest.raises(MisformedRegexError):
        regex_str_to_dfa("[*|.]")


def test_regex_str_to_dfa():
    for graph in all_test_graphs:
        dfa = regex_str_to_dfa(graph.reg)
        acception_test(dfa, graph)
