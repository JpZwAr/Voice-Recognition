from os import listdir, startfile, walk
import pyautogui as pa
import shutil
import time
import speech_recognition as sr

# definição dos diretórios a serem indexados
raizes = ['C:/Users/Victor Mateus/AppData/Roaming/Microsoft/Windows/Start Menu',
          'C:/ProgramData/Microsoft/Windows/Start Menu/Programs',
          'C:/Users/Public/Desktop',
          'C:/Users/Victor Mateus/Music',
          'D:/Filmes',
          'D:/The Office',
          'D:/Pac Baja',
          'D:/Softwares/Arquivos de Programas/Among Us']


# quando chamada, retorna uma lista contendo as palavras ditas pelo usuário
def ouvir():
    # cria uma instância da classe usada para reconhecer a fala
    r = sr.Recognizer()
    # cria uma instância do dispositivo de entrada
    with sr.Microphone() as source:
        # faz o cancelamento de ruído
        r.adjust_for_ambient_noise(source)
        print('Diga algo!')
        # faz o reconhecimento da fala
        audio = r.listen(source)
        try:
            speech = r.recognize_google(audio, language='pt').lower().split()
        # tratamento de possíveis erros
        except sr.UnknownValueError:
            print('Google nao pode reconhecer o que foi dito')
        except sr.RequestError as e:
            print(f'Os servicos Google requisitados estao indisponiveis; {e}')
    return speech


# retorna a extensão do arquivo
def fileext(nome):
    ext = ''
    try:
        # a partir de técnicas de slicing dde strings, encontra o último ponto do nome e retorna a extensão
        for i in range(len(nome) - list(nome)[::-1].index('.') - 1, len(nome)):
            ext = ext + nome[i]
        return ext
    # para os raros casos de arquivos do sistema sem extensão
    except ValueError:
        return ''


# função usada para encontrar a origem e o destino de arquivos a serem movidos
def pesquisador():
    u = 'C:/'
    # mostra uma lista dos diretórios contidos na raiz
    print(listdir("C:/"))
    for s in range(1000):
        a = str(input('Chegamos?(sim/não) '))
        if a == 'sim':
            b = str(input('Digite o nome do arquivo: '))
            # recebe o nome do arquivo a ser movido pelo usuário
            u = u + b + '/'
            break
        elif a != 'sim' and a != 'não':
            print('Não entendi')
            break
        else:
            # pergunta ao usuário o diretório de destino
            z = str(input('Pra onde chefe? '))
            u = u + z + '/'
            print(u)
            print(listdir(u))
    return u


# retorna um dicionário cujas chaves são os nomes dos arquivos, e os valores são as extensões e diretórios dos arquivos
def scandir(root):
    # declara o dicionário
    dicio = {}
    # dígito de identificação usada para distinguir arquivos com o mesmo nome, mas com extensões diferentes
    ide = 0
    igual = ''
    for uni in root:
        for raiz, dires, files in walk(uni):
            # analisa os arquivos presentes na árvore de diretórios presente nas raízes informadas
            if files:
                # separa os arquivos presentes nos diretórios em tuplas do formato (nome do arquivo, extensão)
                edited = [(item.replace(fileext(item), ''), fileext(item)) for item in files]
                # insere o dígito de identificação para arquivos com o mesmo nome como chave do dicionário, cujos
                # valores são sua extensão e seu diretório
                # (ATENÇÃO: todos os valores contém, portanto, ao menos um dígito '0' ao final do nome)
                for file, ext in edited:
                    if file == igual:
                        ide += 1
                    else:
                        ide = 0
                    dicio.update({f'{file}{ide}'.lower(): (ext, raiz)})
                    igual = file
    return dicio


retorno = scandir(raizes)


