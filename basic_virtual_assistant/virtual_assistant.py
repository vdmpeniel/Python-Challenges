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


def play_sound(sound, volume=0.5):
    try:
        mixer.init()
        mixer.music.set_volume(volume)
        if isinstance(sound, str):
            mixer.music.load(f'./basic_virtual_assistant/sounds/{sound}')
        else:
            sound.seek(0)
            mixer.music.load(sound, 'mp3')

        mixer.music.play()
        while mixer.music.get_busy():  # do while music to finish playing
            print('Talking...', end='\r')

        print(' ', end='\r')
        time.sleep(0.001)
        mixer.stop()

    except Exception as e:
        print(f'An exception of type: {type(e)} occurred. Arguments: {e.args}')


def google_text_to_speech(message):
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
    engine.say(message)
    engine.runAndWait()
    stop_speech_engine()


def talk(message):
    if tts_type == 'python':
        python_text_to_speech(message)
    else:
        google_text_to_speech(message)


def calibrate_recognizer():
    try:
        recognizer = sr.Recognizer()
        # with sr.Microphone() as source:
        #     print('\nCalibrating...')
        #     recognizer.adjust_for_ambient_noise(source)
        #     time.sleep(0.1)
        #     print('Done.\n')
        return recognizer
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")

    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return None


def listen_to_voice_command():
    global name
    # time.sleep(0.01)
    recognizer = sr.Recognizer()
    error_message = ''
    try:
        with sr.Microphone() as source:
            print('\nListening...')
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            command = command.lower()

            if name.lower() in command:
                play_sound('chime.mp3')
                command = command.replace(name.lower(), '').rstrip(' ').lstrip(' ')
                return command
            print(f'- Name was not present in the heard utterance: {command}')
            return '...'

    except sr.UnknownValueError:
        error_message = ' (Error: Google Speech Recognition could not understand audio)'

    except sr.RequestError as e:
        error_message = f' (Error: Could not request results from Google Speech Recognition service; {e})'

    except Exception as e:
        error_message = f' (Error: Exception of type {e} occurred)'

    return 'Silence' + error_message


def contains_any(term, iterable):
    for element in iterable:
        if element in term:
            return True
    return False


def remove_all(term, iterable):
    for item in iterable:
        term.replace(term, '')
    return term


question_starts = {
    "what's",
    'what is',
    "who's",
    'who is',
    'what was',
    'who was',
    'who were',
    'when is',
    'when was'
}


def say(message):
    print(f'- Assistant: {message}')
    talk(message)


def run_virtual_assistant():
    global name
    # recognizer = calibrate_recognizer()

    say(f'I am {name}, your virtual assistant')
    say('How can I help you?')

    command = ''
    while True:
        command = listen_to_voice_command()
        message = ''
        print(f'- User: {command}')

        if command == 'exit' or keyboard.is_pressed(' '):
            break

        elif contains_any(command, {'...', 'Silence (Error:'}):
            continue

        elif command == '':
            message = "I'm sorry, is there anything I may help you with?"

        elif contains_any(command, {'hi', 'hello', 'howdy'}):
            message = 'Hi. It is my pleasure to help you'

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

        elif contains_any(command, question_starts):
            subject = remove_all(command, question_starts)
            try:
                info = wikipedia.summary(subject, 1)
                message = 'This is what I found in Wikipedia: ' + info
            except:
                message = "I'm sorry, I couldn't find any results on that subject"

        elif 'joke' in command:
            message = pyjokes.get_joke()

        else:
            message = "I didn't get that, sorry. Come again"
        say(message)

    say('Good bye!')


def main():
    global name, tts_type
    name = 'alexa'
    tts_type = 'google'
    run_virtual_assistant()


if __name__ == '__main__':
    main()
