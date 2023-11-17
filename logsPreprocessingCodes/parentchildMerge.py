# child merge to parent.
import csv

def parentchild():
    def merge_csv_files(file1, file2, output_file, key_column):
        data1 = read_csv(file1)
        data2 = read_csv(file2)

        merged_data = merge_data(data1, data2, key_column)

        write_csv(output_file, merged_data)
        print(f"Merged data saved to {output_file}")

    def read_csv(file_path):
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
        return data

    def merge_data(data1, data2, key_column):
        merged_data = []
        processed_keys = set()  # Keep track of processed keys from data2

        for row1 in data1:
            key_value = row1[key_column]
            matching_rows = [row2 for row2 in data2 if row2[key_column] == key_value]

            if matching_rows:
                for row2 in matching_rows:
                    merged_row = {**row1, **row2}
                    merged_data.append(merged_row)
                    processed_keys.add(key_value)
            else:
                merged_data.append(row1)

        # Append remaining unmatched rows from data2
        unmatched_rows = [row2 for row2 in data2 if row2[key_column] not in processed_keys]
        merged_data.extend(unmatched_rows)

        return merged_data

    def write_csv(file_path, data):
        fieldnames = data[0].keys()

        with open(file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    # Example usage
    file1 = '/var/vMalwareDetector/analysis/preprocessing/csv/parent.csv'
    file2 = '/var/vMalwareDetector/analysis/preprocessing/csv/filtered_data.csv'
    output_file = '/var/vMalwareDetector/analysis/preprocessing/csv/merged.csv'
    key_column = 'Executable_name'

    merge_csv_files(file1, file2, output_file, key_column)
