import pytest

from pyformlang.cfg import Variable, CFG
from pyformlang.regular_expression import Regex

from project import reg_str_to_dfa, ECFG


def reg_is_equal(r1: Regex, r2: Regex):
    return reg_str_to_dfa(str(r1)).is_equivalent_to(reg_str_to_dfa(str(r2)))


@pytest.mark.parametrize(
    "text_ecfg, expected_productions",
    [
        ("", []),
        (
            " S -> a S b S | $ ",
            {Variable("S"): Regex("a S b S | $")},
        ),
        (
            " S -> (a | b)* c ",
            {Variable("S"): Regex("(a | b)* c")},
        ),
        (
            """
                S -> (a (S | $) b)*
                A -> a b c
            """,
            {
                Variable("S"): Regex("(a (S | $) b)*"),
                Variable("A"): Regex("a b c"),
            },
        ),
        (
            """
                S -> (a (S | $) b)* | A
                A -> (a b c)
            """,
            {
                Variable("S"): Regex("(a (S | $) b)* | A"),
                Variable("A"): Regex("a b c"),
            },
        ),
    ],
)
def test_read_from_text(text_ecfg, expected_productions):
    ecfg = ECFG.from_text(text_ecfg)
    assert len(ecfg.productions) == len(expected_productions) and all(
        reg_is_equal(body, expected_productions[head])
        for head, body in ecfg.productions.items()
    )


@pytest.mark.parametrize(
    "text_cfg",
    [
        """
            S -> B -> C
        """,
        """
            A -> b B -> a
        """,
        """
            S -> a S b S
            A -> B ->
        """,
    ],
)
def test_more_than_one_production_per_line(text_cfg):
    with pytest.raises(Exception):
        ECFG.from_text(text_cfg)


@pytest.mark.parametrize(
    "text_cfg",
    [
        """
            S -> A
            S -> B
        """,
        """
            A -> b
            B -> a
            A -> c
        """,
    ],
)
def test_more_than_one_production(text_cfg):
    with pytest.raises(Exception):
        ECFG.from_text(text_cfg)


@pytest.mark.parametrize(
    "in_cfg, exp_ecfg_productions",
    [
        (
            " S -> epsilon ",
            {Variable("S"): Regex("$")},
        ),
        (
            """
                S -> a S b S
                S -> epsilon
            """,
            {Variable("S"): Regex("(a S b S) | $")},
        ),
        (
            """
                S -> i f ( B ) t h e n { ST } e l s e { ST }
                B -> t | f
                ST -> p a s s | S
            """,
            {
                Variable("S"): Regex("i f ( B ) t h e n { ST } e l s e { ST }"),
                Variable("B"): Regex("t | f "),
                Variable("ST"): Regex("p a s s | S"),
            },
        ),
    ],
)
def test_ecfg_productions(in_cfg, exp_ecfg_productions):
    cfg = CFG.from_text(in_cfg)
    ecfg = ECFG.from_cfg(cfg)
    ecfg_productions = ecfg.productions
    assert len(ecfg_productions) == len(exp_ecfg_productions) and all(
        reg_is_equal(body, exp_ecfg_productions[head])
        for head, body in ecfg_productions.items()
    )
