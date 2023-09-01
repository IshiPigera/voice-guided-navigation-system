import pyttsx3
import speech_recognition as sr
import spacy
from plyer import vibrator
import pyautogui

# Initialize spaCy
nlp = spacy.load("en_core_web_sm")

# Initialize the recognizer
r = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)

# Function to provide haptic feedback
def provide_haptic_feedback():
    # vibrator.vibrate(0.1)
    pyautogui.move(1, 1)

# Function to extract keywords from a command
def extract_keywords(command):
    # Split the command into words
    words = command.split()
    
    # Filter out common words (e.g., "get", "for", "the", "and", etc.)
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
        if command == "scan":
            engine.say("Starting environment scan")
            engine.runAndWait()
            provide_haptic_feedback()  # Provide haptic feedback for scan
        elif command.startswith("get"):
            object_label = command.split()[1]
            engine.say(f"Searching for object: {object_label}")
            engine.runAndWait()
            provide_haptic_feedback()  # Provide haptic feedback for object search
            # Extract keywords from the command
            keywords = extract_keywords(command)
            print("Keywords:", keywords)
        elif command.startswith("obstacle detected"):
            engine.say(f"Obstacle detected in the path")
            engine.runAndWait()
            provide_haptic_feedback()  # Provide haptic feedback for obstacle detection
        else:
            engine.say("Invalid command.")
            engine.runAndWait()
    else:
        print("No command detected.")
