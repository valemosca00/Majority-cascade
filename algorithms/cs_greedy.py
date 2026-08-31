"""
greedy.py

Algoritmo Cost-Seeds-Greedy, con le tre funzioni surrogate f1, f2, f3.

Le funzioni f_i(S) = sum_{v in V} h_i(|N(v) ∩ S|, d(v)) sono scomposte in un
contributo puntuale h_i, che dipende solo dal conteggio di vicini attivi di
un nodo e dal suo grado. Questo permette di calcolare il guadagno marginale
Δ_u f_i(S_d) di un candidato u guardando solo i suoi vicini diretti, invece
di ricalcolare f_i su tutta la rete ad ogni iterazione.
"""

import math
from collections import defaultdict


def _h1(count, degree):
    threshold = math.ceil(degree / 2)
    return min(count, threshold)


def _h2(count, degree):
    threshold = math.ceil(degree / 2)
    return sum(max(threshold - i + 1, 0) for i in range(1, count + 1))


def _h3(count, degree):
    threshold = math.ceil(degree / 2)
    total = 0.0
    for i in range(1, count + 1):
        denom = degree - i + 1
        if denom > 0:
            total += max((threshold - i + 1) / denom, 0)
    return total


_H_FUNCTIONS = {"f1": _h1, "f2": _h2, "f3": _h3}


def cost_seeds_greedy(G, k, c, f_name):
    """
    Implementa Cost-Seeds-Greedy(G, k, c, f_i).

    Parametri
    ---------
    G : networkx.Graph
    k : int o float
        Budget massimo (c(S) <= k).
    c : dict {nodo: costo}
    f_name : str
        Una tra "f1", "f2", "f3".

    Ritorna
    -------
    set
        Il seed set S trovato (il più grande con costo <= k).
    """
    h = _H_FUNCTIONS[f_name]
    degree = dict(G.degree())

    # counts[z] = numero di vicini di z attualmente in S_d
    counts = defaultdict(int)

    S_d = set()
    cost_S_d = 0
    candidates = set(G.nodes())

    while candidates:
        best_u, best_ratio = None, -1
        for v in candidates:
            delta = 0.0
            for z in G.neighbors(v):
                old = h(counts[z], degree[z])
                new = h(counts[z] + 1, degree[z])
                delta += new - old
            ratio = delta / c[v]
            if ratio > best_ratio:
                best_ratio, best_u = ratio, v

        S_p = set(S_d)
        S_d.add(best_u)
        cost_S_d += c[best_u]
        candidates.discard(best_u)

        if cost_S_d > k:
            return S_p

        for z in G.neighbors(best_u):
            counts[z] += 1

    return S_d