swissTournament-udacityproject
================================
Final project for "intro to relational databases" on udacity in which
we simulate a swiss-style tournament.  See the [Wikipedia article](https://en.wikipedia.org/wiki/Swiss-system_tournament) for more detail.

Setting up the Database
-----------------------
Be sure to run the database setup script before running anything from swissTournament:

    > psql
    > \i tournament.sql

Database Structure
------------------
Table `players`:

 * `id`: automatically generated index for player
 * `name`: player name

Table `matches`:

 * `winner_id`: index of winner in `players` table
 * `loser_id`: index of loser in `players` table

tournament.py API
-----------------
This module contains all of the core functionality, interfacing with
the tournament database through psychopg2.

 * `connect()`: connects to the database.  This gets called anywhere we read or write to the database.

 * `deleteMatches()`: deletes from matches table

 * `deletePlayers()`: deletes from both players and matches table

 * `countPlayers()`: counts the number of registered players in the tournament returns: int
    

 * `registerPlayer(name)`: registers new player to tournament. Input: `name` (str)

 * `playerStandings()`: Returns a list of the players and their win records, sorted by wins. returns: list of tuples `(id, name, wins, matches)` where
     * `id`: assigned player id used in tournament db (int)
     * `name`: player name (str)
     * `wins`: number of wins (int)
     * `matches`: number of matches played (int)

 * `reportMatch(winner, loser)`: inserts output of match into matches table. Input: winner id (int), loser id (int)

 * `delete_matches()`: clears out matches table
 
 * `swissPairings()`: Returns a list of pairs of players for the next round of a match following swiss tournament rules. in the list, each element is a tuple of the format: 
    `(id1, name1, id2, name2)`,
where `id*` is and int and `name*` is a string. After pairings, all matches are deleted from the matches table
  
Testing:
--------
To test, run the supplied `tournament_test.py`
    > python tourament_test.py



 
