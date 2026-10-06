"""
Performance monitoring for automation pipeline
"""

import psutil
import time
import os
from datetime import datetime

def monitor_pipeline_performance():
    """
    Monitor pipeline performance metrics
    """
    print("Pipeline Performance Monitor")
    print("=" * 40)
    
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('.')
    
    print(f"System Performance:")
    print(f"  CPU Usage: {cpu_percent}%")
    print(f"  Memory Usage: {memory.percent}%")
    print(f"  Disk Usage: {disk.percent}%")
    
    log_file = "logs/pipeline.log"
    if os.path.exists(log_file):
        log_size = os.path.getsize(log_file)
        print(f"\nPipeline Metrics:")
        print(f"  Log file size: {log_size} bytes")
        
        with open(log_file, 'r') as f:
            lines = f.readlines()
            recent_lines = [line for line in lines if datetime.now().strftime('%Y-%m-%d') in line]
            print(f"  Today's log entries: {len(recent_lines)}")
    
    data_files = len([f for f in os.listdir('data') if f.endswith('.csv')])
    print(f"  CSV files in data directory: {data_files}")

if __name__ == "__main__":
    monitor_pipeline_performance()
