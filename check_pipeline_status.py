"""
Pipeline Status Checker
"""

import os
import glob
from datetime import datetime, timedelta

def check_pipeline_status():
    """
    Check the status of the automation pipeline
    """
    print("=" * 50)
    print("AUTOMATION PIPELINE STATUS")
    print("=" * 50)
    
    log_file = "logs/pipeline.log"
    if os.path.exists(log_file):
        log_size = os.path.getsize(log_file)
        log_modified = datetime.fromtimestamp(os.path.getmtime(log_file))
        print(f"Log file: {log_file}")
        print(f"Log size: {log_size} bytes")
        print(f"Last modified: {log_modified}")
        
        print("\nLast 10 log entries:")
        print("-" * 30)
        with open(log_file, 'r') as f:
            lines = f.readlines()
            for line in lines[-10:]:
                print(line.strip())
    else:
        print("Log file not found!")
    
    print(f"\nData Directory Status:")
    print("-" * 30)
    csv_files = glob.glob("data/*.csv")
    print(f"Total CSV files: {len(csv_files)}")
    
    processed_files = [f for f in csv_files if 'processed_' in f]
    report_files = [f for f in csv_files if 'processing_report_' in f]
    
    print(f"Processed files: {len(processed_files)}")
    print(f"Report files: {len(report_files)}")
    
    if csv_files:
        print("\nRecent files:")
        csv_files.sort(key=os.path.getmtime, reverse=True)
        for file_path in csv_files[:5]:
            modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            print(f"  {os.path.basename(file_path)} - {modified_time}")

if __name__ == "__main__":
    check_pipeline_status()
