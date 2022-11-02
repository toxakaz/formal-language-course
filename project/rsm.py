from pyformlang.cfg import Variable
from pyformlang.finite_automaton import EpsilonNFA
from typing import Dict

from project.ecfg import ECFG


class RSM:
    def __init__(self, start: Variable, boxes: Dict[Variable, EpsilonNFA]):
        self.start = start
        self.boxes = boxes

    @classmethod
    def from_ecfg(cls: "RSM", ecfg: ECFG) -> "RSM":
        return cls(
            ecfg.start,
            {head: body.to_epsilon_nfa() for head, body in ecfg.productions.items()},
        )

    def minimize(self: "RSM") -> "RSM":
        for var, nfa in self.boxes.items():
            self.boxes[var] = nfa.minimize()
        return self
