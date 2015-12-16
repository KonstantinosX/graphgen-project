package com.umdb.vertexCentric;

import java.sql.SQLException;
import java.util.List;

import com.tinkerpop.blueprints.Direction;
import com.umdb.genCSR.CondensedCSRGraph;
import com.umdb.genCSR.Graph;
import com.umdb.genCSR.Vertex;
import com.umdb.graphgen.GraphGenerator;

/**
 * An example of an implementation of a vertex centric degree counter. 
 * This runs efficiently and in parallel (depending on number of cores) on the output graph
 * Users can implement any compute function. 
 * */
public class JavaGraphGen {
	public static void main(String[] args) throws SQLException,
			InterruptedException {

		// Instanciate graphgen object
		GraphGenerator ggen = new GraphGenerator("localhost", "5432",
				"kostasx", "kostasx", "password");

		List<Graph> l = null;
		String query = "Nodes(ID, Name) :- Author(ID, Name). "
				+ "Edges(ID1, ID2) :- AuthorPublication(ID1, PubID), AuthorPublication(ID2, PubID).";
		try {
			//generateGraph returns a list of graphs.
			l = ggen.generateGraph(query);
		} catch (SQLException e) {
			e.printStackTrace();
		}

		CondensedCSRGraph g = (CondensedCSRGraph) l.get(0);

		// g.expand(true);
		
		// This is a condensed graph that can be used as-is to run any kind of
		// graph analytics on this grpah without the need to expand it
		// with a performance tradeoff
		System.out.println(g);

		// Initialize vertec-centric object
		VertexCentric p = new VertexCentric(g);

		// The property id for the result will be "Degree"
		Executor degree = new Executor("Degree") {

			@Override
			//implement compute function for executor
			public void compute(Vertex v, VertexCentric p) {
				v.setVal(0); // initialize

				//iterate over v's real neighbors
				for (Vertex w : v.getVertices(Direction.BOTH)) {
					v.setVal((int) v.getVal() + 1);
				}
				p.voteToHalt(v);
			}
		};

		System.out.println("Running Degree...");
		p.run(degree); //run degree counter

		System.out.println("Done");
	}
}
