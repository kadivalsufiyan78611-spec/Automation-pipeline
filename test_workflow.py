"""
Test script for workflow functions
"""

import sys
import os
import logging
from scripts.workflow_functions import process_csv_files, generate_report, cleanup_old_files

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_workflow_functions():
    """
    Test all workflow functions
    """
    print("Testing workflow functions...")
    
    try:
        print("\n1. Testing CSV processing...")
        processed_files = process_csv_files("data")
        print(f"Processed files: {processed_files}")
        
        if processed_files:
            print("\n2. Testing report generation...")
            report_path = generate_report(processed_files, "data")
            print(f"Report generated: {report_path}")
        
        print("\n3. Testing cleanup function...")
        deleted_files = cleanup_old_files("data", 2)
        print(f"Deleted files: {deleted_files}")
        
        print("\nAll tests completed successfully!")
        
    except Exception as e:
        print(f"Test failed: {str(e)}")

if __name__ == "__main__":
    test_workflow_functions()
