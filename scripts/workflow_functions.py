import pandas as pd
import os
import glob
from datetime import datetime
import logging

def process_csv_files(data_directory="data"):
    """
    Process all CSV files in the specified directory
    Returns: List of processed files
    """
    processed_files = []
    csv_files = glob.glob(os.path.join(data_directory, "*.csv"))
    
    for file_path in csv_files:
        try:
            df = pd.read_csv(file_path)
            df['processed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            base_name = os.path.basename(file_path)
            processed_name = f"processed_{base_name}"
            processed_path = os.path.join(data_directory, processed_name)
            df.to_csv(processed_path, index=False)
            processed_files.append(processed_path)
            logging.info(f"Successfully processed: {file_path}")
        except Exception as e:
            logging.error(f"Error processing {file_path}: {str(e)}")
            raise
    
    return processed_files

def generate_report(processed_files, report_directory="data"):
    """
    Generate a summary report of processed files
    """
    try:
        report_data = []
        
        for file_path in processed_files:
            df = pd.read_csv(file_path)
            report_data.append({
                'file_name': os.path.basename(file_path),
                'row_count': len(df),
                'column_count': len(df.columns),
                'processed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        report_df = pd.DataFrame(report_data)
        report_path = os.path.join(report_directory, f"processing_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        report_df.to_csv(report_path, index=False)
        
        logging.info(f"Report generated: {report_path}")
        return report_path
        
    except Exception as e:
        logging.error(f"Error generating report: {str(e)}")
        raise

def cleanup_old_files(directory="data", days_old=1):
    """
    Clean up files older than specified days
    """
    try:
        import time
        current_time = time.time()
        cutoff_time = current_time - (days_old * 24 * 60 * 60)
        deleted_files = []
        
        for file_path in glob.glob(os.path.join(directory, "*.csv")):
            file_modified_time = os.path.getmtime(file_path)
            
            if file_modified_time < cutoff_time:
                os.remove(file_path)
                deleted_files.append(file_path)
                logging.info(f"Deleted old file: {file_path}")
        
        logging.info(f"Cleanup completed. Deleted {len(deleted_files)} files.")
        return deleted_files
        
    except Exception as e:
        logging.error(f"Error during cleanup: {str(e)}")
        raise