while True:
    comando = ouvir()
    # comando para abrir programas e arquivos
    if comando[0] == 'abrir':
        # insira na lista os tipos dos aquivos que se deseja abrir
        exts = ['.lnk', '.exe']
        # retira a palavra 'abrir' do comando
        comando.pop(0)
        # une a lista com as palavras do comando em uma string
        comando = ' '.join(comando)
        # obtém a tupla contendo a extensão e o diretório do arquivo solicitado
        valor = retorno.get(f'{comando}0')
        if valor:
            if valor[0] in exts:
                startfile(f'{valor[1]}/{comando}{valor[0]}')
            else:
                print(f'O arquivo solicitado não tem nenhuma das extensões: {exts}')
                resp = input('Deseja abrir mesmo assim?')
                if resp == 'sim':
                    startfile(f'{valor[1]}/{comando}{valor[0]}')
        # faz uma pesquisa por palavras nos diretórios indexados
        else:
            parecidos = []
            for item in retorno.keys():
                for frag_fala in comando.split():
                    if frag_fala in item.split() and len(frag_fala) > 2 and item not in parecidos and (retorno.get(item)[0] in exts):
                        # adiciona na lista os itens encontrados que são parecidos com o solicitado
                        parecidos.append(item)
            # se for encontrada apenas uma correspondência, a abre
            if len(parecidos) == 1:
                print('Trabalhando nisso...\n')
                valor = retorno.get(parecidos[0])
                startfile(f'{valor[1]}/{parecidos[0]}{valor[0]}')
                print(valor)
            # se forem encontradas várias correspondências, pergunta ao usuário se ele deseja abrir alguma delas
            elif len(parecidos) > 1:
                print(f'{parecidos}\n')
                while True:
                    x = input('Não encontrei o item solicitado. Alguma das opções acima é o que você deseja? ').lower()
                    if x == 'sim':
                        resp = int(input('Qual indice? '))
                        print('Trabalhando nisso...\n')
                        valor = retorno.get(parecidos[resp])
                        startfile(f'{valor[1]}/{parecidos[resp]}{valor[0]}')
                        break
                    elif x == 'não':
                        print('Foi mal mano\n')
                        break
                    else:
                        print('Tendi foi nada kkkk\n')
            # se não encontrar nenhuma correspondência, abre o menu iniciar, digita na pesquisa
            # a fala do usuário e dá enter
            else:
                pa.hotkey('win', 's')
                time.sleep(0.5)
                pa.typewrite(comando)
                time.sleep(0.5)
                pa.press('enter')

    # comando para fazer uma pesquisa no google
    elif comando[0] == 'pesquisar':
        # retira a palavra 'pesquisar' do comando
        comando.pop(0)
        # une a lista com as palavras do comando em uma string
        comando = ' '.join(comando)
        site = 'www.google.com/search?q='
        # substitui os caracteres especiais pelos correspondentes na URL
        comando = comando.replace('%', '%25')
        comando = comando.replace('+', '%2B')
        comando = comando.replace(' ', '+')
        # faz a pesquisa no navegador padrão
        startfile(site + comando)

    # comando para fechar janelas
    elif comando[0] == 'fechar':
        # retira a palavra 'fechar' do comando
        comando.pop(0)
        # une a lista com as palavras do comando em uma string
        comando = ' '.join(comando)
        # obtém uma lista com as janelas abertas cujo título corresponde à solicitação do usuário
        lista = pa.getWindowsWithTitle(comando).copy()
        # se existir apenas uma correspondência, a fecha
        if len(lista) == 1:
            pa.getWindowsWithTitle(comando)[0].close()
        elif len(lista) == 0:
            print('não encontrado')
        else:
            # se houver mais de uma correspondência,
            # cria uma lista com o título das janelas
            print(list(map(lambda x: x.title, lista)))
            # pergunta para o usuário qual o item da lista ele quer fechar
            ind = int(input('Qual o índice? '))
            # fecha o item especificado
            lista[ind].close()

    # comando para mover arquivos
    elif comando[0] == 'mover':
        print('Mostre o caminho para o Arquivo')
        y = pesquisador()
        print('Mostre o caminho para onde vai o Arquivo')
        w = pesquisador()
        print('Origem:', y)
        print('Destino:', w)
        con = str(input('Confirma? '))
        if con == 'sim':
            print('Movendo')
            # move o arquivo entre o diretório de origem e o de destino
            shutil.move(y, w)
        elif con == 'não':
            y = ''
            w = ''

    # comando não terminado
    """
    elif comando[0] == 'editar':
        comando.pop(0)
        comando = ' '.join(comando)
        results = []
        x = 0
        while True:
            if retorno.get(f'{comando}{x}'):
                results.append(comando)
                x += 1
            else:
                break
        if len(results) == 1:
            valor = retorno.get(f'{comando}0')
            if valor[0] in ['.txt', '.docx']:
                startfile(f'{valor[1]}/{comando}{valor[0]}')
        elif len(results) > 1:
            print('Qual você deseja? ')
            print(results)
            x = 0
            print(f'{results[0]}{x}')
            results = [f'{item}{retorno.get(f"{item}{x}")[0]}' for item in results for x in range(len(results))]
            results = list(set(filter(lambda prog: fileext(prog) in ['.txt', '.docx'], results)))
            print(results)
            resp = int(input())
            valor = results[resp]
            valorsem = f'{valor.replace(fileext(valor), "")}{resp}'
            startfile(f'{retorno.get(valorsem)[1]}/{valor}')
"""

