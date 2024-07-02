import os
from SubFunction.b64_to_image import convert_base64_to_image  #(importing b64_to_image python file)

# Function to process a person's folder
def process_person_folder(person_folder):
    base64_files = [file for file in os.listdir(person_folder) if file.endswith('_base64.txt')]
    
    for base64_file in base64_files:
        base64_file_path = os.path.join(person_folder, base64_file)
        
        # Read the base64 file
        with open(base64_file_path, 'r') as file:
            base64_string = file.read()
        
        # Define the image file name and path
        image_file_name = os.path.splitext(base64_file)[0] + '.jpg'  # Assuming the images are in JPG format
        image_file_path = os.path.join(person_folder, image_file_name)
        
        # Convert base64 string to image and save
        convert_base64_to_image(base64_string, image_file_path)
        
        # Delete the base64 file
        os.remove(base64_file_path)


# Function to process the data folder
def process_data_folder(data_folder):
    # Get a list of all subfolders (persons)
    person_folders = [os.path.join(data_folder, subfolder) for subfolder in os.listdir(data_folder) if os.path.isdir(os.path.join(data_folder, subfolder))]
    
    for person_folder in person_folders:
        process_person_folder(person_folder)
    
    print("All base64 files have been converted to images and the base64 files have been deleted.")