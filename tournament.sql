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
            first_player  int,
            second_player int,
            winner int,
            CONSTRAINT first_player  foreign key(first_player) references players(id),
            CONSTRAINT second_player  foreign key(second_player) references players(id),
            CONSTRAINT winner  foreign key(winner) references players(id),
            PRIMARY KEY(first_player, second_player));
create view player_matches as select id,name, count(winner) as matches from players left join matches on players.id = matches.first_player or players.id = matches.second_player group by id;
create view player_wins as select id,name, count(winner) as wins from players left join matches on players.id = matches.winner group by id;
create view player_standings as select player_matches.id, player_matches.name, player_wins.wins, player_matches.matches from player_matches, player_wins where player_wins.id = player_matches.id order by wins desc;










--create view first_players as select row_number() over() as num, id, name from (select row_number() over(order by wins desc) as num, id, name from player_wins) as my_table where num %2=0;
--create view second_players as select row_number() over() as num, id, name from (select row_number() over(order by wins desc) as num, id, name from player_wins) as my_table where num %2=1;
--create view swiss_pairings as select second_players.id as id1, second_players.name as name1, first_players.id as id2, first_players.name as name2 from second_players, first_players where second_players.num = first_players.num;
