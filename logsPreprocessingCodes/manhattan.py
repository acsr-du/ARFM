#mahanttan distance

import csv

def manhattandst():
    def manhattan_distance(point1, point2):
        distance = sum(abs(a - b) for a, b in zip(point1, point2))
        return distance

    def calculate_distances(input_csv):
        distances = []
        with open(input_csv, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = [list(map(float, row[1:])) for i, row in enumerate(reader) if i != 0]

        for i in range(len(data)):
            row_distances = []
            for j in range(len(data)):
                distance = manhattan_distance(data[i], data[j])
                row_distances.append(distance)
            distances.append(row_distances)

        return distances

    def write_csv(distances, input_csv, output_csv):
        with open(input_csv, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the first row
            row_names = [row[0] for row in reader]  # Get row names from input CSV (excluding the first column)

        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Write the first column with row names
            writer.writerow([''] + row_names)

            # Write the remaining rows with distances
            for i, row in enumerate(distances):
                writer.writerow([row_names[i]] + row)


                # Specify the input and output file paths
    input_csv = '/var/vMalwareDetector/analysis/preprocessing/csv/test.csv'
    output_csv = '/var/vMalwareDetector/analysis/preprocessing/csv/output_markov_chain.csv'

    # Calculate the distances
    distances = calculate_distances(input_csv)

    # Write the distances to the Markov chain CSV file
    write_csv(distances, input_csv, output_csv)