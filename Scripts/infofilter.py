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
    df_filtered.to_csv('output/p3/filtered_interpolated_information.csv', index=False)

    print("Filtered data saved to output/p3/filtered_interpolated_information.csv")


def normalize_data(time_series_path):
    # Load the data
    # keep_default_na=False prevents 'NA' (Namibia) from being parsed as a missing value
    geo_weights_path = 'data/piracy_search_geo.csv'

    ts_df = pd.read_csv(time_series_path, index_col='date', keep_default_na=False)
    weights_df = pd.read_csv(geo_weights_path, keep_default_na=False)
    
    # Clean up column names in case there are trailing spaces
    weights_df.columns = weights_df.columns.str.strip()
    
    # Create a dictionary mapping country codes to their relative global weight
    weights_dict = weights_df.set_index('Codes')['Piracy Searches'].to_dict()
    
    # Create a copy of the time series dataframe to hold normalized data
    normalized_df = ts_df.copy()
    
    # Apply the normalization
    for col in normalized_df.columns:
        if col in weights_dict:
            # Convert weight to a multiplier (e.g., 50 becomes 0.5)
            weight = float(weights_dict[col]) / 100.0
            
            # Multiply the timeline values by the country's specific weight
            normalized_df[col] = pd.to_numeric(normalized_df[col], errors='coerce') * weight
        else:
            # If the country code isn't in the weights file, mark as None
            normalized_df[col] = None

    normalized_df.to_csv('output/p2/normalized_piracy_searches.csv')

    print("Normalized data saved to output/p2/normalized_piracy_searches.csv")

