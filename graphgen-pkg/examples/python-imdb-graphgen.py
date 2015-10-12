# -*- coding: utf-8 -*-

from graphgenpy import GraphGenerator
from graphgenpy import utils
import os
import networkx as nx


# datalogQuery = "Nodes(Id,Name) :- Author(Id,Name).Edges(id1,id2) :- AuthorPublication(id1,P), AuthorPublication(id2,P)."
datalogQuery = "Nodes(id,name):- name(id,name),cast_info(_,id,movie_id,_,_,_,role),movie_id <=200,role='1'. Edges(id1,id2):- cast_info(_,id1,movie_id,_,_,_,role),cast_info(_,id2,movie_id,_,_,_,role), role='1',movie_id<= 200."

# filename = 'coauthorship'
filename = 'coactorship'


# Specify database connection details and instanciate GraphGen object
gg = GraphGenerator("localhost","5432","imdb","kostasx","pass")

# Evaluate graph extraction query and serialize the resulting graph to disk in a standard format
fname = gg.generateGraph(datalogQuery,filename,GraphGenerator.GRAPHML)


print "The file is located at : " + os.path.dirname(os.path.realpath(__file__)) + '/' + fname
# Import graph into NetworkX by reading the serialized graph

#for GML Format
G = nx.read_gml(fname);
print "Graph Loaded into NetworkX! Running PageRank..."
nx.pagerank(G)
print "Done!"
