import pyaudio
import wave
import speech_recognition as sr
import os

BASE_DIR = os.getcwd()
#print("record test working dir :", BASE_DIR)


class Record:
    def __init__(self):

        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.RECORD_SECONDS = 5
        self.WAVE_OUTPUT_FILENAME = "output.wav"

        self.r = sr.Recognizer()


    def listen(self):
        p = pyaudio.PyAudio()
        print("* recording")
        current = os.getcwd()
        print("While Listening this is the directory :",current)
        frames = []

        stream = p.open(format=self.FORMAT,
                             channels=self.CHANNELS,
                             rate=self.RATE,
                             input=True,
                             frames_per_buffer=self.CHUNK)

        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = stream.read(self.CHUNK)
            frames.append(data)

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        with sr.AudioFile(self.WAVE_OUTPUT_FILENAME) as source:
            # remove this if it is not working
            # correctly.
            self.r.adjust_for_ambient_noise(source)
            audio_listened = self.r.listen(source)

        try:
            # try converting it to text
            rec = self.r.recognize_google(audio_listened)
            # print(rec)
            return rec
        except BaseException as e:
            print("The error in text recognition is :", e)


if __name__ == "__main__":
    rec = Record()
    val = rec.listen()
    print(val)
