from networkx import MultiDiGraph
from pyformlang.cfg import CFG, Terminal
from scipy.sparse import dok_matrix
from project import BoolDecomposedNFA, graph_to_nfa, cfg_to_wcnf, RSM, ECFG, Variable
from typing import Set, Tuple, Union

__all__ = ["cfpq_by_tensor", "tensor", "cfpq"]


def hellings(graph: MultiDiGraph, cfg: CFG) -> Set[Tuple]:

    wcnf = cfg_to_wcnf(cfg)
    eps_prods = set()
    term_prods = {}
    var_prods = {}

    for p in wcnf.productions:
        ph = p.head
        pb = p.body
        if len(pb) == 0:
            eps_prods.add(ph)
        elif len(pb) == 1:
            if ph not in term_prods:
                term_prods[ph] = set()
            term_prods[ph].add(pb[0])
        elif len(pb) == 2:
            if ph not in var_prods:
                var_prods[ph] = set()
            var_prods[ph].add((pb[0], pb[1]))

    result = set()

    for u, v, data in graph.edges(data=True):
        label = data["label"]
        for p in term_prods:
            if Terminal(label) in term_prods[p]:
                result.add((u, p, v))

    for v in graph.nodes:
        for p in eps_prods:
            result.add((v, p, v))

    queue = result.copy()
    while len(queue) > 0:
        s, label, f = queue.pop()

        temp = set()

        for u, p, v in result:
            if v == s:
                for curr in var_prods:
                    if (p, label) in var_prods[curr] and (u, curr, f) not in result:
                        queue.add((u, curr, f))
                        temp.add((u, curr, f))
            if u == f:
                for curr in var_prods:
                    if (label, p) in var_prods[curr] and (s, curr, v) not in result:
                        queue.add((s, curr, v))
                        temp.add((s, curr, v))

        result = result.union(temp)

    return result


def cfpq_by_hellings(
    cfg: CFG,
    graph: MultiDiGraph,
    start_symbol: Variable = Variable("S"),
    start_nodes: Set = None,
    final_nodes: Set = None,
) -> Set[Tuple[any, any]]:
    return cfpq(cfg, graph, start_symbol, start_nodes, final_nodes, hellings)


def tensor(graph: MultiDiGraph, cfg: CFG) -> Set[Union[int, str, int]]:

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
    start_nodes: Set = None,
    final_nodes: Set = None,
) -> Set[Tuple]:
    return cfpq(cfg, graph, start_symbol, start_nodes, final_nodes, tensor)


def cfpq(
    cfg: CFG,
    graph: MultiDiGraph,
    start_symbol: Variable = Variable("S"),
    start_nodes: Set = None,
    final_nodes: Set = None,
    algorithm: callable = tensor,
) -> Set[Tuple]:

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
