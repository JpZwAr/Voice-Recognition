import speech_recognition as sr
r = sr.Recognizer()
with sr.Microphone() as source:
	r.adjust_for_ambient_noise(source)
	while True:
		print('Diga algo!')
		audio = r.listen(source)
		try: 
			speech = r.recognize_google(audio, language='pt')
			print(speech)
			arquivo = open('chat.txt', 'a')
			s = 'Orador: {fala}\n'.format(fala = speech)
			arquivo.write(s)
			arquivo.close()
		except sr.UnknownValueError:
			print('Google nao pode reconhecer o que foi dito')
		except sr.RequestError as e:
			print('Os servicos Google requisitados estao indisponiveis; {0}'.format(e))		

