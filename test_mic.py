#!/usr/bin/env python3
"""
Test microphone for F.R.I.D.A.Y.
"""

import speech_recognition as sr

def test_microphone():
    print("Testing microphone...")
    print("Say something (will timeout after 5 seconds)")
    
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            print("Got audio, recognizing...")
            
            # Test with Google (requires internet)
            try:
                text = recognizer.recognize_google(audio)
                print(f"You said: {text}")
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results: {e}")
                
        except sr.WaitTimeoutError:
            print("No speech detected")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_microphone()
