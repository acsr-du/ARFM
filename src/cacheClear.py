import os

def cacheClear():

    directory_path = "/home/pc-02/drakvuf"
    drakvuf_file_name = "processed_exec.txt"
    drakvuf_file_path = os.path.join(directory_path, drakvuf_file_name)

    # Check if the file exists
    if os.path.exists(drakvuf_file_path):
        # Open the file in write mode to empty its content
        with open(drakvuf_file_path, "w") as file:
            file.truncate(0)
        print(f"Content of {drakvuf_file_name} has been emptied.")
    else:
        print(f"{drakvuf_file_name} does not exist in {directory_path}.")


    def clear_folder(folder_path):
        try:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Removed: {file_path}")
        except Exception as e:
            print(f"Error clearing folder {folder_path}: {e}")

    def clear_multiple_folders(folder_paths):
        for folder_path in folder_paths:
            clear_folder(folder_path)

    folders_to_clear = [
        "/var/LearnStreamlit/cacheClear.py",
        # Add more folder paths here
    ]

    clear_multiple_folders(folders_to_clear)