import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import pprint
import sys

username = None; #<< postgres username
password = None; #<< postgres password
dbname = "testgraphgen"; #<< change this name if you already have a valuable database with that name...I think it's safe you assume you don't

if username is None or password is None:
    print "Please edit this file with the username and password to your database!"
    sys.exit(1)
    
# create the new test database
try:
    conn = psycopg2.connect("dbname='postgres' user="+username+" host = 'localhost' password="+password)
except:
    print "I am unable to connect to Postgres."

conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()
cur.execute("DROP DATABASE "+dbname+";")
cur.execute("CREATE DATABASE "+dbname+";")

# connect to the newly created database
try:
    conn = psycopg2.connect("dbname='"+dbname+"' user="+username+" host='localhost' password="+password+"")
except:
    print "I am unable to connect to the database"

cur = conn.cursor()
try:
    authorTable = "CREATE TABLE author (id integer NOT NULL PRIMARY KEY,name character varying(1024));"
    cur.execute(authorTable)

    conference = "CREATE TABLE conference (id integer NOT NULL PRIMARY KEY,name character varying(1024),year integer,location character varying(1024));"
    cur.execute(conference)

    pub = "CREATE TABLE publication (id integer NOT NULL PRIMARY KEY,title character varying(2048),cid integer NOT NULL REFERENCES conference(id));"
    cur.execute(pub)

    authorpub = "CREATE TABLE authorpublication (aid integer NOT NULL  REFERENCES author(id), pid integer NOT NULL REFERENCES publication(id), PRIMARY KEY(aid,pid));"
    cur.execute(authorpub)

    # # execute our Query
    authors = """INSERT INTO author (id, name) VALUES
        (1,'Anindya Datta'),
        (2,'Heiko Schuldt'),
        (3,'Sandeepan Banerjee'),
        (4,'Christophe Bobineau'),
        (5,'Sangyong Hwang'),
        (6,'Tirthankar Lahiri'),
        (7,'Evangelos Eleftheriou'),
        (8,'Quan Z. Sheng'),
        (9,'Egemen Tanin'),
        (10,'Brandon Lloyd');"""
    cur.execute(authors)

    conferences = """ INSERT INTO conference (id, name,year,location) VALUES
        (49,'VLDB',2014,'Hangzhou, China'),
        (87,'VLDB',2015,'Kailua Kona, HI USA'),
        (84,'SIGMOD',2014,'Snowbird, Utah'),
        (36,'SIGMOD',2015,'Melbourne, Australia'),
        (59,'CIDR',2015,'Asilomar, CA USA');"""
    cur.execute(conferences)

    publications = """ INSERT INTO publication (id, title,cid) VALUES
        (8,'Title 1.',49),
        (15,'Title 2.',87),
        (25,'Title 3.',84),
        (44,'Title 4.',36),
        (64,'Title 5.',59);
        """
    cur.execute(publications)
    authorpubs = """INSERT INTO authorpublication (aid, pid) VALUES
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
        (3,64);"""
    cur.execute(authorpubs)

    conn.commit();
    cur.close()
    conn.close()
except:
    print "Unexpected error:", sys.exc_info()[0]
