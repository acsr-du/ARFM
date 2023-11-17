# Nomalization

from sklearn.preprocessing import MinMaxScaler
import pandas as pd

def normalize():
    df = pd.read_csv("/var/vMalwareDetector/analysis/preprocessing/csv/output_markov_chain.csv")
    encoder = MinMaxScaler()

    # Selecting columns to normalize
    columns_to_normalize = df.columns[1:]

    # Perform normalizationZ
    df[columns_to_normalize] = encoder.fit_transform(df[columns_to_normalize]).round(2)

    # Print the first few rows of the normalized dataframe
    # print(df.head())
    df.to_csv("/var/vMalwareDetector/analysis/preprocessing/csv/normalise.csv",index=False)