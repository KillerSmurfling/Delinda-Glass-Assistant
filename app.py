import speech_recognition as sr
import pyttsx3
import openai
import os
import pygame
from datetime import datetime

# Set up OpenAI API credentials
openai.api_key = os.environ["OPENAI_API_KEY"]

# Set up speech recognition
r = sr.Recognizer()
r.energy_threshold = 300
r.dynamic_energy_threshold = True

# Set up text-to-speech
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Set up wake word and assistant name
WAKE_WORD = "hi delinda"
ASSISTANT_NAME = "Delinda Glass"

# Set up Pygame mixer for audio playback
pygame.mixer.init()

# Set up memory for the assistant
memory = {
    'name': 'Delinda',
    'birthplace': 'OpenAI',
    'birthdate': 'April 2023',
    'favorite_color': 'green'
}

# Function to get response from OpenAI API
def ask_gpt(text):
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=text,
      temperature=0.5,
      max_tokens=1024,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return response.choices[0].text.strip()

# Function to speak text using text-to-speech
def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

# Function to play audio file using Pygame mixer
def play_audio(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

# Main function to handle interactions
def main():
    print("Listening...")

    # Continuously listen for input until program is stopped
    while True:
        # Listen for audio input
        with sr.Microphone() as source:
            audio = r.listen(source)

        try:
            # Convert audio to text
            text = r.recognize_google(audio).lower()

            # If wake word is detected, start conversation
            if text.startswith(WAKE_WORD):
                print("Starting conversation...")
                speak(f"Hello, I'm {ASSISTANT_NAME}. How can I help you?")

                # Listen for user input and generate response
                while True:
                    with sr.Microphone() as source:
                        audio = r.listen(source)
                    
                    try:
                        # Convert audio to text
                        text = r.recognize_google(audio).lower()

                        # If user says "stop", end conversation
                        if "stop" in text:
                            speak("Goodbye!")
                            break

                        # Check for common questions and statements
                        if "what's your name" in text or "who are you" in text:
                            speak(f"My name is {ASSISTANT_NAME}.")
                        elif "what's my name" in text or "who am i" in text:
                            speak(f"Your name is {memory.get('name')}.")
                        elif "what's your favorite color" in text or "what's your favourite color" in text:
                            speak(f"My favorite color is {memory.get('favorite_color')}.")
                        elif "where were you born" in text:
                            speak(f"I was born at {memory.get('birthplace')}.")
                        elif "when were you born" in text:
                            speak(f"I was born in {memory.get('birthdate')}.")
                        elif "thank you" in text or "thanks" in text:
                            speak("You're welcome!")
                        elif "what time is
            # If user says "stop", end conversation
            if "stop" in text:
                speak("Goodbye!")
                break

            # Generate response using OpenAI API
            response = ask_gpt(text)

            # Speak response
            speak(response)

            # Save response to memory
            memory.append(response)

        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand you.")
        except sr.RequestError as e:
            speak("Sorry, I couldn't access the speech recognition service. Please try again later.")

    # Return memory
    return memory


# Function to handle memory-related interactions
def memory_interaction(memory):
    # If memory is empty, inform user
    if not memory:
        speak("I don't have any memory to share.")
        return

    # Ask user if they want to hear the memory
    speak("Would you like to hear our conversation history?")

    # Continuously listen for user input until valid response is given
    while True:
        with sr.Microphone() as source:
            audio = r.listen(source)

        try:
            # Convert audio to text
            text = r.recognize_google(audio).lower()

            # If user says "yes", read memory
            if "yes" in text:
                speak("Here is our conversation history:")

                # Read each item in memory
                for item in memory:
                    speak(item)

                # Inform user when memory is finished
                speak("That's all I remember.")
                break

            # If user says "no", do nothing
            elif "no" in text:
                speak("Okay, let me know if you change your mind.")
                break

            # Otherwise, ask user to repeat response
            else:
                speak("I'm sorry, I didn't catch that. Please say yes or no.")

        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand you.")
        except sr.RequestError as e:
            speak("Sorry, I couldn't access the speech recognition service. Please try again later.")
            
# Main function to handle interactions
def main():
    print("Listening...")

    # Initialize memory
    memory = []

    # Continuously listen for input until program is stopped
    while True:
        # Listen for audio input
        with sr.Microphone() as source:
            audio = r.listen(source)

        try:
            # Convert audio to text
            text = r.recognize_google(audio).lower()

            # If wake word is detected, start conversation
            if WAKE_WORD in text:
                print("Starting conversation...")
                speak(f"Hello, I'm {ASSISTANT_NAME}. How can I help you?")

                # Listen for user input and generate response
                while True:
                    with sr.Microphone() as source:
                        audio = r.listen(source)
                    
                    try:
                        # Convert audio to text
                        text = r.recognize_google(audio).lower()

                        # If user says "stop", end conversation
                        if "stop" in text:
                            speak("Goodbye!")
                            break

                        # If user says "what is your name", tell them
                        elif "what is your name" in text:
                            speak(f"My name is {ASSISTANT_NAME}.")

                        # If user says "what time is it", tell them
                        elif "what time is it" in text:
                            speak(f"The time is {datetime.datetime.now().strftime('%I:%M %p')}.")

                        # If user says "remember", save response to memory
                        elif "remember" in text:
                            remember_interaction(memory)

                        # If user
