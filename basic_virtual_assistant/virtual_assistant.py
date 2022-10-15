import datetime
import time

import speech_recognition as sr
import pyttsx3
#import pyAudio
import keyboard
import pywhatkit
import datetime
import wikipedia
import pyjokes
from gtts import gTTS
from pygame import mixer
from io import BytesIO


engine = None
name = ''
tts_type = ''


def play_sound(sound):
    mixer.init()
    sound.seek(0)
    mixer.music.load(sound, 'mp3')
    mixer.music.play()
    while mixer.music.get_busy():  # do while music to finish playing
        print('Talking...', end='\r')
    time.sleep(0.001)
    mixer.stop()


def google_text_to_speech(message):
    print(f'Google\'s TTS talking...')
    tts = gTTS(text=message, lang='en')
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    play_sound(mp3_fp)
    time.sleep(0.01)


def init_speech_engine():
    global engine
    engine = pyttsx3.init()
    engine.setProperty('voice', engine.getProperty('voices')[1].id)
    engine.setProperty('rate', 160)


def stop_speech_engine():
    global engine
    engine.stop()


def python_text_to_speech(message):
    global engine
    init_speech_engine()
    print(f'Python\'s TTS talking...')
    engine.say(message)
    engine.runAndWait()
    stop_speech_engine()


def talk(message):
    if tts_type == 'python':
        python_text_to_speech(message)
    else:
        google_text_to_speech(message)


def take_command():
    global name
    print('Listening...')
    listener = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            voice = listener.listen(source)
            command = listener.recognize_google(voice)

            command = command.lower()
            if name.lower() in command:
                # play sound
                command = command.replace(name, '')
                return command
            return '...'
    except:
        return '...'


def contains_any(term, iterable):
    for element in iterable:
        if element in term:
            return True
    return False


def remove_all(term, iterable):
    for item in iterable:
        term.replace(term, '')
    return term


def run_virtual_assistant():
    global name
    talk(f'I am {name}, your virtual assistant')
    talk('How can I help you?')

    command = ''
    is_halt = False
    while not is_halt:
        command = take_command()

        print(f'- User: {command}')
        message = ''
        if command == 'exit' or keyboard.KEY_DOWN:
            message = 'Good bye!'
            is_halt = True

        elif command == '...':
            continue

        elif command == '':
            message = "I'm sorry, is there anything I may help you with?"

        elif 'play' in command:
            song = command.replace('play', '')
            pywhatkit.playonyt(song)
            message = f'Now playing {song}'

        elif command in {
            'what is the time',
            'tell me the time',
            'what time is it'
        }:
            time = datetime.datetime.now().strftime('%I:%M %p')
            message = f'Current time is: {time}'

        elif contains_any(command, {"what's", 'what is', "who's", 'who is', 'what was', 'who was', 'who were'}):
            subject = remove_all(command, {"what's", 'what is', "who's", 'who is', 'what was', 'who was', 'who were'})
            try:
                info = wikipedia.summary(subject, 2)
                message = 'This is what I found in Wikipedia: ' + info
            except:
                message = "I'm sorry, I couldn't find any results on that subject"

        elif 'joke' in command:
            message = pyjokes.get_joke()

        else:
            message = "I didn't get that, sorry. Come again"

        print(f'- Assistant: {message} \n')
        talk(message)


def main():
    global name, tts_type
    name = 'Alexa'
    tts_type = 'google'
    run_virtual_assistant()


if __name__ == '__main__':
    main()
