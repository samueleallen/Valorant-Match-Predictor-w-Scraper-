import psycopg2
import config
import pandas as pd

DB_HOST = config.DB_HOST
DB_NAME = config.DB_NAME
DB_USER = config.DB_USER
DB_PASSWORD = config.DB_PASSWORD

CSV_FILE_PATH = "C:/Users/Sam/Documents/Comp Sci/Valorant-Match-Predictor-w-Scraper-/content/overall_game_stats.csv"

def get_or_create_player(cursor, player_name):
    """
    Purpose: Checks if a player exists.
        Case 1: If player exists, return player_ID.
        Case 2: If player DNE, create the player and return new player_ID
    
    Arguments:
        cursor: Cursor object
        player_name (string): Player name
    Output:
        Returns player_id
    """
    # Check if player exists
    cursor.execute("SELECT player_id FROM Players WHERE player_name = %s;", (player_name,))
    player_id = cursor.fetchone()

    # If player exists, return player_id
    if player_id:
        return player_id[0]
    
    # Else, insert player
    cursor.execute("INSERT INTO Players (player_name) VALUES (%s) RETURNING player_id;", (player_name,))
    return cursor.fetchone()[0]

def get_or_create_team(cursor, team_name):
    """
    Purpose: Checks if a team exists.
        Case 1: If team exists, return team_ID.
        Case 2: If team DNE, create the team and return new team_ID
    
    Arguments:
        cursor: Cursor object
        team_name (string): Team name
    Output:
        Returns team_id
    """
    # Check if team exists
    cursor.execute("SELECT team_id FROM Teams WHERE team_name = %s;", (team_name,))
    team_id = cursor.fetchone()

    # If team exists, return team_id
    if team_id:
        return team_id[0]
    
    # Else, insert team
    cursor.execute("INSERT INTO Teams (team_name) VALUES (%s) RETURNING team_id;", (team_name,))
    return cursor.fetchone()[0]
    
def load_rosters():
    """
    Purpose: Loads current team roster data.
    
    Arguments:
        None

    Outputs:
        None. Just updates an SQL database named Rosters
    """
    try:
        # Load csv
        df = pd.read_csv(CSV_FILE_PATH)

        # Only include player and team attributes
        df = df[["Player", "Team", "date"]]

        # Connect to database
        with psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD) as cn:
            with cn.cursor() as rs:
                for index, row in df.iterrows():
                    # Get player name and ID
                    player_name = row["Player"]
                    player_id = get_or_create_player(rs, player_name)

                    # Get agent name and ID
                    agent_name = row["Agent"]
                    agent_id = get_or_create_agent(rs, agent_name)

                    # Try to convert to expected use_pct value
                    try:
                        use_pct = int(str(row["Use"]).split(" ")[1].strip("%"))
                    except (IndexError, ValueError):
                        print(f"Error: Could not parse Use value in row {index}: {row['Use']}")
                        use_pct = None

                    # Try to convert to expected kast value
                    try:
                        kast = int(str(row["KAST"]).strip("%"))
                    except (IndexError, ValueError):
                        print(f"Error: Could not parse KAST value in row {index}: {row['KAST']}")
                        kast = None

                    # Create and execute query
                    q = """
                        INSERT INTO PlayerAgentStats (player_id, agent_id, rounds, r2, use_pct, acs, kd_ratio, adr, kast_pct, kpr, fkpr, fdpr, kills, deaths, assists, fk, fd)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (player_id, agent_id) DO NOTHING;
                        """
                    
                    rs.execute(q, (player_id, agent_id, 
                                   row["RND"], row["Rating2.0"], use_pct, row["ACS"],
                                   row["K:D"], row["ADR"], kast, row["KPR"], row["FKPR"], row["FDPR"], row["K"], row["D"], row["A"],
                                   row["FK"], row["FD"]
                                   ))
                    
                cn.commit()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    load_rosters()