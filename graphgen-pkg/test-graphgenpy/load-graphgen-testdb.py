"""
Loads an example database into PostgreSQL to show off GraphGen examples.
"""

##########################################################################
## Imports
##########################################################################

import sys
import pprint
import psycopg2

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

##########################################################################
## Module Fixtures
##########################################################################

USERNAME = "kostasx" #<< insert PostgreSQL username here
PASSWORD = "password"  #<< insert PostgreSQL password here

# Change the database name if you already have a database called this.
# I think it's safe to assume you don't though ...
DBNAME   = "testgraphgen"

##########################################################################
## Helper Functions
##########################################################################

def connect_and_create(username=USERNAME, password=PASSWORD, dbname=DBNAME):
    """
    Connects to the database and drops the current database and creates a new one.
    """

    if username is None or password is None:
        print "Please edit this file with the username and password to your database!"
        sys.exit(1)

    # Create new test database
    try:
        dsn  = "dbname='postgres' user='{}' host='localhost' password='{}'"
        conn = psycopg2.connect(dsn.format(username, password))
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    except:
        print "Can't connect to PostgreSQL using the following DSN:\n    {}".format(repr(dsn))
        sys.exit(1)

    cursor = conn.cursor()
    cursor.execute("DROP DATABASE IF EXISTS {}".format(dbname))
    cursor.execute("CREATE DATABASE {}".format(dbname))

    # Connect to the new database and return the connection
    try:
        dsn  = "dbname='{}' user='{}' host='localhost' password='{}'"
        conn = psycopg2.connect(dsn.format(dbname, username, password))
        return conn
    except:
        print "Can't connect to PostgreSQL using the following DSN:\n    {}".format(repr(dsn))
        sys.exit(1)


def create_tables(conn):
    """
    Using a passed in connection, creates the tables in the DB.
    """
    cursor = conn.cursor()
    stmts  = (
        "CREATE TABLE author (id integer NOT NULL PRIMARY KEY,name character varying(1024));",
        "CREATE TABLE conference (id integer NOT NULL PRIMARY KEY,name character varying(1024),year integer,location character varying(1024));",
        "CREATE TABLE publication (id integer NOT NULL PRIMARY KEY,title character varying(2048),cid integer NOT NULL REFERENCES conference(id));",
        "CREATE TABLE authorpublication (aid integer NOT NULL  REFERENCES author(id), pid integer NOT NULL REFERENCES publication(id), PRIMARY KEY(aid,pid));",
    )

    for stmt in stmts:
        try:
            cursor.execute(stmt)
        except Exception as e:
            print "Problem creating database table with the folowing SQL:"
            print stmt
            print e
            sys.exit(2)

def insert_data(conn):
    """
    Inserts data into the tables that were created using the create tables statement.
    """

    # Data Structures
    database = (
        ('authors', {
            'data': (
                (1,'Anindya Datta'),
                (2,'Heiko Schuldt'),
                (3,'Sandeepan Banerjee'),
                (4,'Christophe Bobineau'),
                (5,'Sangyong Hwang'),
                (6,'Tirthankar Lahiri'),
                (7,'Evangelos Eleftheriou'),
                (8,'Quan Z. Sheng'),
                (9,'Egemen Tanin'),
                (10,'Brandon Lloyd'),
            ),
            'sql': "INSERT INTO author (id, name) VALUES (%s, %s);",
        }),
        ('conferences', {
            'data': (
                (49,'VLDB',2014,'Hangzhou, China'),
                (87,'VLDB',2015,'Kailua Kona, HI USA'),
                (84,'SIGMOD',2014,'Snowbird, Utah'),
                (36,'SIGMOD',2015,'Melbourne, Australia'),
                (59,'CIDR',2015,'Asilomar, CA USA'),
            ),
            'sql': "INSERT INTO conference (id, name, year, location) VALUES (%s, %s, %s, %s);",
        }),
        ('publications', {
            'data': (
                (8,'Title 1.',49),
                (15,'Title 2.',87),
                (25,'Title 3.',84),
                (44,'Title 4.',36),
                (64,'Title 5.',59),
            ),
            'sql': "INSERT INTO publication (id, title, cid) VALUES (%s, %s, %s);",
        }),
        ('authorpubs', {
            'data': (
                (1,8),
                (1,64),
                (1,44),
                (2,8),
                (3,15),
                (4,15),
                (5,25),
                (5,44),
                (6,25),
                (7,25),
                (7,8),
                (8,44),
                (9,64),
                (10,64),
                (10,44),
                (10,8),
                (3,64),
            ),
            'sql': "INSERT INTO authorpublication (aid, pid) VALUES (%s, %s);",
        }),
    )

    cursor = conn.cursor()
    for table, meta in database:
        try:
            cursor.executemany(meta['sql'], meta['data'])
        except Exception as e:
            print "Problem inserting data into {}:".format(table)
            print e

    conn.commit()
    cursor.close()

if __name__ == '__main__':
    conn = connect_and_create()
    create_tables(conn)
    insert_data(conn)
    conn.close()

    print "Successfully created the test database called {}".format(repr(DBNAME))
