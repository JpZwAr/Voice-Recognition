from os import listdir, path

raiz = 'C:/ProgramData/Microsoft/Windows/Start Menu/Programs'
saida = 'C:/Users/Victor Mateus/Desktop'


def fileext(nome):
    ext = ''
    try:
        for i in range(len(nome) - list(nome)[::-1].index('.') - 1, len(nome)):
            ext = ext + nome[i]
        return ext
    except ValueError:
        return ''


def scandir(root, output):
    pastas = 0
    pastas_negadas = []
    arquivos = []
    dires = []
    diret = root
    file = open(f'{output}/Output.txt', 'w')
    while True:
        print(f'{pastas} pastas analisadas')
        while True:
            try:
                indice = listdir(diret)
                break
            except PermissionError:
                pastas_negadas.append(diret)
                diret = dires.pop()
        diret_qnt = 0
        arquivos.clear()
        for item in indice:
            if path.isdir(f'{diret}/{item}'):
                dires.insert(len(dires) - diret_qnt, f'{diret}/{item}')
                diret_qnt += 1
            else:
                arquivos.append(f'    Arquivo {fileext(item)}: {item}\n')
        if len(arquivos) > 0:
            arquivos.sort()
            file.write(f'{diret}:\n')
            for item in arquivos:
                file.write(item)
            file.write('\n\n')
        pastas += 1
        if not dires:
            if pastas_negadas:
                file.write(f'Não foi possível obter acesso a:\n    {pastas_negadas}')
            file.close()
            break
        diret = dires.pop()


scandir(raiz, saida)
