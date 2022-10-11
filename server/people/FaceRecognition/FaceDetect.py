import os
import face_recognition
import cv2
import numpy as np
import time


class Face:

    def __init__(self,face,name):
        self.known_face_encodings = face
        self.known_face_names = name
        #print('face',self.known_face_encodings)
        #print('name',self.known_face_names)

    def find(self):
        video_capture = cv2.VideoCapture(0)
        max_count = 2
        count = 0
        start = time.time()
        while count < (max_count+1):
            #print('in while',count)
            #count += 1
            ret, frame = video_capture.read()
            rgb_frame = frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_frame)
            fl = len(face_locations)
            if fl != 0:
                #print('Faces found : ',fl)
                """
                for (top, right, bottom, left) in face_locations:
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    #print('single face count :',cnt,'       Time Taken : ',(temp2 - temp))
                    cv2.imshow('Video', frame)
                    cv2.waitKey(1)
                """
                if fl != 1:
                    cnt = 0
                    print('*'*20)
                    print(' '*5,'multiple faces detected')
                    print('*'*20)
                else:
                    count += 1

                if count == max_count:
                    print('last')
                    name = self.get_name(rgb_frame,face_locations)
                    return name
            else:
                current = time.time()
                if current-start > 5:
                    return "No Face"
                print('no face')

    def get_name(self,rgb_frame,face_locations):

        face_encoding = (face_recognition.face_encodings(rgb_frame, face_locations))[0]
        matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = self.known_face_names[best_match_index]
            return name

    def add(self):
        video_capture = cv2.VideoCapture(0)
        capture = True
        start_time = time.time()
        while capture:
            ret, frame = video_capture.read()
            cv2.imshow('This is what would be captured', frame)
            current_time = time.time()
            # print(current_time - start_time)
            if cv2.waitKey(1) & (current_time - start_time >= 5):  # 0xFF == ord(' '):
                capture = False
                cv2.destroyWindow("This is what would be captured")
                base = os.getcwd()
                new = os.path.join(base,'people','static','people')
                os.chdir(new)

                n = str(int(time.time()))
                file = n + '.jpg'
                cv2.imwrite(file, frame)

                a = face_recognition.load_image_file(file)
                # print('a', a)
                b = face_recognition.face_encodings(a)[0]
                #self.known_face_encodings.append(b)
                #c = (n.split('.'))[0]
                #self.known_face_names.append(n)
                os.chdir(base)
                return [file,b]


