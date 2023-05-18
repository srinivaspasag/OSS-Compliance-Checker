from flask import Flask, jsonify, render_template, request
import csv_reader
#import license
import argparse
import consts
from logger import setup_logger

app = Flask(__name__)
logger = setup_logger()

# Start server
if __name__ == "__main__":
    """
    Starts the Flask application server.

    Parameters:
        debug (bool): If True, runs the application in debug mode.

    Returns:
        None.
    """
    parser = argparse.ArgumentParser(description="CSV Processor")
    parser.add_argument('--remove-dups', action='store_true', help='Remove duplicates from the CSV')
    parser.add_argument('--group_by_family', action='store_true', help='Shrink the CSV file')
    parser.add_argument('--format-file', action='store_true', help='Format the CSV file')
    parser.add_argument('--src', type=str, help='Path to the source CSV file')
    parser.add_argument('--tgt', type=str, help='Path to the target CSV file')

    
    args = parser.parse_args()

    if not args.remove_dups and not args.group_by_family:
        #app.run(debug=True)
        csv_reader.read_csv()
    else:
        file_path = consts.file_directory
        src = None
        tgt = None
        
        if args.src is not None:
            src = str(file_path) + "/" + args.src
        
        if args.tgt is not None:
            tgt = str(file_path) + "/" + args.tgt
        
        if args.remove_dups:
            if src is not None and tgt is not None:
                csv_reader.remove_dups(src, tgt)
            else:
                print("Missing source or target file path.")
            
        if args.group_by_family:
            if src is not None and tgt is not None:
                csv_reader.group_by_family(src, tgt)
            else:
                print("Missing source or target file path.")
                
        if args.format_file:
            if src is not None and tgt is not None:
                csv_reader.format_file(src, tgt)
            else:
                print("Missing source or target file path.")