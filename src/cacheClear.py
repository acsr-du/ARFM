import os

def cacheClear():
    
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
        # Add more folder paths here
    ]

    clear_multiple_folders(folders_to_clear)
