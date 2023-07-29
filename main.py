#!/usr/bin/env python3

import speech_recognition as sr
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
# from chatterbot.trainers import ChatterBotCorpusTrainer
import pyttsx3


print('modules imported')


r = sr.Recognizer()
r.pause_threshold = 1
print('initialized speech recognizer')

bot = ChatBot('digital_assistance')
print('initialized chatbot')
print('preparing data for training the bot...')
with open('database/qna.txt') as txt:
    qna = txt.readlines()
qna = filter(bool, qna)
qna = list(map(lambda x: x[3:], qna))
print('done')
trainer = ListTrainer(bot)
print('initialized bot trainer, started training...')
trainer.train(qna)
print('done')

engine = pyttsx3.init()
print('initialized text to speech object')

rate = engine.getProperty("rate")

engine.setProperty("rate", 150)

voices = engine.getProperty("voices")

# print("Male voice :{0}".format(voices[0].id))
# print("Female voice :{0}".format(voices[1].id))

engine.setProperty("voice", voices[1].id)



while True:
    with sr.Microphone() as source:
        print('\nListening...')
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language='en-in')
    except sr.UnknownValueError:
        print('Sorry for the confusion',' Could you please express yourself in a different way or provide more clarity, '
              'so that I can understand it better?', end='\n\n')
        continue
    except sr.RequestError as e:
        print('Please check your internet connection or try again later.', end='\n\n')
        continue
    except Exception as e:
        print(f'An error occurred during speech recognition: {e}', end='\n\n')
        raise

    print(f'INPUT: "{text}"')
    response = bot.get_response(text)

    rate = engine.getProperty("rate")

    engine.setProperty("rate",150)

    voices = engine.getProperty("voices")

   # print("Male voice :{0}".format(voices[0].id))
   # print("Female voice :{0}".format(voices[1].id))

    engine.setProperty("voice",voices[1].id)



    print(f'OUTPUT: "{response}"')
    engine.say(response)
    engine.runAndWait()
