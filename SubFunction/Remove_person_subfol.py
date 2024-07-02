import os
# import dlib
# import csv
# import numpy as np
import logging
# import cv2


# Function to remove a person's folder and its contents
def remove_person_folder(person_folder):
    if os.path.exists(person_folder):
        for root, dirs, files in os.walk(person_folder, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                os.rmdir(dir_path)
        os.rmdir(person_folder)
        logging.info(f"Removed {person_folder} and its contents.")
    else:
        logging.warning(f"{person_folder} does not exist.")

# Function to remove all person subfolders after processing
def remove_all_person_folders(data_folder):
    person_folders = [os.path.join(data_folder, subfolder) for subfolder in os.listdir(data_folder) if os.path.isdir(os.path.join(data_folder, subfolder))]
    
    for person_folder in person_folders:
        remove_person_folder(person_folder)
    
    print("All person subfolders have been deleted.")