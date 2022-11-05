import pytest

from project import ECFG, RSM


@pytest.mark.parametrize(
    "ecfg_text",
    (
        "",
        " S -> $ ",
        """
            S -> (a S b S) f*
            B -> B | (B C)
            C -> (A* B*) | (A* B*)
        """,
    ),
)
def test_rsm_minimize(ecfg_text):
    ecfg = ECFG.from_text(ecfg_text)
    rsm = RSM.from_ecfg(ecfg)
    minimized_rsm = rsm.minimize()
    assert all(
        [
            rsm.boxes[p].is_equivalent_to(minimized_rsm.boxes[p])
            for p in minimized_rsm.boxes
        ]
    )
