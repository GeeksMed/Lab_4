import math

'''
while True:
    angulo = float(input("Informe angulo: "))

    seno = math.sin(math.radians(angulo))

    print("{:.3f}".format(seno))
'''
def transformar_grau_radianos(angulo):
    angulo = angulo.split(" ")
    if len(angulo) == 1:
        angulo = [float(angulo[0])]
    elif len(angulo) == 2:
        angulo = [float(angulo[0]), float(angulo[1])/60]
    elif len(angulo) == 3:
        angulo = [float(angulo[0]), float(angulo[1])/60, float(angulo[2])/60/60]

    somatorio = 0
    for valor in angulo:
        somatorio += valor
    return math.radians(somatorio)


def distancia_reduzida_zenital(vetor):
    leitura_na_mira_fio_inferior = vetor[5]
    leitura_na_mira_fio_superior = vetor[7]
    angulo_vertical = vetor[8]

    #dr = ((fs-fi)*100) * (sin(angulo) ** 2)
    fs = leitura_na_mira_fio_superior
    fi = leitura_na_mira_fio_inferior
    angulo = transformar_grau_radianos(angulo_vertical)
    dr = ((fs-fi)*100) * (math.sin(angulo) ** 2)
    vetor.append(dr)

    return vetor

def diferenca_nivel_zenital(vetor):
    altura_do_aparelho = vetor[1]
    leitura_na_mira_fio_inferior = vetor[5]
    leitura_na_mira_fio_medio = vetor[6]
    leitura_na_mira_fio_superior = vetor[7]
    angulo_vertical = vetor[8]

    #dn = ((fs - fi) * 100) * (math.sin(2 * angulo) / 2) + altura_do_aparelho - leitura_na_mira_fio_medio
    angulo = transformar_grau_radianos(angulo_vertical)
    dn = ((leitura_na_mira_fio_superior - leitura_na_mira_fio_inferior) * 100) * (math.sin(2 * angulo) / 2) + altura_do_aparelho - leitura_na_mira_fio_medio
    vetor.append(dn)

    return vetor


def calcula_cota(vetor):
    cota = float(vetor[0])
    dn = vetor[10]
    vetor.append(cota + dn) if cota + dn < cota else vetor.append(cota - dn)
    return vetor


def calcula(cota, altura_do_aparelho, estacao, ponto_visado, angulo_horizontal, leitura_na_mira_fio_inferior, leitura_na_mira_fio_medio, leitura_na_mira_fio_superior, angulo_vertical):
    vetor = [
        cota,
        float(altura_do_aparelho.replace(",", ".")),
        estacao,
        ponto_visado,
        angulo_horizontal,
        float(leitura_na_mira_fio_inferior.replace(",", ".")) if "," in leitura_na_mira_fio_inferior else float(leitura_na_mira_fio_inferior)/1000,
        float(leitura_na_mira_fio_medio.replace(",", ".")) if "," in leitura_na_mira_fio_medio else float(leitura_na_mira_fio_medio)/1000,
        float(leitura_na_mira_fio_superior.replace(",", ".")) if "," in leitura_na_mira_fio_superior else float(leitura_na_mira_fio_superior)/1000,
        angulo_vertical
    ]
    vetor = distancia_reduzida_zenital(vetor)
    vetor = diferenca_nivel_zenital(vetor)
    vetor = calcula_cota(vetor)
    return vetor


def exemplo_vetor():
    # testeFaculdade
    c = '800'
    ai = '1,45'
    est = 'A'
    pv = 'B'
    ah = '0'
    fi = '775'
    fm = '865'
    fs = '950'
    av = '99 02 25'

    resultado = calcula(c, ai, est, pv, ah, fi, fm, fs, av)
    return resultado

if __name__ == '__main__':
    #testeYoutube
    c = "222"
    ai = "1,65"
    est = 'A'
    pv = 'B'
    ah = '0'
    fi = "1,185"
    fm = "1,430"
    fs = "1,675"
    av = '120 10 20'

    resultado = calcula(c, ai, est, pv, ah, fi, fm, fs, av)
    print(resultado)

    # testeYoutube
    ai = "1,65"
    est = 'A'
    pv = 'B'
    ah = '0'
    fi = "1,025"
    fm = "1,685"
    fs = "2,345"
    av = '59 10 20'

    resultado = calcula(c, ai, est, pv, ah, fi, fm, fs, av)
    print(resultado)

