import pandas as pd

def sample_from(file_path,size):
    
    df = pd.read_csv(filepath_or_buffer=file_path, encoding='utf-8')

    sampled_df = df.sample(n=size, replace=False)

    columns_to_keep = ['Name', 'Changed', "Months before (4)", "Months after (4)"]
    sampled_df_subset = sampled_df[columns_to_keep]

    sampled_df_subset.to_csv("output/sampled_delisted.csv", index=False)