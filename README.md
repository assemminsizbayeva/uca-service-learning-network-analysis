# UCA Service-Learning Network Analysis  
**Graph Theory Visualization – Naryn & Batken Regions**

**[▶ Click here for the live interactive network](https://YOUR-USERNAME.github.io/uca-service-learning-network-analysis/output/interactive_network.html)**

![Preview](output/preview.png)

## Project Description
This project models the University of Central Asia (UCA) Service-Learning network as a directed graph using real data from Naryn and Batken regions.  
Volunteers → Schools & Community Partners = knowledge flow edges.

Features:
- Interactive web visualization (zoom, drag, hover shows centrality)
- Centrality analysis (Degree, Betweenness, Eigenvector, PageRank)
- Automatic highlighting of the most influential volunteers & partners
- Ready for expansion simulations

## How to Run Locally
```bash
git clone https://github.com/YOUR-USERNAME/uca-service-learning-network-analysis.git
cd uca-service-learning-network-analysis
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python src/generate_network.py
# Then open output/interactive_network.html
