import pandas as pd

def clean_data(input_file):
    try:
        df = pd.read_csv(input_file, index_col=0)
        df_cleaned = df[df.sum(axis=1) > 0]

        original_rows = len(df)
        cleaned_rows = len(df_cleaned)
        rows_removed = original_rows - cleaned_rows

        print(f"Cleaning complete!")
        print(f"Original rows: {original_rows} rows")
        print(f"Cleaned rows: {cleaned_rows} rows")
        print(f"Removed {rows_removed} rows containing all zeros")
        return df_cleaned

    except FileNotFoundError:
        print(f"Error: The input file '{input_file}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def interpolate_info(df):
    try:
        if df is None or df.empty:
            print("\nDataFrame is empty. Nothing to extract.")
            return

        # Read the delisted data to get the delist dates
        try:
            delisted_df = pd.read_csv("output/p3/sampled_delisted.csv")
            # The first column might have a leading space, so strip whitespace from column names
            delisted_df.columns = delisted_df.columns.str.strip()
            # And from the 'Name' column values
            delisted_df['Name'] = delisted_df['Name'].str.strip()
            delist_date_map = pd.Series(delisted_df.Changed.values, index=delisted_df.Name).to_dict()
        except FileNotFoundError:
            print("Error: Sample file not found in output folder")
            delist_date_map = {} # Keep going without the delist dates

        df.index = pd.to_datetime(df.index)

        positive_trends_data = []
        for column in df.columns:
            # The column name from the trends df should match the 'Name' in the delisted_df
            keyword = column.strip() # Make sure to strip whitespace
            positive_trends = df[df[column] > 0]

            if not positive_trends.empty:
                delist_date = delist_date_map.get(keyword, 'N/A') # Get the delist date
                for date, row in positive_trends.iterrows():
                    trend_value = row[column]
                    positive_trends_data.append({
                        'Keyword': keyword,
                        'Date': date.strftime('%Y-%m-%d'),
                        'Value': trend_value,
                        'Date Delisted': delist_date
                    })

        if positive_trends_data:
            positive_trends_df = pd.DataFrame(positive_trends_data)
            # Reorder columns to have Date Delisted next to the keyword if desired, but this order is fine.
            output_filename = "output/p3/interpolated_infomation.csv"
            positive_trends_df.to_csv(output_filename, index=False)
            print(f"\nPositive trend dates have been written to '{output_filename}'")
        else:
            print("\nNo dates with search trend > 0 found for any keyword.")

    except Exception as e:
        print(f"An error occurred while extracting dates: {e}")