from os import chdir, listdir, path


def fileext(nome):
    ext = ''
    try:
        for i in range(len(nome) - list(nome)[::-1].index('.') - 1, len(nome)):
            ext = ext + nome[i]
        return ext
    except ValueError:
        return ''


def scandir(root, output):
    dires = []
    diret = root
    chdir(output)
    file = open('Output.txt', 'w')
    chdir(diret)
    while True:
        diret_qnt = 0
        arquivos = []
        for item in listdir():
            if path.isdir(f'{diret}/{item}'):
                dires.insert(len(dires) - diret_qnt, f'{diret}/{item}')
                diret_qnt += 1
                pastas += 1
            else:
                arquivos.insert(0, f'    Arquivo {fileext(item)}: {item}\n')
        if len(arquivos) > 0:
            file.write(f'{diret}:')
            file.write('\n')
            arquivos.sort()
            arquivos.reverse()
            for _ in arquivos:
                file.write(f'{arquivos.pop()}')
            file.write('\n\n')
        if len(dires) > 0:
            diret = dires.pop()
            chdir(diret)
        else:
            break
