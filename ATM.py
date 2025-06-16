entrada = int(input('Digite um valor: '))
valor = entrada
cedula = 0
notas = (50,20,10,5,2,1)
cedulas = [0,0,0,0,0,0]
while valor != 0:
    if valor >= notas[0]:
        cedula += 1
        cedulas[0] += 1
        valor -= notas[0]
    elif valor >= notas[1]:
        cedula += 1
        cedulas[1] += 1
        valor -= notas[1]
    elif valor >= notas[2]:
        cedula += 1
        cedulas[2] += 1
        valor -= notas[2]
    elif valor >= notas[3]:
        cedula += 1
        cedulas[3] += 1
        valor -= notas[3]
    elif valor >= notas[4]:
        cedula += 1
        cedulas[4] += 1
        valor -= notas[4]
    elif valor >= notas[5]:
        cedula += 1
        cedulas[5] += 1
        valor -= notas[5]
    else:
        break
print(f'O valor digitado foi {entrada}')
print(f"""Foram usadas {cedula} cedulas
Sendo elas
{cedulas[0]} notas de 50 reais
{cedulas[1]} notas de 20 reais
{cedulas[2]} notas de 10 reais
{cedulas[3]} notas de 5 reais
{cedulas[4]} notas de 2 reais
{cedulas[5]} moedas de 1 Real""")