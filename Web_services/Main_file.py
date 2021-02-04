import ctypes
import datetime
import email
import imaplib
import json
import os
import random
import shutil
import smtplib
import pyaudio
import subprocess
import wave
import webbrowser
from urllib.request import urlopen
import pyjokes
import pyttsx3
import requests
import speech_recognition as sr
import wikipedia
import winshell
import wolframalpha
from clint.textui import progress
from ecapture import ecapture as ec
from playsound import playsound
from twilio.rest import Client
import time

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning Sir !")

    elif 12 <= hour < 18:
        speak("Good Afternoon Sir !")

    else:
        speak("Good Evening Sir !")

    assname = "Jarvis"
    speak("I am your Assistant")
    speak(assname)


def usrname():
    speak("What should i call you sir")
    uname = takeCommand()
    speak("Welcome Mister")
    speak(uname)
    columns = shutil.get_terminal_size().columns

    print("#####################".center(columns))
    print("Welcome Mr.", uname.center(columns))
    print("#####################".center(columns))

    speak("How can i Help you")


def takeCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")
        r.pause_threshold = 1

        audio = r.listen(source)

    try:
        print("Recognizing...")
        voice_command = r.recognize_google(audio, language='en-in')
        print(f"User said: {voice_command}\n")

    except Exception as e:
        print(e)
        print("Unable to Recognizing your voice.")
        return "None"

    return voice_command


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()

    # Enable low security in gmail
    server.login('170320107063.ce.shubham@gmail.com', 'JAYambe@1401$')
    server.sendmail('170320107063.ce.shubham@gmail.com', to, content)
    server.close()


def read_email_from_gmail():
    Email = input("Email =")
    FROM_EMAIL = Email
    FROM_PWD = input("Password =")
    SMTP_SERVER = "imap.gmail.com"
    SMTP_PORT = 993

    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER, SMTP_PORT)
        mail.login(FROM_EMAIL, FROM_PWD)
        mail.select('inbox')

        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]

        id_list = mail_ids.split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in range(latest_email_id, first_email_id, -1):
            typ, data = mail.fetch(i, '(RFC822)')

            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    email_subject = msg['subject']
                    email_from = msg['from']
                    print('From : ' + email_from + '\n')
                    print('Subject : ' + email_subject + '\n')

    except Exception as e:
        print(e)


def start_song(song_name):
    words = song_name.split()

    url = "http://www.youtube.com/results?search_query="

    for word in words:
        url = url + word + "+"
    time.sleep(1)  # Sleeps for a second
    webbrowser.open_new(url)


