import pyttsx3
import speech_recognition as sr

# Initialize the recognizer
r = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)

# Listen for voice command
def listen_for_command():
    with sr.Microphone() as source:
        print("Listening for command...")
        engine.say("Listening for command...")
        engine.runAndWait()
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        print("Command:", command)
        return command.lower()
    except sr.UnknownValueError:
        print("Unable to recognize speech")
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
        elif command.startswith("get"):
            object_label = command.split()[1]
            engine.say(f"Searching for object: {object_label}")
            engine.runAndWait()
        elif command.startswith("obstacle detected"):
        object_label = command.split()[1]
        engine.say(f"Obstacle detected in the path")
        engine.runAndWait()
        else:
            engine.say("Invalid command.")
            engine.runAndWait()
    else:
        print("No command detected.")
