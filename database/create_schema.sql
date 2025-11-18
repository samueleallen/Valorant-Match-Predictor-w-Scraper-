DROP TABLE IF EXISTS MatchStats;
DROP TABLE IF EXISTS Matches;
DROP TABLE IF EXISTS Roster;
DROP TABLE IF EXISTS Teams;
DROP TABLE IF EXISTS PlayerAgentStats_90Days;
DROP TABLE IF EXISTS PlayerAgentStats;
DROP TABLE IF EXISTS Regions;
DROP TABLE IF EXISTS Players;
DROP TABLE IF EXISTS Agents;

CREATE TABLE Agents (
    agent_id SERIAL,
    agent_name VARCHAR(30) NOT NULL UNIQUE,
    PRIMARY KEY (agent_id)
);

CREATE TABLE Players (
    player_id SERIAL,
    player_name VARCHAR(30) NOT NULL UNIQUE,
    PRIMARY KEY (player_id)
);

CREATE TABLE Regions (
    region_id SERIAL,
    region_name VARCHAR(20) NOT NULL UNIQUE,
    PRIMARY KEY (region_id)
);

CREATE TABLE PlayerAgentStats (
    player_id INT,
    agent_id INT,
    rounds INT NOT NULL,
    r2 DECIMAL(3, 2),
    use_pct INT,
    acs DECIMAL(4, 1),
    kd_ratio DECIMAL(3, 2),
    adr DECIMAL(4, 1),
    kast_pct INT,
    kpr DECIMAL(3, 2),
    fkpr DECIMAL(3, 2),
    fdpr DECIMAL(3, 2),
    kills INT,
    deaths INT,
    assists INT,
    fk INT,
    fd INT,
    PRIMARY KEY (player_id, agent_id),
    FOREIGN KEY (player_id) REFERENCES Players(player_id),
    FOREIGN KEY (agent_id) REFERENCES Agents(agent_id)
);

CREATE TABLE PlayerAgentStats_90Days (
    player_id INT,
    agent_id INT,
    rounds INT NOT NULL,
    r2 DECIMAL(3, 2),
    use_pct INT,
    acs DECIMAL(4, 1),
    kd_ratio DECIMAL(3, 2),
    adr DECIMAL(4, 1),
    kast_pct INT,
    kpr DECIMAL(3, 2),
    fkpr DECIMAL(3, 2),
    fdpr DECIMAL(3, 2),
    kills INT,
    deaths INT,
    assists INT,
    fk INT,
    fd INT,
    PRIMARY KEY (player_id, agent_id),
    FOREIGN KEY (player_id) REFERENCES Players(player_id),
    FOREIGN KEY (agent_id) REFERENCES Agents(agent_id)
);

CREATE TABLE Teams (
    team_id SERIAL,
    team_name VARCHAR(100) NOT NULL UNIQUE,
    region_id INT NOT NULL,
    PRIMARY KEY (team_id),
    FOREIGN KEY (region_id) REFERENCES Regions(region_id)
);

CREATE TABLE Roster (
    player_id INT,
    team_id INT,
    PRIMARY KEY(player_id),
    FOREIGN KEY (player_id) REFERENCES Players(player_id),
    FOREIGN KEY (team_id) REFERENCES Teams(team_id)
)

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