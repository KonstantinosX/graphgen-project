# Python GraphGen

*A Python Wrapper for the GraphGen library*

For more information and a great tutorial on the Python wrapper for GraphGen, please see [Efficient Graph Analytics on top of Relational Data](http://konstantinosx.github.io/graphgen-project/).

## Quickstart

This quickstart will show you how to get started using the example code. First install the graphgenpy module as follows:

    $ python setup.py install

You can now load a test DBLP database to use for the examples. First, edit the file in `examples/load-graphgen-testdb.py` on lines 19 and 20 to insert your PostgreSQL specific username and password, then run it as follows:

    $ python examples/load-graphgen-testdb.py

You can now execute GraphGen with the DBLP example:

    $ python examples/python-dblp-example-graphgen.py

If you have any questions, please submit an issue on Github! 
