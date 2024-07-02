import sqlite3
import datetime



# insert data in database
def attendance(self, name):
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    # Check if the name already has an entry for the current date
    cursor.execute("SELECT * FROM attendance WHERE name = ? AND date = ?", (name, current_date))
    existing_entry = cursor.fetchone()
    if existing_entry:
        print(f"{name} is already marked as present for {current_date}")
    else:
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        cursor.execute("INSERT INTO attendance (name, time, date) VALUES (?, ?, ?)", (name, current_time, current_date))
        conn.commit()
        print(f"{name} marked as present for {current_date} at {current_time}")
    # here write the gpio led code 
    conn.close()