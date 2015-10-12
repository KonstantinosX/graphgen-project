package release_test;

import java.sql.SQLException;
import java.util.List;

import com.tinkerpop.blueprints.Direction;
import com.tinkerpop.blueprints.Graph;
import com.tinkerpop.blueprints.Vertex;
import com.umdb.genCSR.GenGraph;
import com.umdb.genCSR.GenVertex;
import com.umdb.graphgen.GraphGenerator;
import com.umdb.vertexCentric.Executor;
import com.umdb.vertexCentric.VertexCentric;

public class JavaGraphGen {
	public static void main(String[] args) throws SQLException, InterruptedException {

		// instanciate graphgen object
		GraphGenerator ggen = new GraphGenerator("localhost", "5432", "dblp",
				"kostasx", "password");

		List<Graph> l = null;
		String query = "Nodes(ID, Name) :- Author(ID, Name). "
				+ "Edges(ID1, ID2) :- AuthorPublication(ID1, PubID), AuthorPublication(ID2, PubID).";
		try {
			l = ggen.generateGraph(query);
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		GenGraph g = (GenGraph) l.get(0);
		System.out.println(g);

		// Initialize vertec-centric object
		VertexCentric p = new VertexCentric(g);

		// The property id for the result will be "PageRank"
		Executor degree = new Executor("Degree") {

			@Override
			public void compute(Vertex v, VertexCentric p) {
				GenVertex gv = ((GenVertex) v);
				gv.setVal(0); // initialize

				for (Vertex w : v.getVertices(Direction.BOTH)) {
					gv.setVal((int) gv.getVal() + 1);
				}
				p.voteToHalt(gv);
			}
		};
		
		p.run(degree);
		
		System.out.println("Done");
	}
}
