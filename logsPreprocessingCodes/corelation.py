#correlation rows program


import pandas as pd

def corrrel():
    # Read the CSV file
    df = pd.read_csv('/var/vMalwareDetector/analysis/preprocessing/csv/normalise.csv', header=[0], index_col=[0])

    # Calculate the correlation matrix
    corr_matrix = df.iloc[1:, 1:].corr()

    # Set a correlation threshold
    correlation_threshold = 0.6

    # Find less correlated rows
    less_correlated_rows = set()
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            if abs(corr_matrix.iloc[i, j]) < correlation_threshold:
                colname_i = corr_matrix.columns[i]
                colname_j = corr_matrix.columns[j]
                less_correlated_rows.add(colname_i)
                less_correlated_rows.add(colname_j)

    # Drop less correlated rows
    df = df.drop(less_correlated_rows)

    # Save the modified DataFrame to a new CSV file
    # df.to_csv('output.csv')
    # Save the modified DataFrame to a text file
    with open('/var/vMalwareDetector/analysis/preprocessing/csv/output.txt', 'w') as file:
        for row_name in df.index:
            file.write(row_name + '\n')