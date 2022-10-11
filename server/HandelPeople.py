from django.utils import timezone
import os
import sys
import face_recognition
import numpy as np
BASEDIR = os.getcwd()
import datetime
import django
from django.core.files import File
"""
new = os.path.join(BASEDIR, 'SmartReceptionist\server')
# os.chdir(new)
sys.path.append(new)
"""
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from people.FaceRecognition.play_test import say
from people.models import People,ReceptionistDisplayMessage
print('base in handel',BASEDIR)


class AddPeople:
    def add(self):
        #os.chdir("..\FaceRecognition\people")
        people_path = os.path.join(BASEDIR,'people','FaceRecognition','people')
        os.chdir(people_path)
        #print('base',os.getcwd())
        people_list = os.listdir()
        #print('list', people_list)
        known_face_encodings = []

        known_face_names = []

        print('Started encoding',os.getcwd())

        for i in people_list:

            img = face_recognition.load_image_file(i)

            encoded_array = face_recognition.face_encodings(img)[0]
            # print('shape',encoded_array.shape)
            encoded_list = encoded_array.tolist()
            known_face_encodings.append(encoded_array)
            name = (i.split('.'))[0]
            known_face_names.append(name)
            # print('list',encoded_list)

            # If giving Voice error Just Comment the paara below

            time = datetime.datetime.now()
            
            print("name :",name)
            os.chdir(BASEDIR)
            base = os.getcwd()
            new = os.path.join(base, 'people', 'Voice')
            print('new',new)
            os.chdir(new)
            # print(os.getcwd())
            a = say(name + "  .")
            os.chdir(base)
            print('base',base)
            print("File name",a)    
            file = "people/Voice/" + a

            person = People.objects.get_or_create(name=name, face_encoding=encoded_list)[0]
            person.profile_created = time
            person.save()
            
            with open(file, 'rb') as audio:
                person.voice.save(a,File(audio))
                #person.save()
            # print(person.get(id))
            
            os.chdir(people_path)




    """
        person = People()
        person.name = name
        person.face_encoding = encoded_array
        person.profile_created = timezone.now()
        person.save()
    """


class GetPeople:
    def get(self):
        known_face_encodings = []

        known_face_names = []
        people = People.objects.all()
        for p in people:
            known_face_names.append(p.name)
            encoded_list = p.face_encoding
            numpy_array = np.array(encoded_list)
            known_face_encodings.append(numpy_array)

        return known_face_names, known_face_encodings

class MakeMessage:
    def make(self):
        s = 'how are you beautiful people, i am here to kill you, and what do you know'
        texts = s.split(',')
        print(timezone.localtime())
        print('no',timezone.now())
        for text in texts:
            message = ReceptionistDisplayMessage.objects.create(message=text,created_at=timezone.localtime())
            print('made msg:',text)


if __name__ == '__main__':
    print('runnig direct')
    a = AddPeople()
    a.add()
    #GetPeople()


