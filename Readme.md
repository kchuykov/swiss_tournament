Swiss tournament  database and python library

This is a simple database for swiss tournaments and a python library 
that has commands to use the database and have simple tournaments

Quick Start:

Here is how to use the program.

1. You will need a machine with python 2.7 and psql  installed (linux preferred)
2.  $ git clone https://github.com/kchuykov/swiss_tournament.git
3.  $ cd swiss_tournament
4.  $ psql
5.  => \i tournament.sql
6.  => \q
7. Run tests with: 
    $ python tournament_test.py