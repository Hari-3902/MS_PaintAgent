import speech_recognition as sr
import time # Added for the break time

# Mic.py
# Simple microphone-to-text using the SpeechRecognition package and Google Web Speech API.
# Install dependencies:
# pip install SpeechRecognition
# pip install PyAudio or pipwin install pyaudio


def transcribe_from_mic(timeout=None, phrase_time_limit=None, adjust_for_ambient=True):
    """
    Listen to the default microphone and return the transcribed text (Google Web Speech API).
    - timeout: maximum seconds to wait for phrase to start (None = wait indefinitely)
    - phrase_time_limit: maximum seconds for a single phrase (None = unlimited)
    - adjust_for_ambient: whether to auto-adjust for ambient noise before listening
    Returns the recognized string or None on failure.
    """
    r = sr.Recognizer()
    mic = sr.Microphone()  # uses default system microphone

    with mic as source:
        if adjust_for_ambient:
            # listen for 0.8s to calibrate energy threshold for ambient noise
            r.adjust_for_ambient_noise(source, duration=0.8)
        
        print("Please speak now...")    
        try:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            print("No speech detected (timeout).")
            return None

    try:
        # Uses Google Web Speech API (requires internet).
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Speech was unintelligible.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    return None

# if __name__ == "__main__":
#     # Define a time break after the transcription finishes
#     BREAK_TIME_SECONDS = 3 
    
#     # --- Code is now executed once, not in a loop ---
#     print("Program started. Ready for input.")
    
#     # 1. Take a single input
#     result = transcribe_from_mic(timeout=5, phrase_time_limit=10)
    
#     if result:
#         print("You said:", result)
#     else:
#         print("No transcription.")
    
#     print("-" * 40)
    
#     # 2. Give time to break before ending
#     print(f"Giving a break time of {BREAK_TIME_SECONDS} seconds before exiting...")
#     time.sleep(BREAK_TIME_SECONDS) 
    
#     print("Program finished.")