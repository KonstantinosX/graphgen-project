# graphgenpy.py
# A Python wrapper for the GraphGen system.
#
# Author:   Konstantinos Xirogiannopoulos <kostasx@cs.umd.edu>
# Created:  Tue Aug 18 18:37:11 2015

import sys
import os
import utils
import os

class GraphGenerator:
    '''
    GraphGenerator objects keep track of the
    database connection configuration details
    '''
    GRAPHML = 'graphml'
    GML = 'gml'

    def __init__(self, host, port,  dbname, username, password):
        self.dbname = dbname
        self.port = port
        self.host = host
        self.username = username
        self.password = password

    def displayConfig(self):
        print "DBName: %s, Port: %s, Host: %s, Username: %s, Pass:%s " % self.dbname, self.port, self.host, self.username, self.password

    def generateGraph(self,extractionQuery, filename, serialization_format='gml'):
        '''
        Generates a Graph based on the extraction query,
        and serializes the result to disk
        '''

        classpth = os.path.dirname(os.path.abspath(__file__)) + "/lib/GraphGen-0.0.5-SNAPSHOT-jar-with-dependencies.jar";

        # Directly call Java program for graph extraction using popen
        (stdout, stderr) = utils.java(['com.umdb.graphgen.PyGenerateGraph', extractionQuery, serialization_format, filename,
                                       self.host, self.port, self.dbname, self.username, self.password], classpath=classpth)

        if(stderr is None):
            print "Extraction was Successful! Graph was serialized in: " + os.path.dirname(os.path.realpath(__file__)) + '/' + filename + '.' + serialization_format

        return filename+"."+serialization_format
