import speech_recognition as sr
import pyttsx3

# Initialize recognizer and text-to-speech engine
r = sr.Recognizer()
engine = pyttsx3.init()

# Configure text-to-speech engine (optional)
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)

def live_speech_to_text():
    with sr.Microphone() as source:
        print("Adjusting for ambient noise, please wait...")
        r.adjust_for_ambient_noise(source)  # Adjusts for ambient noise
        print("Listening...")

        while True:
            try:
                # Listen for a phrase and recognize it
                audio = r.listen(source)
                text = r.recognize_google(audio)
                
                if (text == "next line"):
                    print("")
                    print("")
                elif (text == "stop"):
                    break
                else:
                    print(f"{text} ", end='', flush=True)

                # Optional: Speak the text back
                engine.say(text)
                engine.runAndWait()

            except sr.UnknownValueError:
                print("...", end='', flush=True)
            except sr.RequestError:
                print("Sorry, there was an issue with the speech recognition service.")

live_speech_to_text()