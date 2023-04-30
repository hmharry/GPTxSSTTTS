# GPTxSSTTTS
1.This program implements ChatGPT with Google STT API and TTS API

2.Please check your API key and paste it into the openai key section.

3.For Google API, check out the procedure of extracting a json file for credentials.

4.Please install the required libraries

5.Current program only consists of English STT. If you wish to use another languages, please check the language code and change it to the required language code.

6.For multi-language support, sorry to inform you that google does not support STT with multi-language input (maybe check out cloud Translate), copy the part for STT and change to your desired language, or simply change 'rb' to 'r' if you know what I mean.

7.There is a part of the code that uses translation to change the STT into English. This part is to convert the text detected into English and work out keyword extraction. 

8.Please comment it if you don't need that part of the code to avoid using the precious credits from Google Cloud. 

9.Change the GPT model if you wish
