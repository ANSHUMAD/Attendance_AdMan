import logging
import os
import pandas as pd


#  "features_all.csv"  / Get known faces from "features_all.csv"
def get_face_database(self):
    if os.path.exists("data/features_all.csv"):
        path_features_known_csv = "data/features_all.csv"
        csv_rd = pd.read_csv(path_features_known_csv, header=None)
        for i in range(csv_rd.shape[0]):
            features_someone_arr = []
            self.face_name_known_list.append(csv_rd.iloc[i][0])
            for j in range(1, 129):
                if csv_rd.iloc[i][j] == '':
                    features_someone_arr.append('0')
                else:
                    features_someone_arr.append(csv_rd.iloc[i][j])
            self.face_features_known_list.append(features_someone_arr)
        logging.info("Faces in Database: %d", len(self.face_features_known_list))
        return 1
    else:
        logging.warning("'features_all.csv' not found!")
        logging.warning("Please run 'get_faces_from_camera.py' "
                        "and 'features_extraction_to_csv.py' before 'face_reco_from_camera.py'")
        return 0