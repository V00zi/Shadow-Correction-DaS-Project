import pandas as pd

def filter_data(file_path):
    # Load the dataset
    df = pd.read_csv(file_path)

    # Convert date columns to datetime objects, handling potential errors
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Date Delisted'] = pd.to_datetime(df['Date Delisted'], errors='coerce')

    # Drop rows where date conversion failed
    df.dropna(subset=['Date', 'Date Delisted'], inplace=True)

    # Calculate the difference in days. A positive value means 'Date' is after 'Date Delisted'.
    df['DateDifference'] = (df['Date'] - df['Date Delisted']).dt.days

    # Filter for dates that are on or after the 'Date Delisted'
    df_after_delist = df[df['DateDifference'] >= 0].copy()

    # For each 'Keyword', find the row with the minimum positive date difference
    # We sort by the difference and then drop duplicates, keeping the first (which is the smallest).
    df_sorted = df_after_delist.sort_values('DateDifference', ascending=True)
    df_filtered = df_sorted.drop_duplicates('Keyword', keep='first')

    # Drop the helper column
    df_filtered = df_filtered.drop(columns=['DateDifference'])

    # Save the result to a new CSV file
    df_filtered.to_csv('output/p3/filtered_interpolated_information.csv', index=False)

    print("Filtered data saved to output/p3/filtered_interpolated_information.csv")
