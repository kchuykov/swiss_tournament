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
    pg = connect()
    c = pg.cursor()
    sql_string = "delete from matches;" 
    c.execute(sql_string)
    pg.commit()
    pg.close() 
    

def deletePlayers():
    """Remove all the player records from the database."""
    pg = connect()
    c = pg.cursor()
    sql_string = "delete from players;"
    c.execute(sql_string)
    pg.commit()
    pg.close()

def countPlayers():
    """Returns the number of players currently registered."""
    pg = connect()
    c = pg.cursor()
    sql_string = "select count(*) as num from players"
    c.execute(sql_string)
    result = c.fetchone()[0]
    pg.close()
    return result


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    pg = connect()
    c = pg.cursor()
    sql_string = "insert into players (name) values(%s);"
    c.execute(sql_string, (name,))
    pg.commit()
    pg.close()

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
    pg = connect()
    c = pg.cursor()
    sql_string = "select * from player_standings;"
    c.execute(sql_string)
    result = c.fetchall()
    pg.close()
    return result

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    # if else block to make sure we don't get the same players paired more than once
    # since first + second is a primary key, we will always insert them smaller id, bigger id
    if winner > loser:
        first = loser
        second = winner
    else:
        first = winner
        second = loser

    
    pg = connect()
    c = pg.cursor()
    sql_string = "insert into matches values(%s,%s,%s);"
    c.execute(sql_string, (first,second,winner,))
    pg.commit()
    pg.close()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    * Functions will also prevents rematches between players
    * Function will also handle odd number of players by skipping one player from pairings
      the players that is not matched will earn a free win. The player will only earn one 
      free win per tournament
  
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
    # free win and exclude him from standings list which we use for pairing
    # we will give the player a free win by reporting a match with the themselves
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

    pair.sort()
    pg = connect()
    c = pg.cursor()
    sql_string = "select * from matches where first_player = %s and second_player = %s;"
    c.execute(sql_string, (pair[0], pair[1],))
    result = c.fetchall()
    return len(result) == 0



