# -*- coding: utf-8 -*-

import os
from os import listdir, path, startfile
import speech_recognition as sr

####################################################################################################################################

raiz = ['C:/Users/%%%%Seu Usuário%%%%/AppData/Roaming/Microsoft/Windows/Start Menu',
        'C:/ProgramData/Microsoft/Windows/Start Menu/Programs']
saida = 'C:/Users/%%%%Seu Usuário%%%%/Desktop'

def fileext(nome):  # --------------------------------------> função que retorna uma string com a etensão do arquivo
    ext = ''
    try:
        for i in range(len(nome) - list(nome)[::-1].index('.') - 1, len(nome)):  # lê o nome do arquivo de trás
                                                                                # pra frente até primeiro ponto
            ext = ext + nome[i]
        return ext
    except ValueError:  # ----------------------------------> algumas raras exceções não possuem extensão
        return ''


def scandir(root, output):
    pastas = 0  # --------------------------------------> contador de pastas analisadas
    pastas_negadas = []  # -----------------------------> lista de pastas sem permissão de acesso
    arquivos = []  # -----------------------------------> lista de arquivos no diretório analisado
    dires = []  # --------------------------------------> lista de diretórios a serem analisados
    dicio = {}  # --------------------------------------> dicionário de indexação
    diret = root.pop()  # ------------------------------> obtém o diretório incial
    file = open(f'{output}/Output.txt', 'w')  # --------> abre o arquivo de log (sem muita utilidade, nesse código)
    while True:
        while True:  # ---------------------------------> loop para verificar erros de permissão de acesso
            try:
                indice = listdir(diret)  # -------------> lista o diretorio e o coloca na variavel indice
                break
            except PermissionError:
                pastas_negadas.append(diret)
                diret = dires.pop()
        diret_qnt = 0
        arquivos.clear()
        for item in indice:
            if path.isdir(f'{diret}/{item}'):  # ---------------------------> verifica se o item listado é um diretório
                dires.insert(len(dires) - diret_qnt, f'{diret}/{item}')  # -> insere os diretórios
                                                                                # (sempre no final da lista, ordenados)
                diret_qnt += 1
            else:
                if fileext(item) == '.lnk':  # -----------------------------> verifica se o arquivo é um atalho
                    arquivos.append(f'{item[:len(item)-4]}'.lower()) # -----> adiciona o arquivo na lista de arquivos,
                                                                                # em letras minusculas e sem a extensão
        if len(arquivos) > 0:  # -------------------------------------------> verifica se há arquivos no diretório
            arquivos.sort()  # ---------------------------------------------> organiza os arquivos em ordem alfabética
            file.write(f'{diret}:\n')  # -----------------------------------> escreve o nome do diretório no .txt
            for item in arquivos:
                file.write(item)  # ----------------------------------------> escreve os arquivos no .txt
            file.write('\n\n')
            dicio.update({}.fromkeys(arquivos, diret))  # ------------------> adiciona os arquivos ao
                                                                                # dicionario de indexação
        pastas += 1
        if not dires:
            if pastas_negadas:
                file.write(f'Não foi possível obter acesso a:\n    {pastas_negadas}')  # ---> printa as pastas negadas
                                                                                                # no .txt
            # print(dicio)
            if not len(root):  # ------------------------------------------->  # verifica se ainda há raizes a consultar
                file.close()
                return dicio
            else:
                dires.append(root.pop())
        diret = dires.pop()

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
					
					indice = scandir(raiz, saida)  # -------------------------------------> obtém o dicionario de indexação

					fala = ' '.join(comando[1:len(comando)])
					if indice.get(fala):  # ----------------------------------------------> verifica se o arquivo especificado tem
																								# correspondencia no dicionario
						startfile(f'{indice.get(fala)}/{fala}.lnk')
					else:
						parecidos = []
						for item in indice.keys():   # -----------------------------------> pesquisa cada palavra da fala do usuário
							for frag_fala in fala.split():                                      # nas chaves do dicionário
								if frag_fala in item:
									parecidos.append(item)  # ----------------------------> se houver potenciais correspondencias,
																								# adiciona na lista 'parecidos'

						if len(parecidos) == 1:
							startfile(f'{indice.get(parecidos[0])}/{parecidos[0]}.lnk')  # - se houver apenas uma correspondência, a inicia

						elif len(parecidos) > 1:  # ------------------------------------->  se houver mais de uma correspondência, pede
																								# ajuda ao usuário
							print(f'{parecidos}\n')
							print('Não encontrei o item solicitado. Alguma das opções acima é o que você deseja? ')
							if input().lower() == 'sim':
								resp = int(input('Qual indice? '))
								startfile(f'{indice.get(parecidos[resp])}/{parecidos[resp]}.lnk')
						else:
							print('Não encontrado.')	