if __name__ == '__main__':
    clear = lambda: os.system('cls')

    # This Function will clean any
    # command before execution of this python file
    clear()
    wishMe()
    usrname()

    while True:

        voice_command = takeCommand().lower()

        # All the commands said by user will be
        # stored here in 'voice_command' and will be
        # converted to lower case for easily
        # recognition of command
        if 'wikipedia' in voice_command:
            speak('Searching Wikipedia...')
            voice_command = voice_command.replace("wikipedia", "")
            results = wikipedia.summary(voice_command, sentences=5)
            speak("According to Wikipedia")
            engine.setProperty('rate', 130)
            print(results)
            speak(results)


        elif 'on youtube' in voice_command:
            song_name = voice_command.replace("on youtube", "")
            speak("Here you go to Youtube\n")
            start_song(song_name)
            time.sleep(5)

        elif 'record my voice' in voice_command:
            print('for how many second do you record')
            speak("for how many second do you record")
            seconds = takeCommand()
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 2
            RATE = 44100
            RECORD_SECONDS = int(seconds)
            WAVE_OUTPUT_FILENAME = "../Voice_assistant/output.wav"

            p = pyaudio.PyAudio()

            stream = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)

            print("* recording")

            frames = []

            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)

            print("* done recording")

            stream.stop_stream()
            stream.close()
            p.terminate()

            wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

        elif "voice recording" in voice_command:
            print("which file do you want to open")
            speak("which file do you want to open")
            file_recording = takeCommand()
            playsound(file_recording + '.wav')

        elif 'open google' in voice_command:
            speak("Here you go to Google\n")
            webbrowser.open("google.com")
            time.sleep(5)

        elif 'open stackoverflow' in voice_command:
            speak("Here you go to Stack Over flow.Happy coding")
            webbrowser.open("stackoverflow.com")
            time.sleep(5)

        elif 'play music' in voice_command or "play song" in voice_command:

            speak("Here you go with music")
            # music_dir = "G:\\Song"
            music_dir = "E:\\Shubham\\Music\\Khelaiya all parts"
            files = os.listdir(music_dir)
            d = random.choice(files)
            os.startfile(music_dir + "\\" + d)

        elif 'the time' in voice_command or ' what is time' in voice_command:
            times = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"Sir, the time is {times}")
            speak(f"Sir, the time is {times}")

        elif 'email to Shubham' in voice_command:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "Receiver email address"
                sendEmail(to, content)
                speak("Email has been sent !")
            except Exception as e:
                print(e)
                speak("I am not able to send this email")

        elif 'send a mail' in voice_command:
            try:
                agree="no"
                while agree!="yes":
                    speak("What should I say?")
                    content = takeCommand()
                    speak("whome should i send")
                    to = input()
                    print("please check the Email-id and content before sending")
                    speak("please check the number and message before sending")
                    print("number = ", number, "\nmessage = ", message)
                    print("type yes for send email and no for change the content or email-id")
                    ans = input()
                    if ans == "yes":
                        agree = "yes"
                        sendEmail(to, content)
                        print("Email has been sent Successfully !")
                        speak("Email has been sent Successfully !")
            except Exception as e:
                print(e)
                speak("I am not able to send this email")

        elif 'read my emails' in voice_command or 'read emails' in voice_command or 'read my mail' in voice_command or 'read my email' in voice_command:
            read_email_from_gmail()

        elif 'how are you' in voice_command:
            speak("I am fine, Thank you")
            speak("How are you,Sir")

        elif 'fine' in voice_command or "good" in voice_command:
            speak("It's good to know that your fine")

        elif "change my name to" in voice_command:
            voice_command = voice_command.replace("change my name to", "")
            assname = voice_command

        elif "change name" in voice_command:
            speak("What would you like to call me, Sir ")
            assname = takeCommand()
            speak("Thanks for naming me")

        elif "what's your name" in voice_command or "What is your name" in voice_command:
            speak("My friends call me Jarvis")
            speak("")
            print("My friends call me", assname)

        elif 'exit' in voice_command:
            speak("Thanks for giving me your time")
            exit()

        elif "who made you" in voice_command or "who created you" in voice_command:
            speak("I have been created by Shubham.")

        elif 'joke' in voice_command:
            speak(pyjokes.get_joke())

        elif "calculate" in voice_command:

            app_id = "GYVQYU-PE3LYY3QAR"
            client = wolframalpha.Client(app_id)
            indx = voice_command.lower().split().index('calculate')
            voice_command = voice_command.split()[indx + 1:]
            res = client.query(''.join(voice_command))
            answer = next(res.results).text
            print("The answer is " + answer)
            speak("The answer is " + answer)

        elif 'search' in voice_command or 'play' in voice_command:

            voice_command = voice_command.replace("search", "")
            voice_command = voice_command.replace("play", "")
            webbrowser.open(voice_command)

        elif "who i am" in voice_command:
            speak("If you talk then definately your human.")

        elif "why you came to world" in voice_command:
            speak("Thanks to Shubham. further It's a secret")

        elif 'is love' in voice_command:
            speak("It is 7th sense that destroy all other senses")

        elif "who are you" in voice_command:
            speak("I am your virtual assistant created by Shubham")

        elif 'reason for you' in voice_command:
            speak("I was created as a Minor project by Mister Shubham ")

        elif 'change background' in voice_command:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, "Location of wallpaper", 0)
            speak("Background changed succesfully")

        elif 'news' in voice_command:

            try:
                news_api = "https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=6756d45ea89946959bb25b8c31af689a"
                jsonObj = urlopen(news_api)
                data = json.load(jsonObj)
                i = 1

                speak('here are some top news from the times of india')
                print('''=============== TIMES OF INDIA ============''' + '\n')
                for item in data['articles']:
                    print(str(i) + '. ' + item['title'] + '\n')

                    print(item['description'] + '\n')
                    speak(str(i) + '. ' + item['title'] + '\n')
                    i += 1
            except Exception as e:

                print(str(e))

        elif "turn on Wi-Fi" in voice_command:
            os.system("netsh interface show interface")

        elif 'lock window' in voice_command:
            speak("locking the device")
            ctypes.windll.user32.LockWorkStation()

        elif 'open desktop' in voice_command:
            speak("Here to go desktop")
            os.startfile(os.path.join(winshell.desktop()))

        elif 'shutdown system' in voice_command:
            print("Are you really shutdown your system , Speak yes for shutdown and no for deny")
            speak("Are you really shutdown your system , Speak yes for shutdown and no for deny")
            review = takeCommand()
            if review == 'no':
                pass;
            else:
                os.system("shutdown /s /t 1")

        elif 'empty recycle bin' in voice_command:
            winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
            speak("Recycle Bin Recycled")

        elif "don't listen" in voice_command or "stop listening" in voice_command:
            speak("for how much time you want to stop jarvis from listening commands")
            a = int(takeCommand())
            time.sleep(a)
            print(a)

        elif "where is" in voice_command:
            voice_command = voice_command.replace("where is", "")
            location = voice_command
            speak("User asked to Locate")
            speak(location)
            webbrowser.open("https://www.google.nl/maps/place/" + location + "")

        # elif "camera" in voice_command or "take a photo" in voice_command:
        #     c = random.randint(1, 100000)
        #     ec.capture(0, "Jarvis Camera ", "img.jpg")

        elif "restart" in voice_command:
            subprocess.call(["shutdown", "/r"])

        elif "hibernate" in voice_command or "sleep" in voice_command:
            speak("Hibernating")
            subprocess.call("shutdown / h")

        elif "log off" in voice_command or "sign out" in voice_command:
            speak("Make sure all the application are closed before sign-out")
            time.sleep(5)
            subprocess.call(["shutdown", "/l"])

        elif "write a note" in voice_command:
            speak("What should i write, sir")
            note = takeCommand()
            file = open('../Voice_assistant/jarvis.txt', 'w')
            speak("Sir, Should i include date and time")
            snfm = takeCommand()
            if 'yes' in snfm or 'sure' in snfm:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                file.write(strTime)
                file.write(" :- ")
                file.write(note)
            else:
                file.write(note)

        elif "show note" in voice_command:
            speak("Showing Notes")
            file = open("../Voice_assistant/jarvis.txt", "r")
            print(file.read())
            speak(file.read(6))

        elif "update assistant" in voice_command:
            speak("After downloading file please replace this file with the downloaded one")
            url = '# url after uploading file'
            r = requests.get(url, stream=True)

            with open("Voice.py", "wb") as Pypdf:

                total_length = int(r.headers.get('content-length'))

                for ch in progress.bar(r.iter_content(chunk_size=2391975),
                                       expected_size=(total_length / 1024) + 1):
                    if ch:
                        Pypdf.write(ch)

                # NPPR9-FWDCX-D2C8J-H872K-2YT43
        elif "jarvis" in voice_command:

            wishMe()
            speak("Jarvis 1 point o in your service Mister")
            speak(assname)

        elif "weather" in voice_command:

            # Google Open weather website
            # to get API of Open weather
            api_key = "Api key"
            base_url = "http://api.openweathermap.org / data / 2.5 / weather?"
            speak(" City name ")
            print("City name : ")
            city_name = takeCommand()
            complete_url = base_url + "appid =" + api_key + "&q =" + city_name
            response = requests.get(complete_url)
            x = response.json()

            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_pressure = y["pressure"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                print(" Temperature (in kelvin unit) = " + str(
                    current_temperature) + "\n atmospheric pressure (in hPa unit) =" + str(
                    current_pressure) + "\n humidity (in percentage) = " + str(
                    current_humidiy) + "\n description = " + str(weather_description))

            else:
                speak(" City Not Found ")

        elif "send message" in voice_command:
            # You need to create an account on Twilio to use this service
            account_sid = 'ACdd3bdd83233031fbc916aada97e36bed'
            auth_token = '099f1a4aff53761e6b6666710ba17849'
            client = Client(account_sid, auth_token)
            agree = "no"
            while (agree != "yes"):
                print('send message to which number write down')
                speak("send message number")
                number = takeCommand()
                print("What should I say?")
                speak("What should I say?")
                message = takeCommand()
                print("please check the number and message before sending")
                speak("please check the number and message before sending")
                print("number = ", number, "\nmessage = ", message)
                print("type yes for send message and no for change the message or number")
                ans = input()
                if ans == "yes":
                    agree = "yes"
                    message = client.messages \
                        .create(
                        body=message,
                        from_='+18636560854',
                        to='+91' + number
                    )

                print("Your mesaage has been sent")
                speak("Your mesaage has been sent")
            else:
                agree == "no"


        elif "best friend" in voice_command:
            engine.setProperty('rate', 130)
            speak("ohh you asked me about your best friend  let me  guess  ")
            speak(" Amm  , oh ,  Yes  you  tell  me ,  Chahna is  your best friend .  You also called  her  Fulvdi")
            speak("hai Diku ,  I  want  to tell you something  secret , which is  Shubham  never told  you  so hear "
                  "me  properly ")
            speak("You  are more than a his life . You’re his  best friend , his partner-in-crime, his  other half . "
                  "You know him  better than he  know hisself. You know what he likes , what he love, what he hate. You "
                  "applaud his passions and tolerate his faults. You’re there for him, always. And it’s not always "
                  "about what we say, or what we do – because you, by yourself, is enough. You, with your smile, "
                  "your laugh, your friendship – it’s more than he deserve. You’ve laughed, you’ve cried, and you’re "
                  "stronger than ever. Because he is  nothing   without you. You’re part of his  , his life, "
                  "his  family, his entire world. Love you to best friend forever")

        elif "Good Morning" in voice_command:
            speak("A warm" + voice_command)
            speak("How are you Mister")
            speak(assname)

        # most asked question from google Assistant
        elif "will you be my gf" in voice_command or "will you be my bf" in voice_command:
            speak("I'm not sure about, may be you should give me some time")

        elif "how are you" in voice_command:
            speak("I'm fine, glad you me that")

        elif "i love you" in voice_command:
            speak("It's hard to understand")

        elif "what is" in voice_command or "who is" in voice_command:

            # Use the same API key
            # that we have generated earlier
            client = wolframalpha.Client("GYVQYU-PE3LYY3QAR")
            res = client.query(voice_command)

            try:
                print(next(res.results).text)
                speak(next(res.results).text)
            except StopIteration:
                results1 = wikipedia.summary(voice_command, sentences=5)
                print(results1)
                speak(results1)
            # elif "" in voice_command:
        # Command go here
        # For adding more commands
