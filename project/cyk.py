from pyformlang.cfg import CFG

__all__ = ["cyk"]


def cyk(word: str, cfg: CFG) -> bool:

    if not word:
        return cfg.generate_epsilon()

    word_len = len(word)
    cnf = cfg.to_normal_form()
    dp = [[set() for _ in range(word_len)] for _ in range(word_len)]

    prods_t = [p for p in cnf.productions if len(p.body) == 1]
    prods = [p for p in cnf.productions if len(p.body) == 2]

    for i in range(word_len):
        dp[i][i].update(p.head.value for p in prods_t if word[i] == p.body[0].value)

    for step in range(1, word_len):
        for i in range(word_len - step):
            j = i + step
            for k in range(i, j):
                dp[i][j].update(
                    p.head
                    for p in prods
                    if p.body[0] in dp[i][k] and p.body[1] in dp[k + 1][j]
                )

    return cfg.start_symbol in dp[0][word_len - 1]
