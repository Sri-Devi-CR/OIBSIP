"""
PROJECT 1 - OASIS INFOBYTE

VOICE ASSISTANT

Decription:
Create a basic voice assistant that can perform simple tasks based on voice commands.
Implement features like responding to "Hello" and providing predefined responses,
telling the time or date, and searching the web for information based on user queries.

Key Concepts and challenges:
1. Speech recognition
2. Task Automation
3. User Interaction
4. Error Handling
5. Customization
"""

import pyttsx3 as pyt #text to speech conversion library
import speech_recognition as sr #https://pypi.org/project/SpeechRecognition/
import webbrowser, wikipedia
import os, sys
import datetime

#set the engine to Pyttsx3 - used for text to speech in python
#sapi5 - Microsoft speech app platform interface used in this function

WEBSITES = ['youtube','google','wikipedia','instagram','gmail','linkedin','github','google classroom']

engine = pyt.init('sapi5')
voices = engine.getProperty('voices')  #list of voices from the selected engine
engine.setProperty('voice',voices[1].id) #0 - male and 1 - female voice

def speak(audioMessage):
    engine.say(audioMessage)
    engine.runAndWait()

def greetingsOfTheDay():
    speak("I am Maxni, your virtual assistant!")
    currentHour = int(datetime.datetime.now().hour)
    if (currentHour >= 0 and currentHour<12):
        speak("Maxni wishes you a Good Morning!")
    elif (currentHour>=12 and currentHour<18):
        speak("Maxni wishes you a Good Afternoon!")
    else:
        speak("Maxni wishes you a Good Evening!")

def userNameInput():
    speak("What is your name?")
    global uName
    uName = takeCommand()
    speak("Maxni welcomes")
    speak(uName)
    question = f"How can Maxni help you today, {uName}?"
    speak(question)

def takeCommand():
    rec = sr.Recognizer()
    with  sr.Microphone() as source:
        print("Maxni is listening...")
        #The pause_threshold parameter is used to determine the minimum length of silence (in seconds) that will be considered a pause in speech. If a pause longer than this threshold is detected, the speech recognition engine will stop listening for further speech.
        rec.pause_threshold = 3 #sec
        audio = rec.listen(source)

    try:
        print("Maxni is recognizing...")
        query = rec.recognize_google(audio,language='en-in')
        print(f"User said : {query}")

    except:
        print("Unable to Recognise User's voice")
        return "Guest"

    return query

print("Launching Maxni...")
greetingsOfTheDay()
userNameInput()

while True:
    queryGiven = takeCommand().lower()

    if 'wikipedia' in queryGiven:
        queryGiven = queryGiven.replace("wikipedia",'')
        speak(f"Maxni is searching Wikipedia for {queryGiven}...")
        res = wikipedia.summary(queryGiven, sentences=1)
        print(res)
        speak(f"According to Wikipedia  , {res}")

    elif 'website' in queryGiven:
        speak(f"Which website do you want Maxni to open?")
        queryGiven = takeCommand().lower()

        if queryGiven in WEBSITES:
            speak(f"Maxni is opening {queryGiven} for you...")
            webbrowser.open(f"{queryGiven}.com")

        else:
            speak("Sorry, Maxni doesn't have such websites in its database")

    elif 'the time' in queryGiven:
        time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {time}")

    elif 'search' in queryGiven:
        queryGiven = queryGiven.replace("search","")
        speak(f"Maxni is searching the web for the query...")
        webbrowser.open(queryGiven)

    elif 'open command prompt' in queryGiven:
        os.system("Start cmd")

    elif "who made you" in queryGiven or "who created you" in queryGiven: 
        speak("Maxni was developed by Sri Devi")

    elif 'hello' in queryGiven:
        speak(f"Hi {uName}!")

    elif 'stop listening' in queryGiven or 'stop' in queryGiven:
        speak("Maxni is halting it's operations now. Bye bye!")
        exit()
    
    else:
        speak(f"Sorry {uName}, Maxni finds the command too complex.. Please wait for the updates..")

'''
FURTHER IMPROVEMENTS:
Add more functionalities such as sending an email, setting reminders, 
providing weather updates, controlling smart home devices, answering gk questions,
and integrating with 3rd part api using NLP 
'''