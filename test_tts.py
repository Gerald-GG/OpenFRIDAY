import pyttsx3
import time

engine = pyttsx3.init()
print("Testing text-to-speech...")
engine.say("F.R.I.D.A.Y. online. Systems nominal.")
engine.runAndWait()
print("Done")
