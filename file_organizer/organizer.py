import os
import shutil
import json

def load_config(config_path="config.json"):
    """Load extension-to-folder mappings from config file."""
    with open(config_path, "r") as file:
        return json.load(file)

def organize_files(target_folder, config_path="config.json"):
    """Organize files based on extension rules in config.json."""
    rules = load_config(config_path)

    for filename in os.listdir(target_folder):
        file_path = os.path.join(target_folder, filename)

        if os.path.isfile(file_path):
            ext = filename.split(".")[-1].lower()

            destination = rules.get(ext, "OTHERS")

            dest_folder = os.path.join(target_folder, destination)
            os.makedirs(dest_folder, exist_ok=True)

            shutil.move(file_path, os.path.join(dest_folder, filename))
            print(f"Moved: {filename} ➝ {destination}")

if __name__ == "__main__":
    folder = input("Enter folder path to organize: ")
    organize_files(folder)
