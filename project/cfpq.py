from networkx import MultiDiGraph
from pyformlang.cfg import CFG
from scipy.sparse import dok_matrix
from project import BoolDecomposedNFA, graph_to_nfa, RSM, ECFG, Variable

__all__ = ["cfpq_by_tensor", "tensor", "cfpq"]


def tensor(graph: MultiDiGraph, cfg: CFG) -> set[int, str, int]:

    graph_bm = BoolDecomposedNFA.from_nfa(graph_to_nfa(graph))
    graph_bm.matrices = graph_bm.take_matrices()
    graph.states_count = graph_bm.take_states_count()

    rsm_bm = BoolDecomposedNFA.from_rsm(RSM.from_ecfg((ECFG.from_cfg(cfg))))

    for var in cfg.get_nullable_symbols():
        if var not in graph_bm.matrices.keys():
            graph_bm.matrices[var] = dok_matrix(
                (graph.states_count, graph.states_count), dtype=bool
            )
        for i in range(graph.states_count):
            graph_bm.matrices[var][i, i] = True

    intersection = rsm_bm.intersect(graph_bm)
    tc = intersection.transitive_closure()

    prev_nnz = tc.nnz
    new_nnz = 0

    while prev_nnz != new_nnz:
        for i, j in zip(*tc.nonzero()):
            rsm_i = i // graph.states_count
            rsm_j = j // graph.states_count

            graph_i = i % graph.states_count
            graph_j = j % graph.states_count

            var, _ = rsm_bm.take_dict()[rsm_i].value

            if (
                rsm_bm.take_start_vector()[0, rsm_i]
                and rsm_bm.take_final_vector()[0, rsm_j]
            ):
                if var not in graph_bm.matrices.keys():
                    graph_bm.matrices[var] = dok_matrix(
                        (graph.states_count, graph.states_count), dtype=bool
                    )
                graph_bm.matrices[var][graph_i, graph_j] = True

        tc = rsm_bm.intersect(graph_bm).transitive_closure()

        prev_nnz, new_nnz = new_nnz, tc.nnz

    return {
        (u, label, v)
        for label, bm in graph_bm.matrices.items()
        for u, v in zip(*bm.nonzero())
    }


def cfpq_by_tensor(
    cfg: CFG,
    graph: MultiDiGraph,
    start_symbol: Variable = Variable("S"),
    start_nodes: set[any] = None,
    final_nodes: set[any] = None,
) -> set[tuple[any, any]]:
    return cfpq(cfg, graph, start_symbol, start_nodes, final_nodes, tensor)


def cfpq(
    cfg: CFG,
    graph: MultiDiGraph,
    start_symbol: Variable = Variable("S"),
    start_nodes: set[any] = None,
    final_nodes: set[any] = None,
    algorithm: callable = tensor,
) -> set[tuple[any, any]]:

    if start_nodes is None:
        start_nodes = set(graph.nodes)

    if final_nodes is None:
        final_nodes = set(graph.nodes)

    result = algorithm(graph, cfg)
    return {
        (u, v)
        for u, var, v in result
        if var == start_symbol and u in start_nodes and v in final_nodes
    }
