#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    execute_query("delete from matches;", commit=True)
    

def deletePlayers():
    """Remove all the player records from the database."""
    execute_query("delete from players;",commit=True)


def countPlayers():
    """Returns the number of players currently registered."""
    return  execute_query("select count(*) as num from players", fetch=True)[0][0]



def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    sql_string = "insert into players (name) values(%s);"
    execute_query(sql_string, (name,),commit=True)


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    return execute_query("select * from player_standings;",fetch=True)

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    sql_string = "insert into matches(winner, loser) values(%s,%s);"
    execute_query(sql_string, (winner,loser,),commit=True)

 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
    
    Each player appears exactly once in the pairings.  Each player is paired 
    with another player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings. Each pair will make unique match preventing rematches
     between players. If tournament has odd number of players, one player will  skip 
     one match and will get a free win. Player can only earn one free win per tournament
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    result = []
    num_players = len(standings)

    # handle odd number of players by givin one player the free win
    # starting from the last player in the standings list, we will find
    # a player that does not have a free win and will give the player the 
    # free win and exclude him from the list which we use for pairing
    # we will give the player a free win by reporting a match with  themselves
    if num_players%2 != 0:
        for i in range(len(standings)-1,-1,-1):
            player_id = standings[i][0]
            if uniqueMatch([player_id,player_id]):
                reportMatch(player_id,player_id)
                standings.pop(i)
                break
            

    #match players and prevent rematches between players using uniqueMatch function
    while len(standings) > 0:
        first_player = standings.pop(0)
        second_player = ''

        #pick the second player from a list which will make a unique match
        for i in range(0,len(standings)):
            second_player = standings[i]
            pair = [first_player[0], second_player[0]]
            if uniqueMatch(pair):
                standings.pop(i)
                break
        if second_player != '':
            pair = (first_player[0], first_player[1],second_player[0],second_player[1],)
            result.append(pair)
    return result

def uniqueMatch(pair):
    """ Returns a true or false if players have been matched before

    Agrs:
      pair: Array of exactly 2 integers of ids of 2 players.

    Returns:
      A boolean true if 2 playes have not been matched before or false if 2 players played before
      in the tounament
    """
    sql_string = "select * from matches where winner = %s and loser = %s or  winner = %s and loser = %s;"
    result = execute_query(sql_string, (pair[0], pair[1], pair[1], pair[0],),fetch=True)
    return len(result) == 0


def execute_query(sql_string, variables =(), fetch=False, commit=False):
    """ Query the database with and return all results
    Args:
      sql_string: the sql string to commit
      params: tuple of params to replace in query
      fetch: flag that determines if the result will be returned, use for query
      commit: flag that is used for queries that needs to be commited set True to commit

    Returns:
      all results from tha database if fetch set to true, otherwice True
    """
    result=True 

    pg = connect()
    c = pg.cursor()
    c.execute(sql_string, variables)
    if fetch:
        result = c.fetchall()
    if commit:
        pg.commit()
    pg.close()
    return result
