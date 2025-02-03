import csv
import threading
from datetime import datetime
import os

class CSVLogger:
    def __init__(self, filename):
        self.filename = filename
        self._initialize_file()

    def _initialize_file(self):
        if not os.path.exists(self.filename):
            with open(self.filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Date', 'Time', 'Message', 'Context', 'Model'])

    def log(self, message, ctx="", model=""):
        thread = threading.Thread(target=self._write_log, args=(message, ctx, model,))
        thread.start()

    def _write_log(self, message, ctx="", model=""):
        current_date = datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.now().strftime('%H:%M:%S')
        
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([current_date, current_time, message, ctx, model])