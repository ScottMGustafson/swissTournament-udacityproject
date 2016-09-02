#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import subprocess

def tableExists(db, tablename):
        c=db.cursor()
        c.execute("""select exists
                        (select * from information_schema.tables 
                         where table_name=%s);""", (tablename,))
        return bool(c.fetchone()[0])


def executeSql(fname):
    with open(fname, 'r') as f:
        sql_file = f.read()

    sql_cmd = [it+';' for it in sql_file.split(';')]

    db = psycopg2.connect("dbname=postgres")
    c=db.cursor()
    for cmd in sql_cmd[0:-2]:
        try:
            c.execute(cmd)
        except psycopg2.ProgrammingError:
            print(cmd)
            raise
    db.commit()
    db.close()

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""

    try:
        db= psycopg2.connect("dbname=tournament")
        assert(tableExists(db,'matches') and tableExists(db,'players'))
    except:
        executeSql("tournament.sql")
        db= psycopg2.connect("dbname=tournament")
        assert(tableExists(db,'matches') and tableExists(db,'players'))
    return db 
        


def deleteMatches():
    """Remove all the match records from the database."""
    
    db=connect()
    c=db.cursor()
    c.execute("""delete from matches;""")
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db=connect()
    c=db.cursor()
    c.execute("""delete from matches;""")
    c.execute("""delete from players;""")

    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db=connect()
    c=db.cursor()
    c.execute("""select count(*) from players;""")
    rows=c.fetchall()
    db.close()
    return int(rows[0][0])
    

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db=connect()
    c=db.cursor()
    c.execute("""insert into players (name) values (%s);""",(name,))
    db.commit()
    db.close()

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
    db=connect()
    c=db.cursor()
    c.execute("""
              select id, name, wins, gamesplayed from standings_view;
              """)
    rows= c.fetchall()
    db.close()
    return rows
    

    #group by players.id order by wins


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db=connect()
    c=db.cursor()
    c.execute("insert into matches (winner_id, loser_id) values (%s, %s);",(str(winner),str(loser)))
    db.commit()
    db.close()

def delete_matches():
    db=connect()
    c=db.cursor()
    c.execute("""delete from matches""")   
    db.commit()
    db.close()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings=playerStandings()
    standings=sorted(standings, key=lambda x: x[2])
    lst=[]
    while len(standings)>1:
        first=standings.pop(0)
        sec=standings.pop(0)
        lst.append((first[0],first[1],sec[0],sec[1]))
    delete_matches()
    return lst
        
                    

