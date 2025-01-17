from project import BoolDecomposedNFA, graph_to_nfa, reg_str_to_dfa
from test_graphs import all_test_graphs
from collections import namedtuple


def test_nfa_to_boolean_matrices():
    for graph in all_test_graphs:
        nfa_before = graph_to_nfa(graph.graph, graph.start_states, graph.final_states)
        bm = BoolDecomposedNFA(nfa_before)
        nfa_after = bm.to_nfa()

        if nfa_before.is_empty():
            assert (
                nfa_after.is_empty()
            ), f"{graph.name} failed, nfa after boolean matrix is different from before"
        else:
            assert nfa_before.is_equivalent_to(
                nfa_after
            ), f"{graph.name} failed, nfa after boolean matrix is different from before"


def test_cross_boolean_matrices():
    test_type = namedtuple(
        "test", "graph1 graph1_nfa graph2 graph2_nfa accepts rejects"
    )
    tests = []
    nfas = [reg_str_to_dfa(i.reg) for i in all_test_graphs]
    for x_ind in range(0, len(all_test_graphs)):
        for y_ind in range(x_ind + 1, len(all_test_graphs)):
            x = all_test_graphs[x_ind]
            y = all_test_graphs[y_ind]
            x_nfa = nfas[x_ind]
            y_nfa = nfas[y_ind]
            accept = []
            reject = x.rejects + y.rejects
            for i in x.accepts + y.accepts:
                if y_nfa.accepts(i) and x_nfa.accepts(i):
                    accept.append(i)
                else:
                    reject.append(i)
            if len(accept) > 0:
                tests.append(test_type(x, x_nfa, y, y_nfa, accept, reject))

    assert (
        len(tests) != 0
    ), "no one intersectable pair of graphs in test graphs, add more tests"

    for test in tests:
        m1 = BoolDecomposedNFA(test.graph1_nfa)
        m2 = BoolDecomposedNFA(test.graph2_nfa)
        m3 = m1 & m2
        nfa = m3.to_nfa()
        for i in test.accepts:
            assert nfa.accepts(
                i
            ), f"cross graph of {test.graph1.name}, {test.graph2.name}, {i} not accepted"
        for i in test.rejects:
            assert not nfa.accepts(
                i
            ), f"cross graph of {test.graph1.name}, {test.graph2.name}, {i} accepted"
