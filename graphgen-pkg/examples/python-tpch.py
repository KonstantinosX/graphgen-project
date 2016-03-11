from graphgenpy import GraphGenerator
import networkx as nx

# a graph of authors if they've bought the same part.
datalogQuery = """
Nodes(ID, Name) :- Customer(ID, Name).
Edges(ID1, ID2) :- Orders(orderId1, ID1),Lineitem(orderId1,part),Orders(orderId2, ID2),Lineitem(orderId2,part),part < 1000.
"""

# Credentials for connecting to the database
gg = GraphGenerator("tpch","localhost","5432","kostasx","password") #All these must be strings!!

# Evaluate graph extraction query and serialize the resulting graph to disk in a standard format. Return the file's name in the FS.
extracted_name = "extracted_graph_tpch"
fname = gg.generateGraph(datalogQuery,extracted_name,GraphGenerator.GML)

# Load graph into NetworkX
G = nx.read_gml(fname,'id') #by default, the graph format will me gml
print "Graph Loaded into NetworkX! Running PageRank..."

# Run any algorithm on the graph using NetowrkX
# print nx.pagerank(G)
print "Done!"
