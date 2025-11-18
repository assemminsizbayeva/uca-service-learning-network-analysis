import pandas as pd
import networkx as nx
from pyvis.network import Network
import os

# ========================================
# 1. Load real data from CSV
# ========================================
df = pd.read_csv("../data/network_data.csv")

# ========================================
# 2. Build the directed graph
# ========================================
G = nx.DiGraph()
for _, row in df.iterrows():
    G.add_edge(row['source'], row['target'], title=row['type'])

# ========================================
# 3. Node categorization & styling
# ========================================
def categorize_node(node):
    if node.startswith("Vol_"):      return "Volunteer"
    if node.startswith("School_"):   return "School"
    if node.startswith("Partner_"):  return "Community Partner"
    return "Other"

node_types = {node: categorize_node(node) for node in G.nodes()}

type_color = {
    "Volunteer":         "#1f77b4",  # blue
    "School":            "#ff7f0e",  # orange
    "Community Partner": "#2ca02c",  # green
}

type_size = {
    "Volunteer": 28,
    "School": 38,
    "Community Partner": 32,
}

for node in G.nodes():
    ntype = node_types[node]
    G.nodes[node]["group"] = ntype
    G.nodes[node]["color"] = type_color.get(ntype, "#808080")
    G.nodes[node]["size"]  = type_size.get(ntype, 20)
    G.nodes[node]["label"] = node.replace("Vol_", "").replace("School_", "").replace("Partner_", "").replace("_", " ")

# ========================================
# 4. Centrality measures
# ========================================
deg_cent  = nx.degree_centrality(G)
betw_cent = nx.betweenness_centrality(G)
eig_cent  = nx.eigenvector_centrality(G, max_iter=1000)
page_rank = nx.pagerank(G)

nx.set_node_attributes(G, deg_cent,  "degree_centrality")
nx.set_node_attributes(G, betw_cent, "betweenness")
nx.set_node_attributes(G, eig_cent,  "eigenvector")
nx.set_node_attributes(G, page_rank, "pagerank")

# Highlight top-5 most influential nodes (by PageRank)
top_nodes = sorted(page_rank.items(), key=lambda x: x[1], reverse=True)[:5]
top_node_names = [n[0] for n in top_nodes]

for node in G.nodes():
    if node in top_node_names:
        G.nodes[node]["color"] = {
            "background": G.nodes[node]["color"],
            "border": "#FFD700",
            "highlight": {"background": "#FFEA00", "border": "#FFD700"}
        }
        G.nodes[node]["borderWidth"] = 5

# ========================================
# 5. Interactive visualization
# ========================================
net = Network(directed=True, height="900px", width="100%", bgcolor="#ffffff")
net.from_nx(G)

net.set_options("""
var options = {
  "nodes": {"font": {"size": 20}},
  "edges": {
    "arrows": {"to": {"enabled": true, "scaleFactor": 0.6}},
    "color": "#999999",
    "smooth": false
  },
  "physics": {
    "enabled": true,
    "barnesHut": {
      "gravitationalConstant": -12000,
      "springLength": 200,
      "springStrength": 0.04
    }
  },
  "interaction": {"hover": true, "navigationButtons": true}
}
""")

# Legend
legend_html = """
<div style="position:absolute;top:10px;left:10px;background:white;padding:15px;border:1px solid #ccc;z-index:1000;font-family:Arial;border-radius:8px;">
  <b>Legend</b><br>
  <span style="color:#1f77b4">●</span> Volunteer<br>
  <span style="color:#ff7f0e">●</span> School<br>
  <span style="color:#2ca02c">●</span> Community Partner<br>
  Gold border = Top 5 most central nodes
</div>
"""
net.html = legend_html + net.html

# Save
os.makedirs("../output", exist_ok=True)
net.write_html("../output/interactive_network.html")
print("Success! Open output/interactive_network.html in your browser")
