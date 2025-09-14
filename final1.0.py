import emoji
import speech_recognition as sr
import datetime
import os
import json

# Emotion-based coping strategies with variants
coping_mechanisms = {
    "sad": "Try writing down your feelings or going for a walk.",
    "angry": "Take deep breaths or count to 10 slowly.",
    "anxious": "Practice mindfulness or guided meditation.",
    "nervous": "Take a few deep breaths and remind yourself you're doing your best.",
    "fear": "Try to ground yourself in the present moment. You're stronger than you think.",
    "excited": "That's great! Embrace the positivity and channel it.",
    "happy": "That's great! Keep doing what makes you feel this way.",
    "lonely": "Reach out to someone you trust or try journaling your feelings.",
    "stressed": "Take a short break and do something calming.",
    "overwhelmed": "Break tasks down into smaller steps. One thing at a time."
}

# Emotion emoji map
emotion_to_emoji = {
    "happy": emoji.emojize(":smile:"),
    "sad": emoji.emojize(":cry:"),
    "angry": emoji.emojize(":angry:"),
    "anxious": emoji.emojize(":fearful:"),
    "nervous": emoji.emojize(":confused:"),
    "fear": emoji.emojize(":face_with_peeking_eye:"),
    "excited": emoji.emojize(":star-struck:"),
    "lonely": emoji.emojize(":disappointed:"),
    "stressed": emoji.emojize(":weary:"),
    "overwhelmed": emoji.emojize(":dizzy_face:")
}

# Personalized library
personalized_library = {}
if os.path.exists("personalized_library.json"):
    with open("personalized_library.json", "r") as file:
        personalized_library = json.load(file)

# Speech recognizer
recognizer = sr.Recognizer()

def speech_to_text():
    with sr.Microphone() as source:
        print("Listening... Please say something.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Couldn't recognize speech. Please type your message instead.")
            return input("You (typed): ")
        except sr.RequestError:
            print("Speech recognition service failed. Please type your message instead.")
            return input("You (typed): ")

def save_diary_entry(text):
    today = datetime.date.today().isoformat()
    with open("diary.txt", "a") as file:
        file.write(f"[{today}] {text}\n")

def view_diary():
    if os.path.exists("diary.txt"):
        print("\nYour Diary Entries:\n")
        with open("diary.txt", "r") as file:
            print(file.read())
    else:
        print("No diary entries found.")

def generate_response(user_input):
    for keyword, response in personalized_library.items():
        if keyword.lower() in user_input.lower():
            return response
    return "I'm here to listen. Tell me more if you want."

def add_to_personalized_library(keyword, response):
    personalized_library[keyword.lower()] = response
    with open("personalized_library.json", "w") as file:
        json.dump(personalized_library, file)

def mental_health_bot():
    print("Mental Health Bot: Hi, I'm here to talk. Say something or type 'quit' to exit. 🤗")

    while True:
        user_input = speech_to_text().strip().lower()

        if user_input in ["quit", "exit", "bye"]:
            print("Mental Health Bot: Goodbye! Remember, it's okay to seek help. 🌈")
            print("Mental Health Bot: Take care! You're not alone. 👋")
            break

        # Teach bot custom responses
        if user_input.startswith("teach me") or user_input.startswith("add keyword"):
            parts = user_input.split(":", 1)
            if len(parts) == 2:
                keyword = parts[0].replace("teach me", "").replace("add keyword", "").strip()
                response = parts[1].strip()
                add_to_personalized_library(keyword, response)
                print(f"Mental Health Bot: I’ve learned a new response for '{keyword}'.")
            else:
                print("Invalid format. Use: teach me keyword: response")
            continue  # Skip diary logging

        # Save diary entry (if not a teaching command)
        if user_input:
            save_diary_entry(user_input)

        # Respond from library or general
        response = generate_response(user_input)
        print(f"Mental Health Bot: {response}")

        # Emotion keyword detection
        for emotion, strategy in coping_mechanisms.items():
            if emotion in user_input:
                print(f"Coping Tip: {strategy} {emotion_to_emoji.get(emotion, '')}")
                break

        # Ask to view diary
        view_diary_prompt = input("Would you like to view your diary entries? (yes/no): ").strip().lower()
        if view_diary_prompt == "yes":
            view_diary()

# Run the bot
mental_health_bot()
