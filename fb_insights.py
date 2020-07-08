import facebook
from datetime import datetime
import mysql.connector

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd= #leaving out password for confidentiality reasons,
    database="insights")

# Create a cursor that we can use to interact easily with SQL
mycursor = db.cursor()

# Page id for HEB
page_id = "650548094975633"

# Access token that is needed to pull data from FB
access_token = "EAAj99Nm8gkYBAOcQ6oYJ2W6b5aG2ZBJlhChBH69R6FZAStI3wiuLZCnst3eURuzrtBzxrzpRmKXT4pYpxy8iy2K4mVQYkdUWaiBfYaqrHM0b3ELceVIXMLLbEZAkLAfO0Ks4qeoUG02Yhq52t1eQWIyoPwanRcKR2PR1395L7gZDZD"

# Connect to Facebook using the access token above
graph = facebook.GraphAPI(access_token=access_token,
                          version="3.1")

# Get all the post id's from Jan. 1 2020 - July 5 2020
posts_2020 = graph.get_all_connections(id=page_id,
                                       connection_name='posts',
                                       fields='created_time',
                                       since=datetime(2020, 1, 1, 0, 0, 0),
                                       until=datetime(2020, 7, 7, 0, 0, 0))

# For each posts in the above range, get the total unique impressions and total engaged users
for post in posts_2020:
    post_insights = graph.get_connections(id=post['id'],
                                          connection_name='insights',
                                          metric='post_impressions_unique, post_engaged_users',
                                          date_preset='yesterday',
                                          period='lifetime')

    # Store the impressions and engagements in a variable
    total_impressions_unique = post_insights['data'][0]['values'][0]['value']
    total_engagement_unique = post_insights['data'][1]['values'][0]['value']

    # Insert the post_id, impressions, and engagements into the 'Posts' table on our SQL database
    mycursor.execute("INSERT INTO Posts (post_id, impressions, engagement, date_posted) VALUES (%s, %s, %s, %s)",
                     (post['id'], total_impressions_unique, total_engagement_unique, post['created_time'][0:10]))
    db.commit()
