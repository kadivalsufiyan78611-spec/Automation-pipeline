"""
Pipeline Control Script
"""

import os
import signal
import sys
import subprocess
import time

def start_pipeline():
    """
    Start the automation pipeline
    """
    print("Starting automation pipeline...")
    
    if is_pipeline_running():
        print("Pipeline is already running!")
        return
    
    process = subprocess.Popen([sys.executable, "automation_pipeline.py"])
    
    with open("pipeline.pid", "w") as f:
        f.write(str(process.pid))
    
    print(f"Pipeline started with PID: {process.pid}")
    print("Use 'python3 pipeline_control.py stop' to stop the pipeline")

def stop_pipeline():
    """
    Stop the automation pipeline
    """
    print("Stopping automation pipeline...")
    
    if not os.path.exists("pipeline.pid"):
        print("No pipeline PID file found. Pipeline may not be running.")
        return
    
    try:
        with open("pipeline.pid", "r") as f:
            pid = int(f.read().strip())
        
        os.kill(pid, signal.SIGTERM)
        time.sleep(2)
        
        try:
            os.kill(pid, 0)
            print("Pipeline is still running. Forcing termination...")
            os.kill(pid, signal.SIGKILL)
        except OSError:
            print("Pipeline stopped successfully.")
        
        os.remove("pipeline.pid")
        
    except Exception as e:
        print(f"Error stopping pipeline: {str(e)}")

def is_pipeline_running():
    """
    Check if pipeline is currently running
    """
    if not os.path.exists("pipeline.pid"):
        return False
    
    try:
        with open("pipeline.pid", "r") as f:
            pid = int(f.read().strip())
        
        os.kill(pid, 0)
        return True
        
    except (OSError, ValueError):
        if os.path.exists("pipeline.pid"):
            os.remove("pipeline.pid")
        return False

def show_status():
    """
    Show pipeline status
    """
    if is_pipeline_running():
        with open("pipeline.pid", "r") as f:
            pid = f.read().strip()
        print(f"Pipeline is running (PID: {pid})")
    else:
        print("Pipeline is not running")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 pipeline_control.py [start|stop|status]")
        return
    
    command = sys.argv[1].lower()
    
    if command == "start":
        start_pipeline()
    elif command == "stop":
        stop_pipeline()
    elif command == "status":
        show_status()
    else:
        print("Invalid command. Use: start, stop, or status")

if __name__ == "__main__":
    main()
