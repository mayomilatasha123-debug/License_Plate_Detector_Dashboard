# License Plate Detector Dashboard

A live dashboard for viewing license plate detection results, built as part of the TechHER25 edge AI and computer vision capstone project. It's designed to eventually sit on top of a YOLOv8 + EasyOCR detection pipeline running on a Jetson Orin Nano, but right now it runs on sample data so we can test the dashboard logic before the real camera feed is connected.

## Current Status

This is running on **sample data**, not live detections. The sample entries were generated from photos shared within the team to simulate what real detections from the Jetson camera feed would look like. Once the Jetson pipeline is live, it will write real entries into the same database table, and the dashboard will pick them up automatically. No changes needed on the dashboard side.

## How It Works

### The database
A SQLite database stores every detection in a single table, with columns for:
- Plate number (the OCR reading)
- Confidence score for the vehicle detection
- Confidence score for the plate detection
- Confidence score for the plate reading
- The detection image
- Timestamp of the detection

A Python script builds this database and fills it with sample entries so the dashboard has something to display while we wait on the real Jetson feed.

### The dashboard
The dashboard doesn't store any data of its own. It just reads from the same SQLite database every few seconds and displays it:

- **Top metrics** (Total Detections, Today, Avg Confidence) are calculated directly from everything in the table
- **Dropdown selector** lets you pick any row and see its photo alongside the plate number and confidence scores
- **Charts** turn the timestamp and confidence columns into trends over time
- **Bottom table** shows all rows, with filters and a search bar to narrow results by confidence level or plate number

In short: the Python script builds and fills the database, and the dashboard is a live display sitting on top of it.

## Next Steps

- Connect the Jetson Orin Nano's real detection pipeline so it inserts live entries into the same table structure
- Consider migrating from SQLite to Supabase (PostgreSQL) for cross-system access to the dashboard
- Replace sample data with real detection history once the camera feed is stable

## Tech Stack

- **Detection:** YOLOv8, EasyOCR
- **Hardware:** Jetson Orin Nano
- **Database:** SQLite (with a possible move to Supabase/PostgreSQL)
- **Dashboard:** Streamlit

## Live Demo

Deployed on Streamlit Community Cloud: https://lpd-dashboard.streamlit.app/#lpd
