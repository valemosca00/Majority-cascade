"""
my_seeds_old.py

Algoritmo My-Seeds: euristica greedy basata sulla k-core decomposition.

Seleziona iterativamente il nodo con il miglior rapporto score(v)/c(v), dove
score(v) parte dalla coreness di v e viene decrementato in modo permanente
ogni volta che un vicino diretto di v viene aggiunto al seed set (per
attenuare la ridondanza dovuta a vicinati sovrapposti).
"""

import networkx as nx


def my_seeds(G, k_budget, c):
    """
    Implementa My-Seeds(G, k, c).

    Parametri
    ---------
    G : networkx.Graph
    k_budget : int o float
    c : dict {nodo: costo}

    Ritorna
    -------
    set
        Il seed set S trovato.
    """
    # k-core decomposition: calcolata una sola volta, costo O(V+E)
    core = nx.core_number(G)
    score = dict(core)

    S = set()
    S_cost = 0
    candidates = set(G.nodes())

    while candidates:
        best_u, best_ratio = None, -1
        for v in candidates:
            ratio = score[v] / c[v]
            if ratio > best_ratio:
                best_ratio, best_u = ratio, v

        if S_cost + c[best_u] > k_budget:
            candidates.discard(best_u)
            return S
            # continue  # questo nodo non ci sta nel budget residuo, si scarta e se ne cerca un altro

        S.add(best_u)
        S_cost += c[best_u]
        candidates.discard(best_u)

        # penalità permanente ai vicini diretti ancora candidati
        for w in G.neighbors(best_u):
            if w in candidates:
                score[w] = max(0, score[w] - 1)

    return S