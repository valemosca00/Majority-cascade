"""
wtss.py

Algoritmo WTSS (Weighted Target Set Selection), adattato al problema con
budget: l'esecuzione si ferma non appena aggiungere un nuovo nodo al seed
set supererebbe il costo massimo consentito k (anche se in teoria potrebbero esserci ancora Casi 1).
"""

import math
import heapq
from collections import deque


def wtss(G, k_budget, c):
    """
    Implementa WTSS(G) troncato al budget k_budget.

    Ad ogni iterazione si seleziona un nodo v secondo tre casi, con priorità
    Caso 1 > Caso 2 > Caso 3:
      - Caso 1 (k(v) = 0): v è già garantito attivo, si propaga il beneficio
        ai suoi vicini senza aggiungerlo a S.
      - Caso 2 (δ(v) < k(v)): v non può attivarsi naturalmente, va aggiunto
        forzatamente a S (se il budget lo consente).
      - Caso 3 (altrimenti): si sceglie il nodo da rimuovere tramite
        l'euristica c(u)*k(u) / (δ(u)*(δ(u)+1)).

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
    degree0 = dict(G.degree())
    delta = dict(degree0)                                     # δ(v) grado residuo: numero di vicini ancora in U
    kk = {v: math.ceil(degree0[v] / 2) for v in G.nodes()}    # k(v) = t(v): soglia residua
    U = set(G.nodes())
    S = set()
    S_cost = 0

    case1_queue = deque()    #non importante l'ordine
    case2_queue = deque()
    heap = []                # coda di priorità per il Caso 3: (-score, nodo)
    current_score = {}       # score attuale, per validare le voci nello heap

    def case3_score(v):
        d = delta[v]
        if d <= 0:
            return float("inf")
        return (c[v] * kk[v]) / (d * (d + 1))

    def refresh(v):
        """Ricontrolla lo stato di v e lo inserisce nella struttura giusta."""
        if v not in U:
            return
        if kk[v] <= 0:
            case1_queue.append(v)
        elif delta[v] < kk[v]:
            case2_queue.append(v)
        else:
            s = case3_score(v)
            current_score[v] = s
            heapq.heappush(heap, (-s, v)) # heapq implementa un min heap: per avere il max, inserisco il negativo di quei numeri
                                               # il minimo dei valori negati corrisponde esattamente al massimo dei valori originali

    for v in list(U):
        refresh(v)

    while U:
        v = None

        # --- selezione del nodo, con priorità Caso 1 > Caso 2 > Caso 3 ---
        while case1_queue and v is None:
            cand = case1_queue.popleft()
            if cand in U and kk[cand] <= 0:
                v = cand
        if v is None:
            while case2_queue and v is None:
                cand = case2_queue.popleft()
                if cand in U and delta[cand] < kk[cand]:
                    v = cand
        if v is None:
            while heap and v is None:
                neg_s, cand = heapq.heappop(heap)
                if (cand in U and cand in current_score
                        and abs(current_score[cand] - (-neg_s)) < 1e-9):
                    v = cand
        if v is None:
            break  # sicurezza: non dovrebbe accadere se U non è vuoto

        # --- azione specifica del caso ---
        if kk[v] <= 0:
            # Caso 1: v attivato "gratis", si propaga ai vicini
            for u in G.neighbors(v):
                if u in U:
                    kk[u] = max(0, kk[u] - 1)
        elif delta[v] < kk[v]:
            # Caso 2: v va aggiunto a S, se il budget lo consente
            if S_cost + c[v] > k_budget:
                return S
            S.add(v)
            S_cost += c[v]
            for u in G.neighbors(v):
                if u in U:
                    kk[u] -= 1
        # Caso 3: nessuna azione specifica, v viene semplicemente rimosso

        # --- rimozione di v dal grafo (comune a tutti i casi) ---
        U.discard(v)
        for u in G.neighbors(v):
            if u in U:
                delta[u] -= 1

        # ricalcola lo stato dei vicini di v, che potrebbe essere cambiato
        for u in G.neighbors(v):
            if u in U:
                refresh(u)

    return S