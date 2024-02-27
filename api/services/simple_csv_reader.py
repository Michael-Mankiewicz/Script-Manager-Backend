# simple_csv_reader.py
from django.conf import settings
import csv
import os

class SimpleCSVReader:
    def __init__(self, file_path):
        self.file_path = os.path.join(settings.MEDIA_ROOT, file_path)

    def read_and_print_lines(self, num_lines=5):
        lines = []
        with open(self.file_path, 'r', newline='', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if i >= num_lines:
                    break
                lines.append(f'Line {i+1}: {row}')
        return lines
