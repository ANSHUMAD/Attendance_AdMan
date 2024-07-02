import os
import dlib
# import csv
import numpy as np
import logging
import cv2


# Path of cropped faces
path_images_from_camera = "data/data_faces_from_camera/"

# Use frontal face detector of Dlib
detector = dlib.get_frontal_face_detector()

UPLOAD_FOLDER = 'data/data_faces_from_camera'

# Get face landmarks
predictor = dlib.shape_predictor('data/data_dlib/shape_predictor_68_face_landmarks.dat')

# Use Dlib resnet50 model to get 128D face descriptor
face_reco_model = dlib.face_recognition_model_v1("data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")



# Function to return 128D features for a single image
def return_128d_features(path_img):
    img_rd = cv2.imread(path_img)
    faces = detector(img_rd, 1)

    logging.info("%-40s %-20s", " Image with faces detected:", path_img)

    # For photos of faces saved, we need to make sure that we can detect faces from the cropped images
    if len(faces) != 0:
        shape = predictor(img_rd, faces[0])
        face_descriptor = face_reco_model.compute_face_descriptor(img_rd, shape)
    else:
        face_descriptor = 0
        logging.warning("no face")
    return face_descriptor

# Function to return the mean value of 128D face descriptor for person X
def return_features_mean_personX(face):

    features_list_personX = []
    person_folder = os.path.join(UPLOAD_FOLDER, face)
    photos_list = os.listdir(person_folder)
    if photos_list:
        for i, photo in enumerate(photos_list):
            photo_path = UPLOAD_FOLDER + "/" + face + "/" + photo
            #image = cv2.imread(photo_path)
            print("hola")
            features_128d = return_128d_features(photo_path)
            print("5",i)

            #if features_128d == 0:
               # continue
            #else:
            features_list_personX.append(features_128d)
    else:
        logging.warning(" Warning: No images in%s/", face)
   
    if features_list_personX:
        features_mean_personX = np.array(features_list_personX, dtype=object).mean(axis=0)
    else:
        features_mean_personX = np.zeros(128, dtype=object, order='C')
       
    return features_mean_personX