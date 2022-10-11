import os
import face_recognition
import cv2
import numpy as np
from time import time as ti
import time
from .play_test import say,simple_play
from .record_test import Record
from ..server.HandelPeople import GetPeople

g = GetPeople()
a = g.get()


BASE = ''

#os.system('cls')


class StartFaceReco:
    def __init__(self, dir):
        global BASE
        BASE = self.join(self.join(dir,'SmartReceptionist'), 'FaceRecognition')
        print('BASE IN FACE', BASE)

    def join(self, path,child):
        return os.path.join(path, child)



class FindFace:
    def __init__(self):
        print('in findaface',BASE)

    def find(self):
        print('\n'*3)
        rec = Record()
        start = ti()
        print('Started process')
        temp2 = start

        BASE_DIR = os.getcwd()
        #print('Current Directory :', BASE_DIR)
        # This is a super simple (but slow) example of running face recognition on live video from your webcam.
        # There's a second example that's a little more complicated but runs faster.

        # PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
        # OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
        # specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

        # Get a reference to webcam #0 (the default one)
        video_capture = cv2.VideoCapture(0)
        temp = ti()
        print('Initialized the camera, Time taken :',(temp - temp2))
        temp2 = temp

        cnt = 0
        """
        PEOPLE_DIR = os.path.join(BASE_DIR,'people')
        os.chdir(PEOPLE_DIR)
        VOICE_DIR = os.path.join(BASE_DIR,'voice')
        
        #print("CHANGED DIR :",os.getcwd())
        people_list = os.listdir()
        
        
        #lis = ["obama.jpg","biden.jpg","CJ.jpg","fatty.jpg"]
        
        """

        """
        # Load a sample picture and learn how to recognize it.
        obama_image = face_recognition.load_image_file("obama.jpg")
        obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
        
        # Load a second sample picture and learn how to recognize it.
        biden_image = face_recognition.load_image_file("biden.jpg")
        biden_face_encoding = face_recognition.face_encodings(biden_image)[0]
        
        cj_image = face_recognition.load_image_file("CJ.jpg")
        cj_face_encoding = face_recognition.face_encodings(cj_image)[0]
        """


        # Create arrays of known face encodings and their names
        known_face_encodings = a[1]
        known_face_names = a[0]

        print('Started encoding')
        """
        for i in people_list:
            a = face_recognition.load_image_file(i)
        
            b = face_recognition.face_encodings(a)[0]
        
            known_face_encodings.append(b)
            c = (i.split('.'))[0]
            known_face_names.append(c)
        
        print("All the available people")
        """
        print(known_face_names)

        temp = ti()
        print('Encoding done in :',(temp-temp2))
        temp2 = temp

        """"= [
            obama_face_encoding,
            biden_face_encoding,
            cj_face_encoding,
        os.chdir(VOICE_DIR)
        ]"""

        def get_name():
            temp = ti()
            face_encoding = (face_recognition.face_encodings(rgb_frame, face_locations))[0]
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            print('*' * 20)
            print(' ' * 5, name)
            print('*' * 20)
            print('\n'*3)

            if name == 'Unknown':
                capture = True
                simple_play("You are not in my data base. Please smile, while i add you in it.")
                start_time = ti()
                while capture:
                    ret, frame = video_capture.read()
                    cv2.imshow('This is what would be captured',frame)
                    current_time = ti()
                    #print(current_time - start_time)
                    if cv2.waitKey(1) & (current_time-start_time >= 2.5): # 0xFF == ord(' '):
                        capture = False
                        cv2.destroyWindow("This is what would be captured")
                        """
                        while 1:
                            simple_play("are you satisfied with the photo")
                            ip = listen()
                            simple_play(ip)
                            q = input("Ok with the image ? [y/n] :")
                            if ip == "yes":#q == 'y':
                                capture = False
                                cv2.destroyWindow("This is what would be captured")
                                break
                        """

                simple_play("What is you name ?")
                while 1:
                    new_name = rec.listen()
                    print("Returned Name :",new_name)
                    if new_name:
                        print("Added to the data base")
                    else:
                        print("Sorry please try again")
                        continue
                    n = new_name + '.jpg' #input('Give a name for the new image : ') + '.jpg'
                    os.chdir(PEOPLE_DIR)
                    cv2.imwrite(n,frame)
                    break

                #print('n',n)
                a = face_recognition.load_image_file(n)
                #print('a', a)
                b = face_recognition.face_encodings(a)[0]

                known_face_encodings.append(b)
                c = (n.split('.'))[0]
                known_face_names.append(c)

                #os.chdir(VOICE_DIR)
            else:
                print(say(name))

            # Draw a box around the face
            # cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            """
            # Draw a label with a name below the face
            cv2.rectangle(frame2, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame2, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            cv2.imshow('Video', frame2)
            cv2.waitKey(10)
            """

        save_frame = 0

        while True:
            # Grab a single frame of video
            ret, frame = video_capture.read()
            frame2 = frame

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_frame = frame[:, :, ::-1]
            temp = ti()
            # Find all the faces and face enqcodings in the frame of video
            face_locations = face_recognition.face_locations(rgb_frame)
            #print('face location list;',face_locations)
            fl = len(face_locations)
            if fl != 0:
                #print('Faces found : ',fl)
                if cnt == 0:
                    save_frame = frame

                for (top, right, bottom, left) in face_locations:
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    temp2 = ti()
                    #print('single face count :',cnt,'       Time Taken : ',(temp2 - temp))
                    cv2.imshow('Video', frame)
                    cv2.waitKey(1)
                if fl != 1:
                    cnt = 0
                    print('*'*20)
                    print(' '*5,'multiple faces detected')
                    print('*'*20)
                    time.sleep(2)
                else:
                    cnt+=1

                if cnt == 10:
                    get_name()
                    cnt = 0

            else:
                cnt = 0
                temp2 = ti()
                #print('face not found.      Time taken :',(temp2-temp))

            #face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            # Loop through each face in this frame of video
            """
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        
                name = "Unknown"
        
                # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]
        
                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
        
                """
            """
                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        
                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                """

            # Display the resulting image

            cv2.imshow('Video', frame)



            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        #check who that person is :




        temp2 = ti()
        print('Time to find name :',(temp2 - temp))


        #wait for input to close the program
        while 1:
            i = input('press q to stop : ')
            if i == 'q':
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()
