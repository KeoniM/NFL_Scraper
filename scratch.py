import pandas as pd
import os

def main():
    folder_path = "data"
    output_file = "2017-2023_NFL_scores.csv"

    scores_files = os.listdir(folder_path)    
    scores_files.sort()

    dfs = [pd.read_csv(os.path.join(folder_path, file)) for file in scores_files if file.endswith('.csv')]

    # dfs = [pd.read_csv(os.path.join(folder_path, file)) for file in os.listdir(folder_path) if file.endswith('.csv')]

    # Concatenate all DataFrames
    combined_df = pd.concat(dfs, ignore_index=True) 

    # Save to a new CSV file in the current directory
    combined_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    main()