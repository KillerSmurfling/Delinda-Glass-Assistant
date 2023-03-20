                        elif "when were you born" in text:
                            speak(f"I was born in {memory.get('birthdate')}.")
                        elif "thank you" in text or "thanks" in text:
                            speak("You're welcome!")
                        elif "what time is it" in text:
                            speak(f"The time is {datetime.now().strftime('%I:%M %p')}.")
                        elif "stop" in text:
                            speak("Goodbye!")
                            break
                        else:
                            # Generate response using OpenAI API
                            response = ask_gpt(text)

                            # Speak response
                            speak(response)

                    except sr.UnknownValueError:
                        speak("Sorry, I couldn't understand you.")
                    except sr.RequestError as e:
                        speak("Sorry, I couldn't access the speech recognition service. Please try again later.")

        except sr.UnknownValueError:
            print("No speech detected.")
        except sr.RequestError as e:
            print("Speech recognition service error. Please try again later.")

if __name__ == "__main__":
    main()
