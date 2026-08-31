import os
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import LogNorm
import numpy as np

# --- Caricamento del grafo (necessario solo se esegui questo file da solo,
#     non dentro il notebook dove G_lcc è già definito da una cella precedente) ---
G = nx.read_edgelist("data/CA-AstroPh.txt", comments="#", nodetype=int)
largest_cc = max(nx.connected_components(G), key=len)
G_lcc = G.subgraph(largest_cc).copy()

# --- Cartella di output (creala se non esiste) ---
output_dir = "plots"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "ca_astroph_plot.png")

# --- Calcolo gradi ---
degrees = dict(G_lcc.degree())
node_degrees = np.array([degrees[n] for n in G_lcc.nodes()])

# --- Layout (riusa lo stesso se già calcolato in una cella precedente, per non ricalcolarlo) ---
pos = nx.spring_layout(G_lcc, seed=42, k=0.15, iterations=20)

# --- Dimensione nodi proporzionale al grado (con un minimo per non sparire) ---
node_sizes = 5 + 40 * (node_degrees / node_degrees.max())

plt.figure(figsize=(11, 11))
ax = plt.gca()

# Disegna prima gli archi (con networkx, che qui funziona senza problemi)
nx.draw_networkx_edges(G_lcc, pos, alpha=0.04, width=0.3, ax=ax)

# Disegna i nodi manualmente con matplotlib, per poter usare LogNorm
xy = np.array([pos[n] for n in G_lcc.nodes()])
scatter = ax.scatter(
    xy[:, 0], xy[:, 1],
    s=node_sizes,
    c=node_degrees,
    cmap=cm.viridis,
    norm=LogNorm(vmin=max(1, node_degrees.min()), vmax=node_degrees.max()),
    linewidths=0.2,
    edgecolors="black",
)

cbar = plt.colorbar(scatter, label="Node degree (scala log)", shrink=0.8)

plt.title("Graph Astro Physics Collaboration Network (ca-AstroPh)", fontsize=13)
plt.axis("off")
plt.tight_layout()
plt.savefig(output_path, dpi=300)
plt.show()

print(f"Plot salvato in: {os.path.abspath(output_path)}")