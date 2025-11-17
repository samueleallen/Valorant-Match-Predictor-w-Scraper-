import psycopg2
import config
import pandas as pd

DB_HOST = config.DB_HOST
DB_NAME = config.DB_NAME
DB_USER = config.DB_USER
DB_PASSWORD = config.DB_PASSWORD

CSV_FILE_PATH = "C:/Users/Sam/Documents/Comp Sci/Valorant-Match-Predictor-w-Scraper-/aggregated_game_stats.csv"

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

def clean_col(col_name):
    """
    Purpose: Helper function to adapt column names from the csv into our sql variable names
    
    Arguments:
        col_name (string): Name of a column
    Outputs:
        cleaned_name (string): Replaced column name that matches expected variable names in database.
    """
    # Replace all problematic attributes
    cleaned_name = col_name.replace(".", "_").replace("+/- K/D", "kd_diff").replace("HS%", "hs_pct").replace("+/- FK/FD", "fk_fd_diff")

    return cleaned_name

def load_normalized_data():
    """
    Purpose: """
    cn = None

    try:
        # Load CSV
        df = pd.read_csv(CSV_FILE_PATH)

        # Drop first column if it is an unnamed index
        if df.columns[0] == "Unnamed: 0":
            df = df.drop(columns=[df.columns[0]])
        
        # Connect to database
        with psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD) as cn:
            with cn.cursor() as rs:
                # Process each row
                for index, row in df.iterrows():
                    match_id = row["Match_ID"] 

                    # ----- Teams Table ----- #
                    team1_name = row["Team"]
                    team2_name = row["vs Team"]

                    team1_id = get_or_create_team(rs, team1_name)
                    team2_id = get_or_create_team(rs, team2_name)

                    # ----- Matches Table ----- #      
                    t1_won = bool(row["T1_Won"])

                    if t1_won:
                        winner_id = team1_id
                        loser_id = team2_id
                    else:
                        winner_id = team2_id
                        loser_id = team1_id
                    
                    match_q = f"""
                    INSERT INTO Matches (match_id, date_played, winner_team_id, loser_team_id, t1_won)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (match_id) DO NOTHING;
                    """

                    rs.execute(match_q, (match_id, row["date_str"], winner_id, loser_id, t1_won))

                    # ----- MatchStats Table ----- #

                    # Insert data for team 1
                    stats_t1_q = f"""
                    INSERT INTO MatchStats (match_id, team_id, is_team1, r2, acs, kills, deaths, assists, kd_diff, kast, adr, hs_pct, fk, fd, fk_fd_diff)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (match_id, team_id) DO NOTHING;
                    """
                    rs.execute(stats_t1_q, (match_id, team1_id, True, 
                                        row['R2.0_T1'], row['ACS_T1'], row['K_T1'], row['D_T1'], row['A_T1'], 
                                        row['+/- K/D_T1'], row['KAST_T1'], row['ADR_T1'], row['HS%_T1'],
                                        row['FK_T1'], row['FD_T1'], row['+/- FK/FD_T1']
                                    ))
                                                        
                    # Insert data for team 2
                    stats_t2_q = f"""
                    INSERT INTO MatchStats (match_id, team_id, is_team1, r2, acs, kills, deaths, assists, kd_diff, kast, adr, hs_pct, fk, fd, fk_fd_diff)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (match_id, team_id) DO NOTHING;
                    """
                    rs.execute(stats_t2_q, (match_id, team1_id, False, 
                                        row['R2.0_T2'], row['ACS_T2'], row['K_T2'], row['D_T2'], row['A_T2'], 
                                        row['+/- K/D_T2'], row['KAST_T2'], row['ADR_T2'], row['HS%_T2'],
                                        row['FK_T2'], row['FD_T2'], row['+/- FK/FD_T2']
                                    ))
                    
                    # Save changes
                    cn.commit()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    load_normalized_data()