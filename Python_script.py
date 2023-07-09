import requests
import psycopg2
from datetime import datetime

# Database connection details
db_host = 'your_db_host'
db_name = 'your_db_name'
db_user = 'your_db_user'
db_password = 'your_db_password'

# TimezoneDB API details
api_key = 'your_api_key'

# API endpoints
timezone_list_endpoint = f'http://api.timezonedb.com/v2.1/list-time-zone?key={api_key}'
timezone_details_endpoint = 'http://api.timezonedb.com/v2.1/get-time-zone'

# Establish database connection
conn = psycopg2.connect(
    host=db_host,
    database=db_name,
    user=db_user,
    password=db_password
)
cur = conn.cursor()

# Delete and recreate TZDB_TIMEZONES table
cur.execute('DROP TABLE IF EXISTS TZDB_TIMEZONES')
cur.execute('CREATE TABLE TZDB_TIMEZONES (zone_id VARCHAR(50) PRIMARY KEY, zone_name VARCHAR(100))')

# Create TZDB_ERROR_LOG table
cur.execute('DROP TABLE IF EXISTS TZDB_ERROR_LOG')
cur.execute('CREATE TABLE TZDB_ERROR_LOG (timestamp TIMESTAMP, error_message TEXT)')

# Create staging table TZDB_ZONE_DETAILS_STAGE
cur.execute('DROP TABLE IF EXISTS TZDB_ZONE_DETAILS_STAGE')
cur.execute('CREATE TABLE TZDB_ZONE_DETAILS_STAGE (zone_id VARCHAR(50) PRIMARY KEY, country_name VARCHAR(100), '
            'abbreviation VARCHAR(10), gmt_offset INT, dst_offset INT)')

# Query TimezoneDB API to populate TZDB_TIMEZONES table
try:
    response = requests.get(timezone_list_endpoint)
    response.raise_for_status()
    data = response.json()
    timezones = data['zones']

    for timezone in timezones:
        zone_id = timezone['zoneId']
        zone_name = timezone['zoneName']
        cur.execute('INSERT INTO TZDB_TIMEZONES (zone_id, zone_name) VALUES (%s, %s)', (zone_id, zone_name))
except requests.HTTPError as err:
    # Log the error into TZDB_ERROR_LOG table
    error_message = str(err)
    timestamp = datetime.now()
    cur.execute('INSERT INTO TZDB_ERROR_LOG (timestamp, error_message) VALUES (%s, %s)', (timestamp, error_message))

# Query TimezoneDB API to populate TZDB_ZONE_DETAILS_STAGE table
for timezone in timezones:
    zone_id = timezone['zoneId']
    params = {'key': api_key, 'zone': zone_id}
    try:
        response = requests.get(timezone_details_endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        if data['status'] == 'OK':
            zone_id = data['zoneName']
            country_name = data['countryName']
            abbreviation = data['abbreviation']
            gmt_offset = data['gmtOffset']
            dst_offset = data['dstOffset']
            cur.execute('INSERT INTO TZDB_ZONE_DETAILS_STAGE (zone_id, country_name, abbreviation, gmt_offset, dst_offset) '
                        'VALUES (%s, %s, %s, %s, %s) ON CONFLICT (zone_id) DO NOTHING',
                        (zone_id, country_name, abbreviation, gmt_offset, dst_offset))
    except requests.HTTPError as err:
        # Log the error into TZDB_ERROR_LOG table
        error_message = str(err)
        timestamp = datetime.now()
        cur.execute('INSERT INTO TZDB_ERROR_LOG (timestamp, error_message) VALUES (%s, %s)', (timestamp, error_message))

# Update TZDB_ZONE_DETAILS table from TZDB_ZONE_DETAILS_STAGE
cur.execute('INSERT INTO TZDB_ZONE_DETAILS SELECT * FROM TZDB_ZONE_DETAILS_STAGE')
cur.execute('DROP TABLE IF EXISTS TZDB_ZONE_DETAILS_STAGE')

# Commit changes and close connection
conn.commit()
cur.close()
conn.close()

print("Data population completed.")
