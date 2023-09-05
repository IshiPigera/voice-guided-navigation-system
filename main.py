import pyttsx3
import speech_recognition as sr
import spacy
from plyer import vibrator
import pyautogui
import time
import subprocess

# Initialize spaCy
nlp = spacy.load("en_core_web_sm")

# Initialize the recognizer
r = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)

adb_path = r'C:\Android\platform-tools\adb.exe'
# Function to vibrate the connected Android device using ADB
def vibrate_phone():
    try:
        subprocess.run([adb_path, "shell", "input", "keyevent", "KEYCODE_NUMPAD_ENTER"])
        print("Phone vibrating...")
    except Exception as e:
        print("Error while vibrating the phone:", str(e))


# Function to extract entities from a command
def extract_entities(command):
    doc = nlp(command)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

# Function to extract subject and object from a command
def extract_subject_object(command):
    doc = nlp(command)
    subject = None
    obj = None
    for token in doc:
        if "subj" in token.dep_:
            subject = token.text
        elif "obj" in token.dep_:
            obj = token.text
    return subject, obj

# Function to provide haptic feedback
def provide_haptic_feedback(duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        pyautogui.move(1, 1)
        pyautogui.move(-1, -1)

# Function to extract keywords from a command
def extract_keywords(command):
    words = command.split()
    common_words = ["get", "for", "the", "and", "with", "on", "in", "to"]
    keywords = [word for word in words if word.lower() not in common_words]
    
    return keywords

# Listen for voice command
def listen_for_command():
    with sr.Microphone() as source:
        r.energy_threshold = 300
        print("Listening for command...")
        engine.say("Hello! Welcome to Smart Eye! Listening for command...")
        engine.runAndWait()
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        print("Command:", command)
        return command.lower()
        
    except sr.UnknownValueError as e:
        print("UnknownValueError:", str(e))
        engine.say("Unable to recognize speech")
        engine.runAndWait()
        return None
    except Exception as e:
        print("An error occurred:", str(e))
        engine.say("An error occurred")
        engine.runAndWait()
        return None
    

# Main program loop
while True:
    command = listen_for_command()
    if command:
        if "scan" in command:
            engine.say("Starting environment scan")
            progress = 0

            while progress < 100:
                 
                progress += 10
                engine.say(f"Scan progress: {progress}%")
                engine.runAndWait()
                 

            engine.say("Environment scan completed")
            engine.runAndWait()   
        elif command.startswith("get"):
            object_label = command.split()[1]
            engine.say(f"Searching for object: {object_label}")
            engine.runAndWait()
            entities = extract_entities(command) 
            keywords = extract_keywords(command)
            print("Keywords:", keywords)
        elif command.startswith("obstacle detected"):
            engine.say(f"Obstacle detected in the path")
            engine.runAndWait()            
            # provide_haptic_feedback(duration=2.0)
            vibrate_phone()

        else:
            engine.say("Invalid command.")
            engine.runAndWait()
    else:
        print("No command detected.")
