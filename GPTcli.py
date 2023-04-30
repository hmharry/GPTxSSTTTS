#!/usr/bin/python
#coding=utf-8
import openai
import speech_recognition as sr
import pyttsx3
import time
#from deepgram import Deepgram
from os import environ
from google.cloud import texttospeech_v1
from playsound import playsound
import pygame
from google.cloud import speech
from googletrans import Translator
from google.cloud import translate_v2
import serial.tools.list_ports
import paho.mqtt.client as mqtt

# Don't forget to change the variables for the MQTT broker!
mqtt_topic = "esp32/wifirssi"
mqtt_broker_ip = "192.168.50.137"
checkgetloc=False
currentlocation=""
userdata=None

  

ports=serial.tools.list_ports.comports()
serialInst=serial.Serial()

    
client = mqtt.Client()    


# Once everything has been set up, we can (finally) connect to the broker
# 1883 is the listener port that the MQTT broker is using

serialInst.baudrate=115200
serialInst.port="/dev/ttyACM0"
serialInst.open()
#command=input("Serial Monitor: ")
#serialInst.write(command.encode('utf-8'))
environ['GOOGLE_APPLICATION_CREDENTIALS']= ""#Enter your own json file
openai.api_key=""#Enter you own API key


PROJECT_ID = 'cloudshell-28429'
assert PROJECT_ID
PARENT = f"projects/{PROJECT_ID}"
import google.cloud.texttospeech as tts
from google.cloud import translate
clientSTT=speech.SpeechClient()
import json

PATH_TO_FILE = 'text.wav'

r=sr.Recognizer()
model_engine = "text-davinci-003"

flang=""
def text_to_wav(voice_name, text):
       clientTTS = texttospeech_v1.TextToSpeechClient()
       synthesis_input = texttospeech_v1.SynthesisInput(text=text)
       
       voice = texttospeech_v1.VoiceSelectionParams(
              language_code=voice_name, ssml_gender=texttospeech_v1.SsmlVoiceGender.FEMALE
       )

       audio_config = texttospeech_v1.AudioConfig(
              audio_encoding=texttospeech_v1.AudioEncoding.MP3
       )
       response = clientTTS.synthesize_speech(
       input=synthesis_input, voice=voice, audio_config=audio_config
              )
       with open(r"output.mp3", "wb") as out:
       # Write the response to the output file.
              out.write(response.audio_content)
       pygame.mixer.init()
       pygame.mixer.music.load('output.mp3')
       pygame.mixer.music.play()
       while pygame.mixer.music.get_busy():
           continue


def SpeakText(command):
	
	engine = pyttsx3.init()
	engine.say(command)
	engine.runAndWait()

MyText=[]
MyTextA=""
confident=[]
lang=[]

def GPT(query):
       response = openai.Completion.create(
	      engine=model_engine,
	      prompt=query,
	      max_tokens=1024,
	      temperature=0.5,
       )
       return str.strip(response['choices'][0]['text']), response['usage']['total_tokens']
   
