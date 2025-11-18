import psycopg2
import config
import pandas as pd

DB_HOST = config.DB_HOST
DB_NAME = config.DB_NAME
DB_USER = config.DB_USER
DB_PASSWORD = config.DB_PASSWORD

CSV_FILE_PATH = "C:/Users/Sam/Documents/Comp Sci/Valorant-Match-Predictor-w-Scraper-/content/team_regions.csv"

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

def get_or_create_region(cursor, region_name):
    """
    Purpose: Checks if a region exists.
        Case 1: If region exists, return region_id.
        Case 2: If region DNE, create the region and return new region_ID
    
    Arguments:
        cursor: Cursor object
        region_name (string): Region name
    Output:
        Returns region_id
    """
    # Check if region exists
    cursor.execute("SELECT region_id FROM Regions WHERE region_name = %s;", (region_name,))
    region_id = cursor.fetchone()

    # If region exists, return region_id
    if region_id:
        return region_id[0]
    
    # Else, insert region
    cursor.execute("INSERT INTO Regions (region_name) VALUES (%s) RETURNING region_id;", (region_name,))
    return cursor.fetchone()[0]

def load_team_data():
    """
    Purpose: Loads valorant team data including team_name and region.
    
    Arguments:
        None

    Outputs:
        None. Just updates an SQL database.
    """
    try:
        # Load csv
        df = pd.read_csv(CSV_FILE_PATH)

        # Connect to database
        with psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD) as cn:
            with cn.cursor() as rs:
                # Process each row
                for index, row in df.iterrows():
                    # Skip any invalid rows
                    region_val = row.get("Region")
                    team_name = row.get("Team Name")

                    if region_val == "Region" or pd.isna(region_val) or pd.isna(team_name):
                        continue

                    region = str(region_val).split(" ")[0] # Only grab the region name, not the tournament name.
                    region_id = get_or_create_region(rs, region)

                    # Now insert into Teams table
                    q = """
                        INSERT INTO Teams (team_name, region_id) VALUES (%s, %s)
                        ON CONFLICT (team_name) DO UPDATE
                        SET region_id = EXCLUDED.region_id;
                        """
                    
                    rs.execute(q, (team_name, region_id))

                cn.commit()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    load_team_data()