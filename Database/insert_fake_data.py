import sqlite3

conn = sqlite3.connect('detections.db')
cursor = conn.cursor()

# Clear old fake data first so you don't get duplicates
cursor.execute("DELETE FROM detections")

fake_data = [
    ('SMK-433KC', 0.94, 0.89, 0.86, 'Vehicles/image 1.jpg', '2026-07-20 08:15:00'),
    ('APP-457JE', 0.91, 0.87, 0.83, 'Vehicles/image 2.jpg', '2026-07-20 09:42:00'),
    ('10J-35FG', 0.88, 0.78, 0.71, 'Vehicles/image 3.jpg', '2026-07-21 07:05:00'),
    ('AGL-226HU', 0.85, 0.72, 0.65, 'Vehicles/image 4.jpg', '2026-07-21 10:30:00'),
    ('ABC-710DE', 0.93, 0.90, 0.88, 'Vehicles/image 5.jpg', '2026-07-22 12:18:00'),
    ('KRD-516JO', 0.90, 0.81, 0.76, 'Vehicles/image 6.jpg', '2026-07-22 14:50:00'),
    ('SMK-95AH', 0.87, 0.80, 0.74, 'Vehicles/image 7.jpg', '2026-07-19 11:20:00'),
    ('MAP-851AA', 0.83, 0.69, 0.60, 'Vehicles/image 8.jpg', '2026-07-19 16:05:00'),
    ('unreadable', 0.79, 0.45, 0.22, 'Vehicles/image 9.jpg', '2026-07-18 13:40:00'),
    ('KTU-585KP', 0.81, 0.62, 0.55, 'Vehicles/image 10.jpg', '2026-07-23 20:15:00'),
]

cursor.executemany('''
INSERT INTO detections (plate_number, vehicle_confidence, plate_confidence, ocr_confidence, image_path, timestamp)
VALUES (?, ?, ?, ?, ?, ?)
''', fake_data)

conn.commit()
conn.close()
print("Fake data inserted successfully")