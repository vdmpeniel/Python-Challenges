import datetime

import speech_recognition as sr
import pyttsx3
#import pyAudio
import keyboard
import pywhatkit
import datetime
import wikipedia
import pyjokes
from gtts import gTTS


engine = None
name = ''
tts_type = ''

def init_speech_engine():
    global engine
    engine = pyttsx3.init()
    engine.setProperty('voice', engine.getProperty('voices')[1].id)
    engine.setProperty('rate', 160)


def stop_speech_engine():
    global engine
    engine.stop()

def google_text_to_speech(message):
    print(f'Creating audio book from pdf.')
    tts = gTTS(text=message, lang='en')
    tts.save(f'downloads/{title}.mp3')
    print(f'Done.')

def python_text_to_speech(message):
    global engine
    engine.say(message)
    engine.runAndWait()

def talk(message):
    if tts_type == 'python':
        python_text_to_speech(message)
    else


def take_command():
    global name
    print('Listening...')
    listener = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            print(f'Utterance: {command}')

            if name.lower() in str(command).lower():
                # play sound
                command = command.replace(name, '')
                return command
            return ''
    except:
        return ''


def run_virtual_assistant():
    #command = take_command()

    command = 'tell me a joke'
    print(command)

    if command == '':
        message = 'I\'m sorry, is there anything I may help you with?'
        print(message)
        talk(message)

    elif 'play' in command:
        song = command.replace('play', '')

        talk(f'Now playing {song}')
        print(f'Now playing {song}...')

        pywhatkit.playonyt(song)
    elif command in (
        'what is the time',
        'tell me  the time',
        'what time is it'
    ):
        time = datetime.datetime.now().strftime('%I:%M %p')
        message = f'Current time is: {time}'
        print(message)
        talk(message)
    elif 'what is' in command or 'who is' in command:
        subject = command.replace('who is', '').replace('what is', '')
        info = wikipedia.summary(subject, 2)
        message = 'This is what I found in Wikipedia: ' + info
        print(message)
        talk(message)
    elif 'joke' in command:
        message = pyjokes.get_joke()
        print(message)
        talk(message)
    else:
        message = pyjokes.get_joke()
        print(message)
        talk(message)

def main():
    global name
    name = 'Alexa'

    init_speech_engine()
    # talk(f'I am {name}, your virtual assistant')
    talk('How can I help you?')

    run_virtual_assistant()
    stop_speech_engine()


if __name__ == '__main__':
    main()