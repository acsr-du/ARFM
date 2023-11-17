import os
import concurrent.futures



def extract_second_inject_pid(filename):
    pid_list = []
    seen_pids = set()
    line_counter = 0

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('[INJECT]'):
                line_counter += 1
                if line_counter == 2:  # Process only the second line starting with [INJECT]
                    pid = int(line.split('INJECTED_PID:')[1].split()[0])
                    if pid not in seen_pids:
                        pid_list.append(pid)
                        seen_pids.add(pid)
                    break  # Stop reading after processing the second line

    return pid_list


def extract_lines_with_pids(filename, pid_list, output_file):
    lines_to_write = []
    include_line = False  # Flag to indicate if the current line should be included

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('[INJECT]'):
                include_line = True  # Start including lines from this point
                lines_to_write.append(line.strip())  # Include the [INJECT] line
                continue

            if include_line and any("PID:" + str(pid) in line for pid in pid_list):
                lines_to_write.append(line.strip())

    with open(output_file, 'w', encoding='utf-8') as f:
        for line in lines_to_write:
            f.write(line + "\n")
            

def process_file(folder_path, output_folder, filename):
    full_path = os.path.join(folder_path, filename)
    if filename.startswith("ne"):
        print("Non executed malware sample", filename)
    else:
        print("Processing file:", filename)
        pid_list = extract_second_inject_pid(full_path)
        print(filename, pid_list)
        output_file = os.path.join(output_folder, f'{filename}')
        extract_lines_with_pids(full_path, pid_list, output_file)

def malwarelogExtractor():
    folder_path = '/var/vMalwareDetector/analysis/logs/memorylogs/executed'
    output_folder = '/var/vMalwareDetector/analysis/logs/memorylogs/extracted'  # Specify the output folder path
    os.makedirs(output_folder, exist_ok=True)  # Create the output folder if it doesn't exist
    filenames = [filename for filename in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, filename)) and not filename.startswith("ne")]
    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
        for filename in filenames:
            executor.submit(process_file, folder_path, output_folder, filename)