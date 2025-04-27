import sqlite3
import threading
import csv
import time
from datetime import datetime, timedelta

class DatabaseManager:
    def __init__(self, db_name="transport.db"):
        # Initializes the database connection and threading lock
        self.db_name = db_name
        self.lock = threading.Lock()  # Lock for thread-safe access
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()  # Create tables if they dont exist

    def create_tables(self):
        # Create all required tables
        with self.lock:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS vehicles (
                    vehicle_id TEXT PRIMARY KEY,
                    vehicle_type TEXT,
                    route_id TEXT,
                    status TEXT,
                    last_seen TEXT
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS routes (
                    route_id TEXT PRIMARY KEY,
                    origin TEXT,
                    destination TEXT,
                    stop_sequence TEXT
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS location_updates (
                    update_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    vehicle_id TEXT,
                    latitude REAL,
                    longitude REAL,
                    speed REAL,
                    timestamp TEXT,
                    network_status TEXT
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS admin_commands (
                    command_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    vehicle_id TEXT,
                    command_type TEXT,
                    parameters TEXT,
                    sent_time TEXT,
                    response_time TEXT,
                    status TEXT
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS event_logs (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    vehicle_id TEXT,
                    event_type TEXT,
                    details TEXT,
                    event_time TEXT
                )
            ''')
            self.conn.commit()

    
    # Insert Methods for Logging

    def log_location_update(self, vehicle_id, latitude, longitude, speed, network_status):
        # Log real-time location updates (from UDP or TCP)
        with self.lock:
            self.cursor.execute('''
                INSERT INTO location_updates (vehicle_id, latitude, longitude, speed, timestamp, network_status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (vehicle_id, latitude, longitude, speed, datetime.now().isoformat(), network_status))
            self.conn.commit()

    def log_admin_command(self, vehicle_id, command_type, parameters, status="Pending"):
        # Log all admin commands sent
        with self.lock:
            self.cursor.execute('''
                INSERT INTO admin_commands (vehicle_id, command_type, parameters, sent_time, response_time, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (vehicle_id, command_type, parameters, datetime.now().isoformat(), None, status))
            self.conn.commit()

    def log_event(self, vehicle_id, event_type, details):
        # Log system-level events or errors
        with self.lock:
            self.cursor.execute('''
                INSERT INTO event_logs (vehicle_id, event_type, details, event_time)
                VALUES (?, ?, ?, ?)
            ''', (vehicle_id, event_type, details, datetime.now().isoformat()))
            self.conn.commit()

    def update_admin_response(self, command_id, response_status):
        # Update a command with response time and status (e.g., after client responds)
        with self.lock:
            self.cursor.execute('''
                UPDATE admin_commands
                SET response_time = ?, status = ?
                WHERE command_id = ?
            ''', (datetime.now().isoformat(), response_status, command_id))
            self.conn.commit()

   
    # data management
    # Purpose: To move location updates older than 15 minutes into csv file
    def archive_old_location_updates(self):
        
        cutoff_time = datetime.now() - timedelta(minutes=15)
        with self.lock:
            # Select old updates
            self.cursor.execute('''
                SELECT * FROM location_updates WHERE timestamp <= ?
            ''', (cutoff_time.isoformat(),))
            old_records = self.cursor.fetchall()

            # Save to CSV
            with open('archived_location_updates.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['update_id', 'vehicle_id', 'latitude', 'longitude', 'speed', 'timestamp', 'network_status'])
                writer.writerows(old_records)

            # (Optional) Delete archived records
            self.cursor.execute('''
                DELETE FROM location_updates WHERE timestamp <= ?
            ''', (cutoff_time.isoformat(),))
            self.conn.commit()

    
    # Predefined Queries for Analysis
   

    def vehicles_in_delayed_state(self):
        # Query vehicles that are currently delayed
        with self.lock:
            self.cursor.execute('''
                SELECT * FROM vehicles WHERE status = "Delayed"
            ''')
            return self.cursor.fetchall()

    def list_shutdown_commands(self):
        # Query list of all SHUTDOWN commands and their outcomes
        with self.lock:
            self.cursor.execute('''
                SELECT * FROM admin_commands WHERE command_type = "SHUTDOWN"
            ''')
            return self.cursor.fetchall()

    def average_response_time_by_vehicle(self):
        # Query average response time to admin commands, grouped by vehicle
        with self.lock:
            self.cursor.execute('''
                SELECT vehicle_id, AVG(julianday(response_time) - julianday(sent_time)) * 24 * 60 AS avg_minutes
                FROM admin_commands
                WHERE response_time IS NOT NULL
                GROUP BY vehicle_id
            ''')
            return self.cursor.fetchall()
