import os
import glob
import argparse
from collections import Counter
from prettytable import PrettyTable

def get_file_counts(glob_pattern):
    """
    Scans all subdirectories matching the given glob pattern and returns a dictionary of file names
    with their counts and unique glob strings.

    Parameters:
        glob_pattern (str): The glob pattern to search for files (e.g., './data/**/*.csv').

    Returns:
        dict: A dictionary with file names as keys and a tuple (count, unique glob string) as values.
    """
    file_counts = Counter()
    file_paths = {}

    for file_path in glob.glob(glob_pattern, recursive=True):
        file_name = os.path.basename(file_path)
        file_counts[file_name] += 1
        if file_name not in file_paths:
            file_paths[file_name] = [file_path]
        else:
            file_paths[file_name].append(file_path)

    result = {}
    for file, count in file_counts.items():
        # Create a unique glob string
        unique_glob = os.path.join(os.path.dirname(glob_pattern), f"**/{file}")
        result[file] = (count, unique_glob)

    return result

def main():
    parser = argparse.ArgumentParser(description="List file names and their counts in subdirectories.")
    parser.add_argument("glob_pattern", type=str, help="Glob pattern to search for files (e.g., './data/**/*.csv').")

    args = parser.parse_args()
    glob_pattern = args.glob_pattern

    file_data = get_file_counts(glob_pattern)

    table = PrettyTable()
    table.field_names = ["File Name", "Count", "Unique Glob String"]

    for file, (count, glob_string) in file_data.items():
        table.add_row([file, count, glob_string])

    print(table)

if __name__ == "__main__":
    main()
