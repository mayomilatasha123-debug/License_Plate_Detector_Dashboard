import sqlite3

conn = sqlite3.connect('detections.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS detections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plate_number TEXT,
    vehicle_confidence REAL,
    plate_confidence REAL,
    ocr_confidence REAL,
    image_path TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()
print("Database and table created successfully")