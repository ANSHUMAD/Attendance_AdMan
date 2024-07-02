# / Use centroid tracker to link face_x in current frame with person_x in last frame
def centroid_tracker(self):
    for i in range(len(self.current_frame_face_centroid_list)):
        e_distance_current_frame_person_x_list = []
        #  For object 1 in current_frame, compute e-distance with object 1/2/3/4/... in last frame
        for j in range(len(self.last_frame_face_centroid_list)):
            self.last_current_frame_centroid_e_distance = self.return_euclidean_distance(
                self.current_frame_face_centroid_list[i], self.last_frame_face_centroid_list[j])
            e_distance_current_frame_person_x_list.append(
                self.last_current_frame_centroid_e_distance)
        last_frame_num = e_distance_current_frame_person_x_list.index(
            min(e_distance_current_frame_person_x_list))
        self.current_frame_face_name_list[i] = self.last_frame_face_name_list[last_frame_num]