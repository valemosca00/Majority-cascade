"""
my_seeds_old.py

Algoritmo My-Seeds: euristica greedy basata sulla k-core decomposition.

Seleziona iterativamente il nodo con il miglior rapporto score(v)/c(v), dove
score(v) parte dalla coreness di v e viene decrementato in modo permanente
ogni volta che un vicino diretto di v viene aggiunto al seed set (per
attenuare la ridondanza dovuta a vicinati sovrapposti).

Implementazione con coda di priorità (heap) e validazione lazy: evita di
riscandire tutti i candidati ad ogni iterazione, mantenendo invece una coda
ordinata per punteggio, con verifica di validità al momento dell'estrazione
(lo stesso principio già usato in wtss.py per il Caso 3).
"""

import heapq
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
    current_score = dict(core)

    # Heap iniziale: (-score/costo, nodo) -- si usa il rapporto come chiave
    # di ordinamento fin dall'inizio, non solo lo score puro.
    heap = [(-current_score[v] / c[v], v) for v in G.nodes()]
    heapq.heapify(heap)

    S = set()
    S_cost = 0
    in_graph = set(G.nodes())  # candidati non ancora scelti né scartati

    while heap:
        neg_ratio, v = heapq.heappop(heap)
        if v not in in_graph:
            continue
        current_ratio = current_score[v] / c[v]
        if abs(current_ratio - (-neg_ratio)) > 1e-9:
            continue  # voce obsoleta: il punteggio di v è cambiato nel frattempo

        if S_cost + c[v] > k_budget:
            # non entra nel budget residuo: scartato definitivamente
            # (il budget residuo può solo diminuire, non tornerà mai a starci)
            in_graph.discard(v)
            # continue
            return S

        S.add(v)
        S_cost += c[v]
        in_graph.discard(v)

        # penalità permanente ai vicini diretti ancora candidati
        for w in G.neighbors(v):
            if w in in_graph:
                current_score[w] = max(0, current_score[w] - 1)
                heapq.heappush(heap, (-current_score[w] / c[w], w))

    return S