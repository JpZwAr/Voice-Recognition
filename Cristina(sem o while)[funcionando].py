import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as s:
    r.adjust_for_ambient_noise(s)
    chat = open('chat.txt', 'w')
    chat.write(f"Orador:")
    audio = r.listen(s)
    speech =r.recognize_google(audio, language='pt')
    print(speech)
    chat = open('chat.txt', 'w')
    chat.write(f"Orador: {speech}")
