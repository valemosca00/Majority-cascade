import os
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import LogNorm
import numpy as np

# --- Caricamento del grafo (salta queste righe se G_lcc è già definito nel notebook) ---
G = nx.read_edgelist("data/CA-AstroPh.txt", comments="#", nodetype=int)
largest_cc = max(nx.connected_components(G), key=len)
G_lcc = G.subgraph(largest_cc).copy()

# --- Cartella di output ---
output_dir = "figures"
os.makedirs(output_dir, exist_ok=True)

# --- Gradi e soglie (percentili, si adattano automaticamente alla distribuzione) ---
degrees = dict(G_lcc.degree())
node_list = list(G_lcc.nodes())
node_degrees = np.array([degrees[n] for n in node_list])

p50 = np.percentile(node_degrees, 50)
p90 = np.percentile(node_degrees, 90)
print(f"Soglie: basso <= {p50:.0f} (mediana), medio <= {p90:.0f} (90-percentile), alto > {p90:.0f}")

low_mask = node_degrees <= p50
mid_mask = (node_degrees > p50) & (node_degrees <= p90)
high_mask = node_degrees > p90

# --- Layout (calcolato una sola volta, riusato nei 3 pannelli) ---
pos = nx.spring_layout(G_lcc, seed=42, k=0.15, iterations=20)
xy = np.array([pos[n] for n in node_list])

# --- Plot: 3 pannelli affiancati ---
fig, axes = plt.subplots(1, 3, figsize=(24, 8))

panels = [
    ("Grado basso (<= mediana)", low_mask, "viridis"),
    ("Grado medio (mediana - 90° percentile)", mid_mask, "viridis"),
    ("Grado alto (> 90° percentile, hub)", high_mask, "viridis"),
]

for ax, (title, mask, cmap_name) in zip(axes, panels):
    # Sfondo: tutti i nodi in grigio chiaro, per dare contesto
    ax.scatter(xy[:, 0], xy[:, 1], s=3, c="lightgray", linewidths=0, zorder=1)
    nx.draw_networkx_edges(G_lcc, pos, alpha=0.03, width=0.3, ax=ax)

    # Nodi evidenziati per la fascia corrente
    sizes = 8 + 60 * (node_degrees[mask] / node_degrees.max())
    sc = ax.scatter(
        xy[mask, 0], xy[mask, 1],
        s=sizes,
        c=node_degrees[mask],
        cmap=cmap_name,
        norm=LogNorm(vmin=max(1, node_degrees[mask].min()), vmax=node_degrees.max()),
        linewidths=0.2,
        edgecolors="black",
        zorder=2,
    )
    ax.set_title(f"{title}\n(n={mask.sum()} nodi)", fontsize=11)
    ax.axis("off")
    plt.colorbar(sc, ax=ax, label="Node degree", shrink=0.7)

plt.suptitle("Graph Astro Physics Collaboration Network (ca-AstroPh) — per fascia di grado", fontsize=14)
plt.tight_layout()

output_path = os.path.join(output_dir, "ca_astroph_plot_thresholds.png")
plt.savefig(output_path, dpi=300)
plt.show()

print(f"Plot salvato in: {os.path.abspath(output_path)}")