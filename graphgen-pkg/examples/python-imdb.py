# -*- coding: utf-8 -*-

from graphgenpy import GraphGenerator
from graphgenpy import utils
import os
import networkx as nx


# Give me a graph of actors (role=1) that have played in the same movie, only for movie_ids 0-200
datalogQuery = """
Nodes(id,name):- name(id,name),cast_info(_,id,movie_id,_,_,_,role),movie_id <=200,role='1'.
Edges(id1,id2):- cast_info(_,id1,movie_id,_,_,_,role),cast_info(_,id2,movie_id,_,_,_,role), role='1',movie_id<= 200.
"""

filename = 'coactorship'


# Specify database connection details and instanciate GraphGen object
gg = GraphGenerator("localhost","5432","imdb","kostasx","pass")

# Evaluate graph extraction query and serialize the resulting graph to disk in a standard format
fname = gg.generateGraph(datalogQuery,filename,GraphGenerator.GML)


# Import graph into NetworkX by reading the serialized graph
#for GML Format
G = nx.read_gml(fname,'id');
print "Graph Loaded into NetworkX! Running PageRank..."
nx.pagerank(G)
print "Done!"
