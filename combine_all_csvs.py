import glob
import pandas as pd

# Define a list of glob_param and output_file pairs
file_combinations = [
    {
        "glob_param": "**/Spot Orders_Filled Orders (Show Order-Splitting).csv",
        "output_file": "./combined/Spot Orders_Filled Orders (Show Order-Splitting)-combined.csv"
    },
    {
        "glob_param": "**/Spot Orders_Filled Orders.csv",
        "output_file": "./combined/Spot Orders_Filled Orders-combined.csv"
    },
    {
        "glob_param": "**/Account History_Funding Account.csv",
        "output_file": "./combined/Account History_Funding Account-combined.csv"
    },
    {
        "glob_param": "**/Account History_Trading Account.csv",
        "output_file": "./combined/Account History_Trading Account-combined.csv"
    },
    {
        "glob_param": "**/Deposit_Withdrawal History_Withdrawal Record.csv",
        "output_file": "./combined/Deposit_Withdrawal History_Withdrawal Record-combined.csv"
    },
    {
        "glob_param": "**/Deposit_Withdrawal History_Deposit History.csv",
        "output_file": "./combined/Deposit_Withdrawal History_Deposit History-combined.csv"
    }
    # Add more entries as needed
]

def combine_csv_files(glob_param, output_file):
    """
    Combines all CSV files matching the glob pattern into a single file.

    Parameters:
        glob_param (str): The glob pattern to search for files (e.g., './data/*.csv').
        output_file (str): The path for the output file.
    """
    # Find all files matching the glob pattern
    matching_files = glob.glob(glob_param)

    if not matching_files:
        print(f"No files found matching the pattern: {glob_param}")
        return

    # Load and combine all matching CSV files
    dataframes = []
    for file in matching_files:
        try:
            df = pd.read_csv(file)
            dataframes.append(df)
        except Exception as e:
            print(f"Error reading file {file}: {e}")

    if not dataframes:
        print("No valid CSV files to combine.")
        return

    combined_data = pd.concat(dataframes, ignore_index=True).drop_duplicates()

    # Save to the specified output file
    try:
        combined_data.to_csv(output_file, index=False)
        print(f"Combined file saved to {output_file}")
    except Exception as e:
        print(f"Error saving combined file: {e}")

if __name__ == "__main__":
    # Iterate over each glob_param and output_file pair and combine CSV files
    for combination in file_combinations:
        combine_csv_files(combination["glob_param"], combination["output_file"])
