from vosk import Model, KaldiRecognizer

import pyaudio

class Listen:

    def __init__(self):
        model = Model(r"./vosk-model-small-en-us-0.15")
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
    
    def text_to_number (self, text):
        updated = ""
        text = text.split(" ")
        for t in text:
            if (t == "one"):
                updated += "1"
            elif (t == "two"):
                updated += "2"
            elif (t == "three"):
                updated += "3"
            elif (t == "four"):
                updated += "4"
            elif (t == "five"):
                updated += "5"
            elif (t == "six"):
                updated += "6"
            elif (t == "seven"):
                updated += "7"
            elif (t == "eight"):
                updated += "8"
            elif (t == "nine"):
                updated += "9"
            elif (t == "zero"):
                updated += "0"
            else:
                updated += t
        return updated

            

