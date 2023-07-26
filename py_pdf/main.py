import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import pandas as pd

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        elif event.event_type == 'created':
            if event.src_path.endswith('.csv'):
                csv_file_path = event.src_path
                pdf_output_path = os.path.join("OUTPUT", f"{os.path.splitext(os.path.basename(csv_file_path))[0]}.pdf")
                csv_data = read_csv_data(csv_file_path)
                create_pdf(pdf_output_path, csv_data)
                print(f"Generated PDF: {pdf_output_path}")
                move_to_dst(csv_file_path)
                print(f"Moved CSV to DST folder: {csv_file_path}")

def read_csv_data(file_path):
    df = pd.read_csv(file_path)
    header = df.columns.tolist()
    data = [header] + df.values.tolist()
    return data

def create_pdf(file_path, data):
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    elements = []

    table = Table(data)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#CCCCCC'),
        ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), '#E6E6E6'),
        ('GRID', (0, 0), (-1, -1), 1, '#000000'),
    ])
    table.setStyle(style)

    elements.append(table)
    doc.build(elements)

def move_to_dst(file_path):
    dst_folder = "DST"
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)
    dst_path = os.path.join(dst_folder, os.path.basename(file_path))
    os.rename(file_path, dst_path)

if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path="CSVDATA", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
