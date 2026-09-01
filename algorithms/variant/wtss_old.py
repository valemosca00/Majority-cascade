"""
wtss.py

Algoritmo WTSS (Weighted Target Set Selection), adattato al problema con
budget: l'esecuzione si ferma non appena aggiungere un nuovo nodo al seed
set supererebbe il costo massimo consentito k.

Versione semplificata: il Caso 3 viene gestito con una scansione lineare
diretta su U (più semplice da leggere rispetto a una coda di priorità con
heap), al costo di una minore efficienza se il Caso 3 viene invocato molte
volte su reti di grandi dimensioni.
"""

import math
from collections import deque


def _pick_case3(U, delta, kk, c):
    """Trova il nodo di U con il punteggio più alto per il Caso 3."""
    best_v, best_score = None, -1
    for v in U:
        d = delta[v]
        score = (c[v] * kk[v]) / (d * (d + 1)) if d > 0 else float("inf")
        if score > best_score:
            best_score, best_v = score, v
    return best_v


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
        l'euristica c(u)*k(u) / (δ(u)*(δ(u)+1)), trovato con una scansione
        lineare su U.

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
    delta = dict(degree0)                                    # δ(v)
    kk = {v: math.ceil(degree0[v] / 2) for v in G.nodes()}    # k(v) = t(v)
    U = set(G.nodes())
    S = set()
    S_cost = 0

    case1_queue = deque()
    case2_queue = deque()

    def refresh(v):
        """Se v soddisfa Caso 1 o Caso 2, lo accoda; altrimenti resta
        candidato per il Caso 3 (gestito tramite scansione diretta di U)."""
        if v not in U:
            return
        if kk[v] <= 0:
            case1_queue.append(v)
        elif delta[v] < kk[v]:
            case2_queue.append(v)

    for v in list(U):
        refresh(v)

    while U:
        v = None

        # --- Caso 1: priorità massima ---
        while case1_queue and v is None:
            cand = case1_queue.popleft()
            if cand in U and kk[cand] <= 0:
                v = cand

        # --- Caso 2 ---
        if v is None:
            while case2_queue and v is None:
                cand = case2_queue.popleft()
                if cand in U and delta[cand] < kk[cand]:
                    v = cand

        # --- Caso 3: scansione lineare su U ---
        if v is None:
            v = _pick_case3(U, delta, kk, c)
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