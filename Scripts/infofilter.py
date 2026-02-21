import pandas as pd

def filter_data(file_path):
    # Load the dataset
    df = pd.read_csv(file_path)

    # Convert date columns to datetime objects, handling potential errors
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Date Delisted'] = pd.to_datetime(df['Date Delisted'], errors='coerce')

    # Drop rows where date conversion failed
    df.dropna(subset=['Date', 'Date Delisted'], inplace=True)

    # Calculate the absolute difference in days between the two dates
    df['DateDifference'] = (df['Date Delisted'] - df['Date']).dt.days.abs()

    # For each 'Keyword', find the row with the minimum date difference
    # We can do this by sorting by the difference and then dropping duplicates, keeping the first.
    df_sorted = df.sort_values('DateDifference', ascending=True)
    df_filtered = df_sorted.drop_duplicates('Keyword', keep='first')

    # Drop the helper column
    df_filtered = df_filtered.drop(columns=['DateDifference'])

    # Save the result to a new CSV file
    df_filtered.to_csv('output/filtered_interpolated_information.csv', index=False)

    print("Filtered data saved to filtered_interpolated_information.csv")
