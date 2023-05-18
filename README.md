
# CSV Processor

This repository contains a CSV processing script that can remove duplicates from a CSV file and shrink the file by grouping rows based on a specific column.

## Instructions

1. First, run the `env.sh` script to set up the necessary environment variables:

   ```shell
   $ source env.sh

Make sure to set the following variables in env.sh:

LOG_DIRECTORY: The directory where the source CSV file exists.
INPUT_FILENAME: The name of the input CSV file.
    $ export INPUT_FILENAME=csv1.csv
OUTPUT_FILENAME: The name of the output CSV file.
    $ export OUTPUT_FILENAME=csv1.csv

2.  To run the script without any additional options, execute the following command:
    $ python runner.py
    This will process the CSV file and perform the necessary operations based on the configured environment variables.

3.  To remove duplicates from the CSV file, use the --remove-dups option along with the --src and --tgt flags to specify the source and target filenames:
$ python runner.py --remove-dups --src <source_filename> --tgt <target_filename>

Replace <source_filename> with the name of the source CSV file and <target_filename> with the desired name for the target CSV file.

4. After running the script, the processed CSV file will be saved in the specified target directory with the provided filename.
