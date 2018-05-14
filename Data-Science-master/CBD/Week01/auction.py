from sqlalchemy import create_engine, Table, MetaData, Column, String
import psycopg2
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
import os

# .dotenv configuration
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

db_user = os.getenv('USER')
db_pass = os.getenv('PASS')

# Connect to DB
engine = psycopg2.connect(database="auction", user = db_user, password = db_pass, 
                        host = "dbinstance.cekgqzi9pswg.us-east-1.rds.amazonaws.com", port = "5432")

con = engine.cursor()

con.execute('DROP TABLE IF EXISTS user_bid; DROP TABLE IF EXISTS bid; DROP TABLE IF EXISTS item; DROP TABLE IF EXISTS users')

# Create table users(id, username, password)
con.execute("""CREATE TABLE IF NOT EXISTS users(ID SERIAL PRIMARY KEY, username TEXT NOT NULL, password TEXT NOT NULL)""")

# Create table item(id, name, description, start_time, user_id)
con.execute("""CREATE TABLE IF NOT EXISTS item(id SERIAL PRIMARY KEY, name TEXT NOT NULL, description TEXT NOT NULL, 
               start_time TIMESTAMP WITHOUT TIME ZONE, user_id INTEGER NOT NULL, FOREIGN KEY(user_id) REFERENCES users)""")

# Create table bid(id, price, item_id)
con.execute("""CREATE TABLE IF NOT EXISTS bid(id SERIAL PRIMARY KEY, price NUMERIC NOT NULL, item_id INT NOT NULL, FOREIGN KEY(item_id) REFERENCES item(id))""")

# Create table user_bid(user_id, bid_id)
con.execute("""CREATE TABLE IF NOT EXISTS user_bid (user_id INT, bid_id INT, PRIMARY KEY(user_id,bid_id), FOREIGN KEY(user_id) REFERENCES users(id), FOREIGN KEY(bid_id) REFERENCES bid(id))""")

# Insert 3 values to users
con.execute("""INSERT INTO users VALUES (1, 'quan', 'quan'), (2, 'hai', 'hai'), (3, 'son', 'son')""")

# Insert 1 value to item
con.execute("""INSERT INTO item VALUES (1, 'pen', 'good status', TIMESTAMP '2015-05-18 15:02:11', 1)""")

# Insert 2 values to bid
con.execute("""INSERT INTO bid VALUES (1, 2.36, 1)""")
con.execute("""INSERT INTO user_bid VALUES (2, 1)""")

con.execute("""INSERT INTO bid VALUES (2, 2.55, 1)""")
con.execute("""INSERT INTO user_bid VALUES (3, 2)""")

# Find the highest price and whose price
con.execute("""SELECT ub.user_id, b.price FROM bid b INNER JOIN user_bid ub ON b.id = ub.bid_id WHERE b.item_id=1 AND b.price = (SELECT MAX(bid.price) FROM bid)""")

df = pd.DataFrame(con.fetchall())

con.execute('SELECT username FROM users WHERE users.ID=' + str(df.iloc[0, 0]))

df = pd.DataFrame(con.fetchall())

# Print out the username who has highest price
print("User " + str(df.iloc[0, 0]) + " won")

con.close()