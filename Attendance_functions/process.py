import logging
import cv2
import dlib

# Dlib  / Use frontal face detector of Dlib
detector = dlib.get_frontal_face_detector()

# Dlib landmark / Get face landmarks
predictor = dlib.shape_predictor('data\data_dlib\shape_predictor_68_face_landmarks.dat')

# Dlib Resnet Use Dlib resnet50 model to get 128D face descriptor
face_reco_model = dlib.face_recognition_model_v1("data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")


#  Face detection and recognition wit OT from input video stream
def process(self, stream):
    
    # 1.  Get faces known from "features.all.csv"
    if self.get_face_database():
        while stream.isOpened():
            self.frame_cnt += 1
            logging.debug("Frame " + str(self.frame_cnt) + " starts")
            flag, img_rd = stream.read()
            kk = cv2.waitKey(1)

            # 2.  Detect faces for frame X
            faces = detector(img_rd, 0)

            # 3.  Update cnt for faces in frames
            self.last_frame_face_cnt = self.current_frame_face_cnt
            self.current_frame_face_cnt = len(faces)

            # 4.  Update the face name list in last frame
            self.last_frame_face_name_list = self.current_frame_face_name_list[:]

            # 5.  update frame centroid list
            self.last_frame_face_centroid_list = self.current_frame_face_centroid_list
            self.current_frame_face_centroid_list = []
            
            # 6.1  if cnt not changes
            if (self.current_frame_face_cnt == self.last_frame_face_cnt) and (
                    self.reclassify_interval_cnt != self.reclassify_interval):
                logging.debug("scene 1:   No face cnt changes in this frame!!!")
                self.current_frame_face_position_list = []
                if "unknown" in self.current_frame_face_name_list:
                    self.reclassify_interval_cnt += 1
                if self.current_frame_face_cnt != 0:
                    for k, d in enumerate(faces):
                        self.current_frame_face_position_list.append(tuple(
                            [faces[k].left(), int(faces[k].bottom() + (faces[k].bottom() - faces[k].top()) / 4)]))
                        self.current_frame_face_centroid_list.append(
                            [int(faces[k].left() + faces[k].right()) / 2,
                             int(faces[k].top() + faces[k].bottom()) / 2])
                        img_rd = cv2.rectangle(img_rd,
                                               tuple([d.left(), d.top()]),
                                               tuple([d.right(), d.bottom()]),
                                               (255, 255, 255), 2)
                        
                #  Multi-faces in current frame, use centroid-tracker to track
                if self.current_frame_face_cnt != 1:
                    self.centroid_tracker()
                for i in range(self.current_frame_face_cnt):
                    # 6.2 Write names under ROI
                    img_rd = cv2.putText(img_rd, self.current_frame_face_name_list[i],
                                         self.current_frame_face_position_list[i], self.font, 0.8, (0, 255, 255), 1,
                                         cv2.LINE_AA)
                # self.draw_note(img_rd)

            # 6.2  If cnt of faces changes, 0->1 or 1->0 or ...
            else:
                logging.debug("scene 2: / Faces cnt changes in this frame")
                self.current_frame_face_position_list = []
                self.current_frame_face_X_e_distance_list = []
                self.current_frame_face_feature_list = []
                self.reclassify_interval_cnt = 0

                # 6.2.1  Face cnt decreases: 1->0, 2->1, ...
                if self.current_frame_face_cnt == 0:
                    logging.debug("  / No faces in this frame!!!")

                    # clear list of names and features
                    self.current_frame_face_name_list = []

                # 6.2.2 / Face cnt increase: 0->1, 0->2, ..., 1->2, ...
                else:
                    logging.debug("  scene 2.2  Get faces in this frame and do face recognition")
                    self.current_frame_face_name_list = []

                    for i in range(len(faces)):
                        shape = predictor(img_rd, faces[i])
                        self.current_frame_face_feature_list.append(
                            face_reco_model.compute_face_descriptor(img_rd, shape))
                        self.current_frame_face_name_list.append("unknown")

                    # 6.2.2.1 Traversal all the faces in the database
                    for k in range(len(faces)):
                        logging.debug("  For face %d in current frame:", k + 1)
                        self.current_frame_face_centroid_list.append(
                            [int(faces[k].left() + faces[k].right()) / 2,
                             int(faces[k].top() + faces[k].bottom()) / 2])
                        self.current_frame_face_X_e_distance_list = []

                        # 6.2.2.2  Positions of faces captured
                        self.current_frame_face_position_list.append(tuple(
                            [faces[k].left(), int(faces[k].bottom() + (faces[k].bottom() - faces[k].top()) / 4)]))
                        
                        # 6.2.2.3 
                        # For every faces detected, compare the faces in the database
                        for i in range(len(self.face_features_known_list)):
                            # 
                            if str(self.face_features_known_list[i][0]) != '0.0':

                                e_distance_tmp = self.return_euclidean_distance(self.current_frame_face_feature_list[k], self.face_features_known_list[i])
                                
                                logging.debug("      with person %d, the e-distance: %f", i + 1, e_distance_tmp)
                                self.current_frame_face_X_e_distance_list.append(e_distance_tmp)

                            else:
                                #  person_X
                                self.current_frame_face_X_e_distance_list.append(999999999)

                        # 6.2.2.4 / Find the one with minimum e distance
                        similar_person_num = self.current_frame_face_X_e_distance_list.index(
                            min(self.current_frame_face_X_e_distance_list))
                        if min(self.current_frame_face_X_e_distance_list) < 0.4:
                            self.current_frame_face_name_list[k] = self.face_name_known_list[similar_person_num]
                            logging.debug("  Face recognition result: %s",
                                          self.face_name_known_list[similar_person_num])
                            
                            # Insert attendance record
                            nam =self.face_name_known_list[similar_person_num]
                            print(type(self.face_name_known_list[similar_person_num]))
                            print(nam)
                            self.attendance(nam)
                        else:
                            logging.debug("  Face recognition result: Unknown person")
                    # 7.  / Add note on cv2 window
                    # self.draw_note(img_rd)
            # 8.  'q'  / Press 'q' to exit
            if kk == ord('q'):
                break
            self.update_fps()
            # cv2.namedWindow("camera", 1)
            # cv2.imshow("camera", img_rd)
            logging.debug("Frame ends\n\n")