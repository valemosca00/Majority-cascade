"""
cascade.py

Simulazione del processo di Majority Cascade (Influence Diffusion).
Dato un grafo G e un seed set S, calcola l'insieme finale dei nodi attivati Inf[S].
"""


def simulate_cascade(G, S):
    """
    Simula il majority cascade su G a partire dal seed set S.

    Un nodo v si attiva quando almeno la metà dei suoi vicini è già attiva:
        |N(v) ∩ active| >= deg(v) / 2

    Implementazione efficiente: invece di
    ricontrollare tutti i nodi della rete ad ogni round, si aggiorna solo il
    contatore di "vicini attivi" dei nodi confinanti con l'ultimo nodo attivato.

    Parametri
    ---------
    G : networkx.Graph
        Il grafo (non orientato).
    S : iterable
        Il seed set iniziale (nodi attivati a priori).

    Ritorna
    -------
    set
        L'insieme Inf[S] di tutti i nodi attivati a fine cascata.
    """
    active = set(S)

    # Soglia di attivazione per ogni nodo (calcolata una sola volta)
    threshold = {v: G.degree(v) / 2 for v in G.nodes()}

    # Contatore: per ogni nodo non ancora attivo, quanti vicini attivi ha finora
    active_neighbor_count = {}

    # Nodi "appena attivati" di cui bisogna ancora propagare l'effetto ai vicini
    frontier = list(active)

    while frontier:
        new_frontier = []
        for u in frontier:
            for w in G.neighbors(u):
                if w in active:
                    continue
                active_neighbor_count[w] = active_neighbor_count.get(w, 0) + 1
                if active_neighbor_count[w] >= threshold[w]:
                    active.add(w)
                    new_frontier.append(w)
        frontier = new_frontier

    return active