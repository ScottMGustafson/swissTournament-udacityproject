--drop tables and views if exists
drop view if exists standings_view;
drop table if exists matches, players;


--tables
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE matches (
    winner_id SERIAL NOT NULL, 
    loser_id SERIAL NOT NULL,
    FOREIGN KEY (winner_id) REFERENCES players(id),
    FOREIGN KEY (loser_id) REFERENCES players(id)
);

--views
create view standings_view as 
    select id, 
           name, 
           (select count(*) from matches 
                where winner_id=id
           ) as wins, 
           (select count(*) from matches 
                where loser_id=id or winner_id=id
           ) as gamesplayed
    from players
    group by id
    order by wins desc;




