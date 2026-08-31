"""
cost_functions.py

Le due funzioni di costo c: V -> N usate negli esperimenti:
- cost_random: valore casuale scelto in un range fissato
- cost_degree: c(u) = ceil(d(u) / 2)
"""

import math
import random


def cost_random(G, low=1, high=21, seed=42):
    """
    Assegna a ciascun nodo un costo casuale intero in [low, high].

    Il seed è fissato di default per garantire che la stessa assegnazione
    di costi venga riusata in modo identico in tutti gli esperimenti che
    coinvolgono questa funzione di costo (necessario per confronti equi
    tra algoritmi e valori di k diversi).

    Parametri
    ---------
    G : networkx.Graph
    low, high : int
        Estremi (inclusi) del range da cui pescare il costo casuale.
    seed : int
        Seed del generatore casuale, per riproducibilità.

    Ritorna
    -------
    dict
        Dizionario {nodo: costo}.
    """
    rng = random.Random(seed)
    return {u: rng.randint(low, high) for u in G.nodes()}


def cost_degree(G):
    """
    Assegna a ciascun nodo un costo pari a ceil(d(u) / 2), dove d(u) è il
    grado del nodo. Funzione deterministica: a parità di grafo G, restituisce
    sempre lo stesso risultato, senza bisogno di un seed.

    Parametri
    ---------
    G : networkx.Graph

    Ritorna
    -------
    dict
        Dizionario {nodo: costo}.
    """
    return {u: math.ceil(G.degree(u) / 2) for u in G.nodes()}