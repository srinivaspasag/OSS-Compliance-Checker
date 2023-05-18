import os
from pathlib import Path

# Get the current working directory
directory = Path.cwd()

# Check if the LOG_DIRECTORY environment variable is set
log_directory = os.getenv("LOG_DIRECTORY")

# If LOG_DIRECTORY is set, use that as the file directory, otherwise use a default directory
if log_directory:
    file_directory = Path(log_directory)
else:
    file_directory = directory / "test_resources"

# Get the input filename from the environment variable or set a default value
input_filename = os.getenv("INPUT_FILENAME", "CSVpy.csv")

# Set the output filenames
output_filename = os.getenv("OUTPUT_FILENAME", "output.csv")

# Build the full file paths using the file directory and file names
input_file_path = file_directory / input_filename
output_file_path = file_directory / output_filename
