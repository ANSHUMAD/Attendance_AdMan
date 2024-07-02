import base64
# Function to convert base64 to image
def convert_base64_to_image(base64_string, output_path):
    image_data = base64.b64decode(base64_string)
    with open(output_path, 'wb') as image_file:
        image_file.write(image_data)