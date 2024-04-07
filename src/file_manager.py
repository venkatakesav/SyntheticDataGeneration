import os

class FileManager:
    def is_file_processed(self, file_name, processed_files_file):
        if not os.path.exists(processed_files_file):
            return False
        with open(processed_files_file, "r") as f:
            processed_files = f.read().splitlines()
        return file_name in processed_files

    def mark_file_processed(self, file_name, processed_files_file):
        with open(processed_files_file, "a") as f:
            f.write(file_name + "\n")