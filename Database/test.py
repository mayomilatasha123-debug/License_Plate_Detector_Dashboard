import sqlite3
import pandas as pd

conn = sqlite3.connect('detections.db')
df = pd.read_sql_query("SELECT * FROM detections", conn)
print(df)