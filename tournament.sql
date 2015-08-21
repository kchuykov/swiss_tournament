-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here
drop database IF EXISTS tournament;

create database tournament;
\c tournament
create table players (
            id  serial primary key,
            name varchar(40) not null check(name <>''));
create table matches (  
            match_id SERIAL PRIMARY KEY,
            winner int,
            loser int,
            CONSTRAINT winner  foreign key(winner) references players(id),
            CONSTRAINT loser  foreign key(loser) references players(id));
create view player_matches as select id,name, count(winner) as matches from players left join matches on players.id = matches.winner or players.id = matches.loser group by id;
create view player_wins as select id,name, count(winner) as wins from players left join matches on players.id = matches.winner group by id;
create view player_standings as select player_matches.id, player_matches.name, player_wins.wins, player_matches.matches from player_matches, player_wins where player_wins.id = player_matches.id order by wins desc;
