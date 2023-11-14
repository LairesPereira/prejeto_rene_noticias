alunos = { 'rian': 1, 'rene': 3, 'lucas': 10, 'maria': 9, 'Dalina': 2, 'jack': 7}
alunos_dec = {}

lista_maiores = []


while len(alunos) > 0 :
    maior = 0
    nome = ''
    for i in alunos:
        if alunos[i] > maior:
            maior = alunos[i]
            nome = i

    alunos_dec[nome] = maior
    lista_maiores.append(nome)
    del alunos[nome]

print(lista_maiores)
print(alunos)
print(alunos_dec)

