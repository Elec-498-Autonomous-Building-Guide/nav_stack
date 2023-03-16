from vosk import Model, KaldiRecognizer
from word2number import w2n

import pyaudio

class Listen:

    def __init__(self):
        model = Model(r"./vosk-model-en-us-0.22")
        self.recognizer = KaldiRecognizer(model, 16000)

        mic = pyaudio.PyAudio()
        self.stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    
    def listening (self):
        self.stream.start_stream()

        while True:
            data = self.stream.read(4096)
            
            if self.recognizer.AcceptWaveform(data):
                text = self.recognizer.Result()
                return text[14:-3]
            
    def text_to_number(self,text):
        return str(w2n.word_to_num(text))

            

