from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import csv
import cv2
import os
import dlib
import sqlite3
import base64     
import logging
from SubFunction.D_create_Mean_Extract import return_features_mean_personX,return_128d_features
from SubFunction.Remove_person_subfol import remove_all_person_folders

# Use frontal face detector of Dlib
detector = dlib.get_frontal_face_detector()

# Get face landmarks
predictor = dlib.shape_predictor('data/data_dlib/shape_predictor_68_face_landmarks.dat')

# Use Dlib resnet50 model to get 128D face descriptor
face_reco_model = dlib.face_recognition_model_v1("data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

def get_db_connection():
    conn = sqlite3.connect('attendance.db')
    conn.row_factory = sqlite3.Row
    return conn

UPLOAD_FOLDER = 'data/data_faces_from_camera'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/')
def index():
    return 'Hello, use the /upload endpoint to upload your images.'

@app.route('/upload', methods=['POST'])
def upload():
    try:
        data = request.get_json()
        imageDataUrls = data.get('imageDataUrls', [])
        username = data.get('username', 'default_user')


        user_folder = os.path.join(UPLOAD_FOLDER, username)
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)

        filenames = []
        for i, imageDataUrl in enumerate(imageDataUrls):
            # Extract base64 image data
            base64_str = imageDataUrl.split(',')[1]
            img_data = base64.b64decode(base64_str)

            # Save image to user's folder
            filename = f'{username}_image_{i+1}.jpg'
            filepath = os.path.join(user_folder, filename)
            
            with open(filepath, 'wb') as f:
                f.write(img_data)

            filenames.append(filename)
        feature()
        
        return jsonify({'filenames': filenames}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_attendance', methods=['GET'])
def get_attendance():
    date = request.args.get('date')
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, time FROM attendance WHERE date = ?", (date,))
    rows = cur.fetchall()
    conn.close()

    if not rows:
        return jsonify({'message': 'No records found for the given date'}), 404

    attendance_list = [{'name': row['name'], 'time': row['time']} for row in rows]
    return jsonify(attendance_list), 200



def feature():
    print("EXTRACTING FEATURES:")
    logging.basicConfig(level=logging.INFO)
    person_list = os.listdir(UPLOAD_FOLDER)
    person_list.sort()
    with open("data/features_all.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for person in person_list:
            print("BELOW IS PERSON NAME")
            print(person)
            # Get the mean/average features of face/personX, it will be a list with a length of 128D
            logging.info("%sperson_%s", UPLOAD_FOLDER, person)
            features_mean_personX = return_features_mean_personX(person)
            
            if len(person.split('_', 2)) == 2:
                # "person_x"
                person_name = person
            else:
                # "person_x_tom"
                person_name = person.split('_', 2)[-1]
            features_mean_personX = np.insert(features_mean_personX, 0, person_name, axis=0)
            # features_mean_personX will be 129D, person name + 128 features
            writer.writerow(features_mean_personX)
            logging.info('\n')
        
        
        logging.info("Save all the features of faces registered into: data/features_all.csv")
    
    # Remove all person subfolders after processing
    remove_all_person_folders(UPLOAD_FOLDER)



# Function to return 128D features for a single image


# Function to return the mean value of 128D face descriptor for person X

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)