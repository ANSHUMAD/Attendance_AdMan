import subprocess
import threading

def run_attendance():
    subprocess.run(["python", "attendance_taker_main.py"])

def run_web():
    subprocess.run(["python", "web.py"])

if __name__ == "__main__":
    attendance_thread = threading.Thread(target=run_attendance)
    web_thread = threading.Thread(target=run_web)

    attendance_thread.start()
    web_thread.start()

    attendance_thread.join()
    web_thread.join()