exit_words = ("q","Q","quit","QUIT","EXIT")
while True:

       def on_connect(client, userdata, flags, rc):
    # rc is the error code returned when connecting to the broker
           print("Connected!", str(rc))
    
    # Once the client has connected to the broker, subscribe to the topic
           client.subscribe(mqtt_topic)
       def on_message(client, userdata, msg):
    # This function is called everytime the topic is published to.
    # If you want to check each message, and do something depending on
    # the content, the code to do this should be run in this function
    
           print("Topic: ", msg.topic + "\nMessage: " + str(msg.payload))
           global currentlocation
           currentlocation=str(msg.payload.decode('utf-8'))
       client.on_connect = on_connect
       client.on_message = on_message
       with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2,duration=0.2)
            print('LISTENING..................................................................................')
            audio2=r.listen(source2)
            try:
                with open("text.wav", "wb") as f:
                    f.write(audio2.get_wav_data())
                MyText.clear()
                confident.clear()
                lang.clear()

                with open("text.wav","rb") as audwav:
                            
                    goog=audwav.read()
                            
                    audgoog=speech.RecognitionAudio(content=goog)
                            
                    config_wav = speech.RecognitionConfig(
								sample_rate_hertz=44100,
								enable_automatic_punctuation=True,
								language_code='en',
								audio_channel_count=1
							)
                            
                    response_standard_wav = clientSTT.recognize(
							    config=config_wav,
							    audio=audgoog
							)
                    print('test')
                    print(response_standard_wav)
                    fstrgoogtran=response_standard_wav.results[0].alternatives[0].transcript
                    fstrgoogconf=response_standard_wav.results[0].alternatives[0].confidence
                    print('Google English:',fstrgoogtran)
                    print('confidence:',fstrgoogconf)
                    MyText.append(fstrgoogtran)
                    confident.append(float(fstrgoogconf))
                    lang.append('en')
                    #Chinese
                with open("text.wav","rb") as audwav:
                    goog=audwav.read()
                    audgoog=speech.RecognitionAudio(content=goog)
                    config_wav = speech.RecognitionConfig(
	     			sample_rate_hertz=44100,
		 			enable_automatic_punctuation=True,
					language_code='zh',
					audio_channel_count=1
				)
                    response_standard_wav = clientSTT.recognize(
					config=config_wav,
					audio=audgoog
					)
                    print(response_standard_wav)
                    fstrgoogtran=response_standard_wav.results[0].alternatives[0].transcript
                    fstrgoogconf=response_standard_wav.results[0].alternatives[0].confidence
                    print('Google Chinese:',fstrgoogtran)
                    print('confidence:',fstrgoogconf)
                    MyText.append(fstrgoogtran)
                    confident.append(float(fstrgoogconf))
                    lang.append('zh')
                    #Korean
                with open("text.wav","rb") as audwav:
                    goog=audwav.read()
                    audgoog=speech.RecognitionAudio(content=goog)
                    config_wav = speech.RecognitionConfig(
				    sample_rate_hertz=44100,
					enable_automatic_punctuation=True,
					language_code='ko',
					audio_channel_count=1
					)
                    response_standard_wav = clientSTT.recognize(
					config=config_wav,
					audio=audgoog
					)
                    print(response_standard_wav)
                    fstrgoogtran=response_standard_wav.results[0].alternatives[0].transcript
                    fstrgoogconf=response_standard_wav.results[0].alternatives[0].confidence
                    print('Google Korean:',fstrgoogtran)
                    print('confidence:',fstrgoogconf)
                    MyText.append(fstrgoogtran)
                    confident.append(float(fstrgoogconf))
                    lang.append('ko')
                    #Japanese
                with open("text.wav","rb") as audwav:
                    goog=audwav.read()
                    audgoog=speech.RecognitionAudio(content=goog)
                    config_wav = speech.RecognitionConfig(
					sample_rate_hertz=44100,
					enable_automatic_punctuation=True,
					language_code='ja',
					audio_channel_count=1
					)
                    response_standard_wav = clientSTT.recognize(
					config=config_wav,
					audio=audgoog
					)
                    print(response_standard_wav)
                    fstrgoogtran=response_standard_wav.results[0].alternatives[0].transcript
                    fstrgoogconf=response_standard_wav.results[0].alternatives[0].confidence
                    print('Google Japanese:',fstrgoogtran)
                    print('confidence:',fstrgoogconf)
                    MyText.append(fstrgoogtran)
                    confident.append(float(fstrgoogconf))
                    lang.append('ja')
                    #Spanish
                with open("text.wav","rb") as audwav:
                    goog=audwav.read()
                    audgoog=speech.RecognitionAudio(content=goog)
                    config_wav = speech.RecognitionConfig(
            	        sample_rate_hertz=44100,
						enable_automatic_punctuation=True,
						language_code='es-ES',
						audio_channel_count=1
					)
                    response_standard_wav = clientSTT.recognize(
						config=config_wav,
						audio=audgoog
					)
                    print(response_standard_wav)
                    fstrgoogtran=response_standard_wav.results[0].alternatives[0].transcript
                    fstrgoogconf=response_standard_wav.results[0].alternatives[0].confidence
                    print('Google Spanish:',fstrgoogtran)
                    print('confidence:',fstrgoogconf)
                    MyText.append(fstrgoogtran)
                    confident.append(float(fstrgoogconf))
                    lang.append('es-ES')
                with open("text.wav","rb") as audwav:
                	    goog=audwav.read()
            	        audgoog=speech.RecognitionAudio(content=goog)
            	        config_wav = speech.RecognitionConfig(
						sample_rate_hertz=44100,
						enable_automatic_punctuation=True,
						language_code='de',
						audio_channel_count=1
					)
                    response_standard_wav = clientSTT.recognize(
						config=config_wav,
						audio=audgoog
					)
                    print(response_standard_wav)
                    fstrgoogtran=response_standard_wav.results[0].alternatives[0].transcript
                    fstrgoogconf=response_standard_wav.results[0].alternatives[0].confidence
                    print('Google German:',fstrgoogtran)
                    print('confidence:',fstrgoogconf)
                    MyText.append(fstrgoogtran)
                    confident.append(float(fstrgoogconf))
                    lang.append('de-DE')
                    #French
                with open("text.wav","rb") as audwav:
                    goog=audwav.read()
                    audgoog=speech.RecognitionAudio(content=goog)
                    config_wav = speech.RecognitionConfig(
						sample_rate_hertz=44100,
						enable_automatic_punctuation=True,
						language_code='fr',
						audio_channel_count=1
					)
                    response_standard_wav = clientSTT.recognize(
						config=config_wav,
						audio=audgoog
					)
                    print(response_standard_wav)
                    fstrgoogtran=response_standard_wav.results[0].alternatives[0].transcript
                    fstrgoogconf=response_standard_wav.results[0].alternatives[0].confidence
                    print('Google French:',fstrgoogtran)
                    print('confidence:',fstrgoogconf)
                    MyText.append(fstrgoogtran)
                    confident.append(float(fstrgoogconf))
                    lang.append('fr')
                          

					#Google STT for cantonese
                with open("text.wav","rb") as audwav:
                    goog=audwav.read()
                    audgoog=speech.RecognitionAudio(content=goog)
                    config_wav = speech.RecognitionConfig(
	        	        sample_rate_hertz=44100,
                        enable_automatic_punctuation=True,
                        language_code='yue-HK',
                        audio_channel_count=1
                  	)
                    response_standard_wav = clientSTT.recognize(
                       	config=config_wav,
                       	audio=audgoog
					)
                    print(response_standard_wav)
                    fstrgoogtran=response_standard_wav.results[0].alternatives[0].transcript
                    fstrgoogconf=response_standard_wav.results[0].alternatives[0].confidence
                    print('Google:',fstrgoogtran)
                    print('confidence:',fstrgoogconf)
                    MyText.append(fstrgoogtran)
                    confident.append(float(fstrgoogconf))
                    lang.append("yue-HK")
                    print(confident)
                    choice=max(confident)
                    print(choice)
                    print('the languages are:',lang)
                    print('the texts are:',MyText)
                        
                    for i in range(len(confident)):
                        if choice == confident[i]:
                                choice = i
                                break
                        else: continue
                    print('the text with highest conf is:',MyText[choice])
                    translate_client =translate_v2.Client()
                    print('f:',choice)
                    query=MyText[choice]
                    print('The query is:',query)
                    flang=lang[choice]
                    print('final langeuage is:',flang)
                    #translation for keyword extraction
                    transquery= translate_client.translate(query,target_language='en')['translatedText']
                    print(transquery)
                    transquery=transquery.lower()
                        

                    if query in exit_words:
                        print("ENDING CHAT")
                        break
                    elif query=="":
                        continue
                    else:
                        (res, usage) = GPT(query)
                              
                        print(res)
                        print('flang is', flang)
                        text_to_wav(flang,res)
                        print("="*20)
                        print("You have used %s tokens" % usage)
                        print("="*20)
        		MyText.clear()
        		confident.clear()
        		lang.clear()
#               else: continue
        	except Exception as e:
                 print(e)
       time.sleep(2)
       
