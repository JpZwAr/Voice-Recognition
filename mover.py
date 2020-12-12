import time
import os
import shutil
def pesquisador():
    u = 'C:/'
    print(os.listdir("C:/"))
    for s in range(1000):
        a = str(input('Chegamos?(sim/não) '))
        if a == 'sim':
            b = str(input('Digite o nome do arquivo: '))
            u = u + b + '/'
            break
        elif a != 'sim' and a != 'não':
            print('Não entendi')
            break
        else:
            z = str(input('Pra onde chefe? '))
            u = u + z + '/'
            print(u)
            print(os.listdir(u))
    return(u)
print('Mostre o caminho para o Arquivo')
y = pesquisador()
print('Mostre o caminho para onde vai o Arquivo')
w = pesquisador()
print('Origem:', y)
print('Destino:', w)
con = str(input(('Confirma? ')))
if con == 'sim':
    print('Movendo')
    shutil.move(y, w)
elif con == 'não':
    y = ''
    w = ''