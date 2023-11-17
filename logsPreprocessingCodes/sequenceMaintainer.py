# 12
#sequence maintainer of merged csv

import pandas as pd

def sequencemaintain():
    # Read the contents of the first CSV file
    csv1 = pd.read_csv('/var/vMalwareDetector/analysis/preprocessing/csv/test.csv')

    # Read the contents of the second CSV file
    csv2 = pd.read_csv('/var/vMalwareDetector/analysis/preprocessing/csv/merged.csv')

    # Identify the column as a common identifier
    common_column = 'Executable_name'

    # Create a mapping between the common identifier and row index in the second CSV file
    mapping = {id: index for index, id in enumerate(csv2[common_column])}

    # Sort the rows in the first CSV file based on the row index in the second CSV file
    csv1['index'] = csv1[common_column].map(mapping)
    csv1.sort_values('index', inplace=True)
    csv1.drop(columns=['index'], inplace=True)

    # Write the sorted rows into a new CSV file
    csv1.to_csv('/var/vMalwareDetector/analysis/preprocessing/csv/sorted_first.csv', index=False)