import math

'''
while True:
    angulo = float(input("Informe angulo: "))

    seno = math.sin(math.radians(angulo))

    print("{:.3f}".format(seno))
'''
def distancia_reduzida(vetor):
    #dr = ((fs-fi)/10) * (sin(angulo) ** 2)
    pass


if __name__ == '__main__':
    altura_do_aparelho = 1.45
    estacao = 'A'
    ponto_visado = 'B'
    angulo_horizontal = '0'
    leitura_na_mira_fio_inferior = 775
    leitura_na_mira_fio_medio = 865
    leitura_na_mira_fio_superior = 950
    angulo_vertical = '99 02 25'

    vetor = [
        altura_do_aparelho,
        estacao,
        ponto_visado,
        angulo_horizontal,
        leitura_na_mira_fio_inferior,
        leitura_na_mira_fio_medio,
        leitura_na_mira_fio_superior,
        angulo_vertical
    ]

    distancia_reduzida(vetor)
