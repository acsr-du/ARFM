# 13  
# removal of pid attached to malwares strings and mergin child to parent
import pandas as pd
import csv
import re


def processed():
    # ---------------------------------------------------------------------------------------------------
    input_file = '/var/vMalwareDetector/analysis/preprocessing/csv/sorted_first.csv'
    output_file = '/var/vMalwareDetector/analysis/preprocessing/csv/soutput.csv'

    # Read the input CSV file and process the data
    output_rows = []
    with open(input_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Skip the header
        output_rows.append(header)

        for row in reader:
            modified_row = []
            first_item = row[0]  # Process only the first column
            parts = first_item.split("_")
            if parts[-1].isdigit():
                modified_row.append("_".join(parts[:-1]))
            else:
                modified_row.append(first_item)

            # Append the rest of the columns unchanged
            modified_row.extend(row[1:])
            output_rows.append(modified_row)

    # Write the processed data to the output CSV file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(output_rows)

    # ------------------------------------------------------------------------------------------------------------------


    df = pd.read_csv('/var/vMalwareDetector/analysis/preprocessing/csv/soutput.csv')

    # Create a dictionary to store rows to be added
    row_sum_dict = {}
    name_mapping = {}

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        name = row['Executable_name']

        # Remove underscore and number at the end of the name
        modified_name = re.sub(r'(_[0-9]+)$', r'\1', name)

        if modified_name not in name_mapping:
            name_mapping[modified_name] = name

        if modified_name in row_sum_dict:
            # Sum the numeric values of the rows
            row_sum_dict[modified_name][1:] += row[1:]
        else:
            # Add the whole row to the dictionary
            row_sum_dict[modified_name] = row

    # Create a new DataFrame from the dictionary values
    result_df = pd.DataFrame(list(row_sum_dict.values()), columns=df.columns)

    # Replace the modified names with the original names from the first occurrence
    result_df['Executable_name'] = result_df['Executable_name'].map(name_mapping)

    # Save the result as a new CSV file
    result_df.to_csv('/var/vMalwareDetector/analysis/preprocessing/csv/modified_result.csv', index=False)



    # ----------------------------------------------------------------------------------------------------


    
    df = pd.read_csv('/var/vMalwareDetector/analysis/preprocessing/csv/modified_result.csv')

    # Fill NaN values with zeros
    df = df.fillna(0)

    # Save the modified DataFrame back to the CSV file
    df.to_csv('/var/vMalwareDetector/analysis/preprocessing/csv/final_data.csv', index=False)