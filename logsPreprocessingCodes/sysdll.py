#1
#for system calls and dll extraction
# create three folders manually output1, vectors1, test1
# also make one separate folder called processed_data. 


import os
import re
import pandas as pd
import csv
from natsort import natsorted


def extract_unique_pids(file):
    pid_list = []
    seen_pids = set()
    for line in file:
        if line.startswith('[INJECT]'):
            pid = int(line.split('INJECTED_PID:')[1].split()[0])
            if pid not in seen_pids and pid != 0:
                pid_list.append(pid)
                seen_pids.add(pid)
        elif 'PPID:' in line:
            ppid = int(line.split('PPID:')[1].split()[0])
            if ppid in seen_pids:
                pid = int(line.split('PID:')[1].split()[0])
                if pid not in seen_pids and pid != 0:
                    pid_list.append(pid)
                    seen_pids.add(pid)
    return pid_list




def extract_lines_with_pids(file, pid_list, output_file):
    lines_with_pids = []
    for line in file:
        if "PID:" + str(4) not in line and "PPID:" + str(0) not in line:
            if any("PID:" + str(pid) in line for pid in pid_list):
                if "[SYSCALL]" in line or "[FILETRACER]" in line or "SYSRET" in line:
                    if any("PID:" + str(pid) in line for pid in pid_list) and ("[SYSCALL]" in line or "[FILETRACER]" in line or "SYSRET" in line):
                        lines_with_pids.append(line.strip())
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in lines_with_pids:
            f.write(line + "\n")



def process_file(folder_path, filename):
    filepath = os.path.join(folder_path, filename)
    print("Processing file:", filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        pid_list = extract_unique_pids(f)
        print(filepath, pid_list)
        for pid in pid_list:
            pid_output_file = os.path.join('/var/vMalwareDetector/analysis/preprocessing/output', f'{filename[:-4]}_{pid}.txt')
            with open(filepath, 'r', encoding='utf-8') as file:  # Open a new file handle for reading
                extract_lines_with_pids(file, [pid], pid_output_file)
    return filename, pid_list



def vector():
    # specify the path to the input folder containing the files
    input_folder_path = "/var/vMalwareDetector/analysis/preprocessing/output"

    # specify the path to the output folder
    output_folder_path = "/var/vMalwareDetector/analysis/preprocessing/vector"

    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # iterate over the files in the input folder
    for input_filename in os.listdir(input_folder_path):
        input_file_path = os.path.join(input_folder_path, input_filename)
        if os.path.isfile(input_file_path):
            # create the output file name by adding "_output" to the input file name
            output_filename = input_filename.replace(f"{input_filename}", f"{input_filename}")
            output_file_path = os.path.join(output_folder_path, output_filename)
            with open(input_file_path, "r", encoding="utf-8") as input_file, open(output_file_path, "w") as output_file:
                for line in input_file:
                    if line.startswith("[SYSCALL]"):
                        syscall_matches = re.findall(r"\bNt\w+\b", line)
                        for syscall_word in syscall_matches:
                            output_file.write(syscall_word + "\n")
                    elif line.startswith("[FILETRACER]"):
                        filetracer_matches = re.findall(r"\b\w+\.dll\b", line)
                        for filetracer_word in filetracer_matches:
                            output_file.write(filetracer_word + "\n")
    [os.remove(os.path.join(input_folder_path, file)) for file in os.listdir(input_folder_path)]




# Get the folder path from the user
def csv_maker():

    input_folder_path = "/var/vMalwareDetector/analysis/preprocessing/vector"
    output_folder_path = "/var/vMalwareDetector/analysis/preprocessing/test"

    # Get a list of all the text files in the input folder
    txt_files = [os.path.join(input_folder_path, f) for f in os.listdir(input_folder_path) if f.endswith('.txt')]

    for txt_file in txt_files:
        # Open the text file in read mode
        with open(txt_file, 'r') as file:
            # Read all the lines into a list
            lines = file.readlines()

        # Initialize an empty dictionary to store the frequency count
        freq = {}

        # Loop through each line in the list of lines
        for line in lines:
            # Split the line into individual words
            words = line.strip().split()
            # Loop through each word in the list of words
            for word in words:
                # If the word is already in the dictionary, increment its count by 1
                if word in freq:
                    freq[word] += 1
                # If the word is not in the dictionary, add it with a count of 1
                else:
                    freq[word] = 1

        # Get the base name of the text file (without the extension)
        base_name = os.path.splitext(os.path.basename(txt_file))[0]

        # Generate the name for the output CSV file
        csv_file = os.path.join(output_folder_path, base_name + '.csv')

        # Write the frequency counts to the CSV file with the same name as the input file
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            # Write the header row
            writer.writerow(['Executable_name'] + list(freq.keys()))
            # Write the frequency counts as a row in the CSV file
            writer.writerow([os.path.splitext(os.path.basename(txt_file))[0]] + list(freq.values()))

    [os.remove(os.path.join(input_folder_path, file)) for file in os.listdir(input_folder_path)]





def csv_merge(pid_lists):
    # read the first CSV file
    m_folder_path = '/var/vMalwareDetector/analysis/preprocessing/test'

    # Get a list of CSV files in the folder
    csv_files = [f for f in os.listdir(m_folder_path) if f.endswith('.csv')]

    # Sort the list of files
    csv_files.sort()

    # Read the first CSV file in the list
    if csv_files:
        first_csv_file = csv_files[0]
        df1 = pd.read_csv(os.path.join(m_folder_path, first_csv_file))
    else:
        print("No CSV files found in the folder.")
    # read all CSV files in the folder except the first one
    dfs = []
    for filename, pid_list in pid_lists:
        for pid in pid_list:
            csv_file = f"{filename[:-4]}_{pid}.csv"
            if csv_file in csv_files:
                df = pd.read_csv(os.path.join(m_folder_path, csv_file))
                dfs.append(df)
    df2 = pd.concat(dfs)

    # merge the two dataframes on a common column and keep all columns
    merged_df = pd.merge(df1, df2, how='outer')

    # fill in any missing values with zeroes
    merged_df.fillna(0, inplace=True)

    # write the merged dataframe to a new CSV file
    # output csv path change if you want to change the csv generation to other location     
    merged_df.to_csv('/var/vMalwareDetector/analysis/preprocessing/csv/test.csv', index=False) 
    [os.remove(os.path.join(m_folder_path, file)) for file in os.listdir(m_folder_path)]



def syscallDLLextractor():
    folder_path = "/var/vMalwareDetector/analysis/logs/memorylogs/extracted"
    filenames = [filename for filename in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, filename)) and not filename.startswith("ne")]
    sorted_filenames = natsorted(filenames)  # Sort the filenames in desired order

    pid_lists = []

    for filename in sorted_filenames:  # Iterate over sorted filenames
        result = process_file(folder_path, filename)
        pid_lists.append(result)

    vector()
    csv_maker()
    csv_merge(pid_lists)