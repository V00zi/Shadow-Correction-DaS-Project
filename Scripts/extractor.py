import csv

def extract_column(file_path, column_index):
    column_data = []
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)

            # Skip header
            header = next(reader, None)
            print(f"Extracting column: {header[column_index]}, from: {file_path}")
            for row in reader:
                if len(row) > column_index and row[column_index]:
                    column_data.append(row[column_index])
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return column_data

def build_timeframe(start, end):
    tf_list = []
    for i, j in zip(start, end):
        tf_list.append(i + ' ' + j)
    return tf_list