"""
Automation Pipeline Script
Combines scheduling, workflows, and logging for automated data processing
"""

import schedule
import time
import logging
import os
import sys
from datetime import datetime
from scripts.workflow_functions import process_csv_files, generate_report, cleanup_old_files

class AutomationPipeline:
    def __init__(self, log_file="logs/pipeline.log", max_retries=3):
        self.max_retries = max_retries
        self.setup_logging(log_file)
        
    def setup_logging(self, log_file):
        """
        Configure centralized logging with timestamps
        """
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("Automation Pipeline initialized")
    
    def execute_with_retry(self, func, *args, **kwargs):
        """
        Execute a function with retry logic
        """
        for attempt in range(1, self.max_retries + 1):
            try:
                self.logger.info(f"Executing {func.__name__} - Attempt {attempt}")
                result = func(*args, **kwargs)
                self.logger.info(f"Successfully executed {func.__name__}")
                return result
                
            except Exception as e:
                self.logger.error(f"Attempt {attempt} failed for {func.__name__}: {str(e)}")
                
                if attempt == self.max_retries:
                    self.logger.error(f"All {self.max_retries} attempts failed for {func.__name__}")
                    raise
                else:
                    self.logger.info(f"Retrying {func.__name__} in 30 seconds...")
                    time.sleep(30)
    
    def run_data_processing_workflow(self):
        """
        Main workflow execution with error handling
        """
        try:
            self.logger.info("=" * 50)
            self.logger.info("Starting Data Processing Workflow")
            self.logger.info("=" * 50)
            
            processed_files = self.execute_with_retry(process_csv_files, "data")
            
            if processed_files:
                report_path = self.execute_with_retry(generate_report, processed_files, "data")
                self.logger.info(f"Workflow completed successfully. Report: {report_path}")
            else:
                self.logger.info("No files to process in this run")
                
        except Exception as e:
            self.logger.error(f"Workflow failed after all retries: {str(e)}")
    
    def run_cleanup_task(self):
        """
        Execute cleanup task with error handling
        """
        try:
            self.logger.info("Starting cleanup task")
            deleted_files = self.execute_with_retry(cleanup_old_files, "data", 1)
            self.logger.info("Cleanup task completed successfully")
            
        except Exception as e:
            self.logger.error(f"Cleanup task failed: {str(e)}")
    
    def schedule_tasks(self):
        """
        Schedule all pipeline tasks
        """
        schedule.every(10).minutes.do(self.run_data_processing_workflow)
        schedule.every().day.at("02:00").do(self.run_cleanup_task)
        schedule.every().hour.do(self.run_cleanup_task)
        
        self.logger.info("Tasks scheduled successfully")
        self.logger.info("- Data processing workflow: Every 10 minutes")
        self.logger.info("- Cleanup task: Daily at 2:00 AM and every hour")
    
    def run_pipeline(self):
        """
        Main pipeline execution loop
        """
        self.logger.info("Automation Pipeline starting...")
        self.schedule_tasks()
        self.logger.info("Running initial workflow...")
        self.run_data_processing_workflow()
        self.logger.info("Starting scheduled execution loop...")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
                
        except KeyboardInterrupt:
            self.logger.info("Pipeline stopped by user")
        except Exception as e:
            self.logger.error(f"Pipeline error: {str(e)}")

def main():
    """
    Main function to start the automation pipeline
    """
    pipeline = AutomationPipeline()
    pipeline.run_pipeline()

if __name__ == "__main__":
    main()
