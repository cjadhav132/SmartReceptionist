 # Import the required module for text  
# to speech conversion 
from gtts import gTTS 
import time
from playsound import playsound
import os
import pyttsx3 
#import vlc
  
# This module is imported so that we can  
# play the converted audio 
import os 


def say(name):
    save = str(time.time()) + '.mp3'
    print('save',save)
    engine = pyttsx3.init() 
    engine.save_to_file(name, save)
    engine.runAndWait() 
    return save
  
    """
    language = 'en'
    myobj = gTTS(text=name, lang=language, slow=False)
    save = str(time.time()) + '.mp3'
    print(save)
    myobj.save(save)
    return save
    """
    
def simple_play(msg):
    print("Given Text for play is :",msg)
    try:
        myobj = gTTS(text=msg, lang='en', slow=False)
        myobj.save("simple_play.mp3")
        playsound("simple_play.mp3")
        os.remove("simple_play.mp3")
    except BaseException as e:
        print("this is the error in simple play", e)


#simple_play("How can i help you.")


if __name__ == "__main__":
    ip = input("Type what to say : ")
    say(ip)
    #say("Clck on the Code button, and say the code")
