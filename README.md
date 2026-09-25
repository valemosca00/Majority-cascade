# Majority Cascade

Implementazione e analisi sperimentale del problema di *seed set selection* nel modello **Majority Dynamical Process** (Majority Cascade) su reti sociali, con vincolo di budget sui costi di attivazione.

Progetto per il corso di **Reti Sociali**, Dipartimento di Informatica, Università degli Studi di Salerno (A.A. 2025-2026).

## Il problema

Data una rete `G = (V, E)` e un seed set iniziale `S ⊆ V`, il processo di Majority Cascade attiva progressivamente i nodi la cui metà (o più) dei vicini è già attiva. Un nodo attivato resta attivo per sempre; il processo termina in un numero finito di passi a un insieme finale `Inf[S]`.

Nella variante con costi, ogni nodo `u` ha un costo `c(u)` per essere incluso nel seed set. Dato un budget `k`, l'obiettivo è trovare `S` con `c(S) ≤ k` che massimizzi `|Inf[S]|`. Il problema è NP-hard e difficile da approssimare anche nel caso di costi unitari, quindi la risoluzione pratica passa attraverso euristiche.

## Algoritmi implementati

- **Cost-Seeds-Greedy** (`algorithms/cs_greedy.py`, variante ottimizzata in `algorithms/variant/cs_greedy_new.py`) — costruisce il seed set aggiungendo iterativamente il nodo con miglior rapporto guadagno marginale / costo, secondo una delle tre funzioni surrogate `f1`, `f2`, `f3`.
- **WTSS** (Weighted Target Set Selection, `algorithms/wtss.py`) — elimina i nodi dal grafo uno alla volta, decidendo per ciascuno se sarà attivato gratuitamente, se va incluso forzatamente nel seed set, o se la decisione va rimandata; troncato al budget disponibile.
- **My-Seeds** (`algorithms/my_seeds.py`) — euristica proposta, basata sulla *k-core decomposition*: seleziona i nodi con il miglior rapporto coreness/costo, applicando una penalità incrementale ai vicini dei nodi già scelti per limitare la ridondanza tra vicinati sovrapposti.

Entrambi gli algoritmi più onerosi (WTSS e My-Seeds) usano code di priorità su heap con validazione lazy per evitare la riscansione completa dei candidati a ogni iterazione.

## Struttura del repository
```
algorithms/
├── cascade.py              # simulazione del Majority Cascade dato un seed set
├── cost_functions.py       # funzioni di costo c1 (random) e c2 (grado)
├── cs_greedy.py             # Cost-Seeds-Greedy (f1, f2, f3)
├── wtss.py                  # WTSS troncato al budget
├── my_seeds.py               # My-Seeds (euristica proposta)
├── graph_analysis/           # analisi strutturale e plot della rete
│   ├── analyze_network.py
│   ├── graph_plot.py
│   └── graph_plot_2.py
└── variant/                   # versioni alternative/precedenti degli algoritmi
    ├── cs_greedy_new.py
    ├── my_seeds_old.py
    └── wtss_old.py

data/
└── CA-AstroPh.txt            # dataset SNAP (rete di collaborazione ca-AstroPh)

results/                      # output CSV dei tre esperimenti
figures/                       # grafici generati (PNG)

experiments.ipynb              # notebook principale: esecuzione dei tre esperimenti e grafici
graph_analysis.ipynb           # analisi strutturale della rete (grado, clustering, diametro...)
tests.ipynb                    # test di verifica sui singoli algoritmi
requirements.txt
```

## Dataset

La rete utilizzata è **ca-AstroPh** (SNAP), una rete di collaborazione scientifica: i nodi sono autori di articoli di astrofisica su arXiv, gli archi indicano co-autorship. È scaricabile da [snap.stanford.edu/data/ca-AstroPh.html](https://snap.stanford.edu/data/ca-AstroPh.html); il file va estratto e posizionato in `data/CA-AstroPh.txt`.

Gli esperimenti lavorano sulla componente connessa più grande, dopo rimozione dei self-loop presenti nel dataset originale.

## Esperimenti

Il notebook `experiments.ipynb` esegue, per ciascuna delle due funzioni di costo (`c1`: casuale in [1, 21]; `c2`: `⌈d(u)/2⌉`):

1. **Esperimento 1** — variazione del budget `k` (0.5%, 1%, 2%, 5%, 10%, 20% del costo totale della rete), confrontando `|Inf[G, S]|` per i cinque algoritmi.
2. **Esperimento 2** — robustezza alla rimozione cumulativa di archi (1%, 5%, 10%, 20%), riutilizzando il seed set calcolato al budget rappresentativo `k* = 10%`.
3. **Esperimento 3** — robustezza alla rimozione cumulativa di vertici, con lo stesso schema dell'Esperimento 2.

I risultati vengono salvati incrementalmente in `results/` (i notebook, se rilanciati, non ricalcolano le configurazioni già presenti nei CSV), e i grafici prodotti sono salvati in `figures/`.

## Come eseguire

```bash
pip install -r requirements.txt
```

Scaricare il dataset come descritto sopra, quindi eseguire in ordine:

1. `graph_analysis.ipynb` (opzionale, per l'analisi strutturale della rete)
2. `tests.ipynb` (opzionale, verifica di correttezza degli algoritmi su grafi piccoli)
3. `experiments.ipynb` (esecuzione degli esperimenti e generazione dei grafici)

## Relazione

Una relazione completa, con motivazione delle scelte progettuali, analisi dei risultati e conclusioni, è disponibile in `progetto_reti_Mosca_Valerio.pdf`.
