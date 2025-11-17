DROP TABLE IF EXISTS MatchStats;
DROP TABLE IF EXISTS Matches;
DROP TABLE IF EXISTS Teams;

CREATE TABLE Teams (
    team_id SERIAL,
    team_name VARCHAR(100) NOT NULL UNIQUE,
    PRIMARY KEY (team_id)
);

CREATE TABLE Matches (
    match_id VARCHAR(128),
    date_played DATE NOT NULL,
    winner_team_id INT,
    loser_team_id INT,
    t1_won BOOLEAN,
    PRIMARY KEY (match_id),
    FOREIGN KEY (winner_team_id) REFERENCES Teams (team_id),
    FOREIGN KEY (loser_team_id) REFERENCES Teams (team_id)
);

CREATE TABLE MatchStats (
    matchstats_id SERIAL,
    match_id VARCHAR(128) NOT NULL,
    team_id INT NOT NULL,
    is_team1 BOOLEAN NOT NULL,

    -- Stats columns
    r2 DECIMAL(5,4),
    acs DECIMAL(5,1),
    kills DECIMAL(5,2),
    deaths DECIMAL(5,2),
    assists DECIMAL(5,2),
    kd_diff DECIMAL(5,2),
    kast DECIMAL(5,2),
    adr DECIMAL(5,2),
    hs_pct DECIMAL(4,1),
    fk DECIMAL(5,2),
    fd DECIMAL(5,2),
    fk_fd_diff DECIMAL(5,2),

    -- Composite unique constraint to ensure just one stat per team per match
    UNIQUE (match_id, team_id),
    
    PRIMARY KEY (matchstats_id),
    FOREIGN KEY (match_id) REFERENCES Matches (match_id),
    FOREIGN KEY (team_id) REFERENCES Teams (team_id)
);