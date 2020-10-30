# -*- coding: utf-8 -*-

import os
from os import listdir, path, startfile
import speech_recognition as sr

####################################################################################################################################

class Abrir:

	def __init__(self):
		self.raiz = ['C:/Users/Joãozinho/AppData/Roaming/Microsoft/Windows/Start Menu',
						'C:/ProgramData/Microsoft/Windows/Start Menu/Programs']
		self.dicio_programas = self.scandir(self.raiz)

	def fileext(self, nome):  # --------------------------------------> função que retorna uma string com a extensão do arquivo
		ext = ''
		try:
			for i in range(len(nome) - list(nome)[::-1].index('.') - 1, len(nome)):  # lê o nome do arquivo de trás
																					# pra frente até o primeiro ponto
				ext = ext + nome[i]
			return ext
		except ValueError:  # ----------------------------------> algumas raras exceções não possuem extensão
			return ''


	def scandir(self, root):
		pastas_negadas = []
		programas = {}
		dires = root.copy()
		diret = dires.pop()
		while True:
			while True:
				try:
					indice = listdir(diret)
					break
				except PermissionError:
					pastas_negadas.append(diret)
					diret = dires.pop()
			diret_qnt = 0
			for item in indice:
				if path.isdir(f'{diret}/{item}'):
					dires.insert(len(dires) - diret_qnt, f'{diret}/{item}')
					diret_qnt += 1
				else:
					if self.fileext(item) == '.lnk':
						programas.update({f'{item[:len(item) - 4]}'.lower(): diret})
			if not dires:
				return programas
			diret = dires.pop()

###################################################################################################################################

class Pesquisar:

	def __init__(self):
		self.site = 'www.google.com/search?q='
		self.item_pesquisa = ''
		
###################################################################################################################################

r = sr.Recognizer()
with sr.Microphone() as source:
	r.adjust_for_ambient_noise(source)
	start = input('Quando estiver pronto para falar, digite sim: ')
	chaves = ['abrir','fechar','mover','consultar','pesquisar']
	if(start == 'sim'):
		while True:
			print('Diga algo!')
			audio = r.listen(source)
			try:
				speech = r.recognize_google(audio, language='pt')
				speech = speech.lower()
				arquivo = open('chat.txt', 'a')
				s = 'Orador: '+speech+'\n'
				arquivo.write(s)
				arquivo.close()
			except sr.UnknownValueError:
				print('Google nao pode reconhecer o que foi dito')
			except sr.RequestError as e:
				print('Os servicos Google requisitados estao indisponiveis; {0}'.format(e))
			comando = speech.split()
			if comando[0] in chaves:
				if comando[0] == chaves[0]:

					indice = Abrir()

					fala = ' '.join(comando[1:len(comando)])
                    
					if indice.dicio_programas.get(fala):  # ----------------------------------------> verifica se o arquivo
																									# especificado tem
																									# correspondencia no dicionario
						startfile(f'{indice.dicio_programas.get(fala)}/{fala}.lnk')
                        
					else:
						parecidos = []
						for item in indice.dicio_programas.keys():   # -----------------------------> pesquisa cada palavra da
							                                                                        # fala do usuário
							for frag_fala in fala.split():                                          # nas chaves do dicionário
								if frag_fala in item:
									parecidos.append(item)  # ----------------------------> se houver potenciais correspondencias,
																						  # adiciona na lista 'parecidos'

						if len(parecidos) == 1:
							startfile(f'{indice.dicio_programas.get(parecidos[0])}/{parecidos[0]}.lnk')  # - se houver apenas uma
																										 # correspondência, a inicia

						elif len(parecidos) > 1:  # -------------------------------------> se houver mais de uma correspondência,
																						 # pede ajuda ao usuário
							print(f'{parecidos}\n')
							print('Não encontrei o item solicitado. Alguma das opções acima é o que você deseja? ')
							if input().lower() == 'sim':
								resp = int(input('Qual indice? '))
								startfile(f'{indice.dicio_programas.get(parecidos[resp])}/{parecidos[resp]}.lnk')
						else:
							print('Não encontrado.')
				if comando[0] == chaves[4]:
					
					pesquisa = Pesquisar()
					
					fala = ' '.join(comando[1:len(comando)])
					
					pesquisa.item_pesquisa = fala
					
					pesquisa.item_pesquisa.replace(' ','+')
					
					startfile(pesquisa.site + pesquisa.item_pesquisa)
