#10
# child process csv maker
import csv
from collections import Counter

def childcsv():
    # Read the text file containing names
    with open('/var/vMalwareDetector/analysis/preprocessing/csv/output.txt', 'r') as text_file:
        names = text_file.read().splitlines()

    # Read the CSV file
    with open('/var/vMalwareDetector/analysis/preprocessing/csv/test.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)  # Assuming the first row is the header
        rows = list(reader)

    # Count occurrences of each row in the CSV file
    row_counts = Counter(row[0] for row in rows)

    # Filter the CSV rows based on the search criteria and occurrence count
    filtered_rows = []
    found_names = set()  # Keep track of the names found in the CSV

    for row in rows:
        name = row[0]
        for text_name in names:
            if text_name in name:
                if name not in found_names:
                    filtered_rows.append(row)
                    found_names.add(name)  # Add the found name to the set
                break  # Break the inner loop once the name is found

    # Add rows with unique or two occurrences not found in the text file
    for row in rows:
        name = row[0]
        if name not in found_names and row_counts[name] <= 2:
            filtered_rows.append(row)
            found_names.add(name)

    # Save the filtered rows to a new CSV file
    with open('/var/vMalwareDetector/analysis/preprocessing/csv/filtered_data.csv', 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(header)
        writer.writerows(filtered_rows)