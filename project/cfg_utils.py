from pyformlang.cfg import CFG

__all__ = ["cfg_to_wcnf"]


def cfg_to_wcnf(cfg: CFG) -> CFG:
    cleared_cfg = (
        cfg.remove_useless_symbols()
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )
    cleared_productions = cleared_cfg._get_productions_with_only_single_terminals()
    cleared_productions = cleared_cfg._decompose_productions(cleared_productions)
    return CFG(start_symbol=cleared_cfg.start_symbol, productions=cleared_productions)
