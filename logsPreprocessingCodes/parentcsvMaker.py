# 9
#parent csv maker

import pandas as pd

def parrentcsv():
    def extract_unique_names(csv_file):
        # Read the CSV file
        df = pd.read_csv(csv_file)

        # Extract the prefix before the underscore
        df['Prefix'] = df.iloc[:, 0].str.split('_').str[0]

        # Set to store the printed values
        printed_values = set()

        # List to store the printed values
        printed_values_list = []

        # Iterate over the rows of the DataFrame
        for _, row in df.iterrows():
            value = row.iloc[0]
            prefix = row['Prefix']

            # Check if the prefix has been encountered before
            if prefix not in printed_values:
                # Append the first occurrence to the list
                printed_values_list.append(value)

                # Add the prefix to the set of printed values
                printed_values.add(prefix)

                # Remove the non-first occurrences
                df = df[df['Prefix'] != prefix]

        # Return the first occurrences
        return printed_values_list


    # Call the function to extract unique names
    unique_names = extract_unique_names('/var/vMalwareDetector/analysis/preprocessing/csv/test.csv')

    # Read the CSV file again
    df = pd.read_csv('/var/vMalwareDetector/analysis/preprocessing/csv/test.csv')

    # Filter the DataFrame to include only rows with matching names
    filtered_df = df[df.iloc[:, 0].isin(unique_names)]

    # Save the filtered DataFrame to a new CSV file
    filtered_df.to_csv('/var/vMalwareDetector/analysis/preprocessing/csv/parent.csv', index=False)
