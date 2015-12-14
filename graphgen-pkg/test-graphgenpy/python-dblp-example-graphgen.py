from graphgenpy import GraphGenerator
import networkx as nx

datalogQuery = """
Nodes(ID, Name) :- Author(ID, Name).
Edges(ID1, ID2) :- AuthorPublication(ID1, PubID), AuthorPublication(ID2, PubID).
"""

# Credentials for connecting to the database
gg = GraphGenerator("localhost","5432","testgraphgen","kostasx","password") #All these must be strings!!

# Evaluate graph extraction query and serialize the resulting graph to disk in a standard format. Return the file's name in the FS.
fname = gg.generateGraph(datalogQuery,"extracted_graph",GraphGenerator.GML)

# Load graph into NetworkX
# by default, the graph format will me gml. 'id' here is the node attribute networkx should use as a label (mandatory)
G = nx.read_gml(fname,'id')
print "Graph Loaded into NetworkX! Running PageRank..."

# Run any algorithm on the graph using NetowrkX
print nx.pagerank(G)
print "Done!"
