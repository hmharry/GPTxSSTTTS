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


environ['GOOGLE_APPLICATION_CREDENTIALS']= ""#Enter your own json file
openai.api_key=""#Enter you own API key


import google.cloud.texttospeech as tts
from google.cloud import translate
clientSTT=speech.SpeechClient()
import json

PATH_TO_FILE = 'text.wav'

r=sr.Recognizer()
model_engine = "text-davinci-003"#Change to your preferred GPT model

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
	#to speak the text (may be outdated)
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
#                print('test')
#                print(response_standard_wav)
                fstrgoogtran=response_standard_wav.results[0].alternatives[0].transcript
                fstrgoogconf=response_standard_wav.results[0].alternatives[0].confidence
#                print('Google English:',fstrgoogtran)
#                print('confidence:',fstrgoogconf)
                MyText.append(fstrgoogtran)
                confident.append(float(fstrgoogconf))
                lang.append('en')
			
#please make changes to the code if you want to achieve multi-language SST capability
#for example, ctrl c+ ctrl v and change the language code
#or if you like maybe change 'rb' into 'r'


                choice=max(confident)
#                    print('the languages are:',lang)
#                    print('the texts are:',MyText)
#                        
                for i in range(len(confident)):
                    if choice == confident[i]:
                        choice = i
                        break
                    else: continue
#                    print('the text with highest conf is:',MyText[choice])
                translate_client =translate_v2.Client()
#                print('f:',choice)
                query=MyText[choice]
#                print('The query is:',query)
                flang=lang[choice]
#                print('final langeuage is:',flang)



                #translation for keyword extraction (extension)
                transquery= translate_client.translate(query,target_language='en')['translatedText']
#                print(transquery)
                transquery=transquery.lower()
                        

                if query in exit_words:
                    print("ENDING CHAT")
                    break
                elif query=="":
                    continue
                else:
                    (res, usage) = GPT(query)
                             
                    print(res)
  #                  print('flang is', flang)
                    text_to_wav(flang,res)
                    print("="*20)
                    print("You have used %s tokens" % usage)
                    print("="*20)
        	MyText.clear()
        	confident.clear()
        	lang.clear()
#            else: continue
        except Exception as e:
             print(e)
       time.sleep(2)
       
