import speech_recognition as sr
import pyttsx3
import openai
import os
import pygame
import threading
import time
import keyboard
from datetime import datetime

# Set up OpenAI API credentials
openai.api_key = "api key goes here"

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

# Function for visual indicator
def visual_indicator(stop_event):
    # ... function body ...

    pygame.init()
    size = (300, 300)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Processing...")
    font = pygame.font.Font(None, 36)
    text = font.render("Shutup, I'm thinking...", True, (255, 255, 255))
    text_rect = text.get_rect(center=(size[0]/2, size[1]/2))

    while not stop_event.is_set():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill((0, 0, 0))
        screen.blit(text, text_rect)

        pygame.display.flip()
        time.sleep(0.1)

    pygame.quit()
# ... previous imports and definitions ...

# Main function to handle interactions
def main():
    print("Listening...")

    # Continuously listen for input until program is stopped
    while True:
        with sr.Microphone() as source:
            audio = r.listen(source)

        response = ""  # Initialize the response variable

        try:
            text = r.recognize_google(audio).lower()

            if text.startswith(WAKE_WORD):
                print("Starting conversation...")
                speak(f"Hello, I'm {ASSISTANT_NAME}. How can I help you?")
            elif "stop" in text:
                speak("Goodbye!")
                break
            # ... other elif conditions here ...

            else:
                # Create the stop_event for visual_indicator
                stop_event = threading.Event()

                # Start the visual indicator thread
                indicator_thread = threading.Thread(target=visual_indicator, args=(stop_event,))
                indicator_thread.start()

                # Generate response using OpenAI API
                response = ask_gpt(text)

                # Stop the visual indicator thread
                stop_event.set()
                indicator_thread.join()

                # Speak response
                speak(response)
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand you.")
        except sr.RequestError as e:
            speak("Sorry, I couldn't access the speech recognition service. Please try again later.")

if __name__ == "__main__":
    main()
