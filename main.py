from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.button import MDFillRoundFlatIconButton, MDFillRoundFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDToolbar
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import MDList
from kivymd.uix.list import OneLineListItem
from openpyxl import Workbook
import datetime
import os
from random import randint
import math


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
    vetor.append(round(dr, 10))
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
    vetor.append(round(dn, 10))
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


class LevantamentoTaquiometrico(MDApp):
    '''def on_start(self):
        for i in range(0, 30):
            self.lista_pontos.add_widget(
                OneLineListItem(text=f'''"1,45";"A";"B";"0";"0,775";"0,865";"0,95";"99 02 25";"17,06793472140695";"797,8694039382831";''')
            )'''

    def campos_vazios(self):
        campos = [self.cota_input.text,
                  self.altura_aparelho_input.text,
                  self.estacao_input.text,
                  self.ponto_visado_input.text,
                  self.ang_horizontal.text,
                  self.fio_inferior.text,
                  self.fio_medio.text,
                  self.fio_superior.text,
                  self.ang_vertical.text]
        for value in campos:
            print(value)
            if value == "":
                return True
        return False

    def calculo_vazio(self):
        campos = [self.distancia_reduzida.text,
                  self.cota_nova.text]
        for value in campos:
            print(value)
            if value == "":
                return True
        return False

    def calcula(self, args):
        if self.campos_vazios():
            self.label_erro_calcular.text = "Não pode ter campos vazios"
        else:
            vetor = calcula(self.cota_input.text,
                            self.altura_aparelho_input.text,
                            self.estacao_input.text,
                            self.ponto_visado_input.text,
                            self.ang_horizontal.text,
                            self.fio_inferior.text,
                            self.fio_medio.text,
                            self.fio_superior.text,
                            self.ang_vertical.text)
            self.distancia_reduzida.text = str(vetor[9])
            self.cota_nova.text = str(vetor[11])
            self.label_erro_calcular.text = ""

    def adicionar(self, args):
        if self.campos_vazios():
            self.label_erro_calcular.text = "Não pode ter campos vazios"
        if self.calculo_vazio():
            self.label_erro_adicionar.text = "Favor calcular antes"
        else:
            campos = [self.cota_input.text,
                      self.altura_aparelho_input.text,
                      self.estacao_input.text,
                      self.ponto_visado_input.text,
                      self.ang_horizontal.text,
                      self.fio_inferior.text,
                      self.fio_medio.text,
                      self.fio_superior.text,
                      self.ang_vertical.text,
                      self.distancia_reduzida.text,
                      self.cota_nova.text,
                      self.observacoes.text,
                      datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")]
            aux = ""
            for campo in campos:
                aux += campo + ';'
            aux+="\n"
            self.lista_pontos.add_widget(
                OneLineListItem(text=aux)
            )
            self.label_erro_calcular.text = ""
            self.label_erro_adicionar.text = ""
            self.distancia_reduzida.text = ""
            self.cota_nova.text = ""

    #REFAZER!!!!
    def exporta_excel(self):
        book = Workbook()
        sheet = book.active
        nome_xlsx = f'{os.path.dirname(os.path.abspath(__file__))}\\LevantamentoTaquiometrico_' + str(
            datetime.datetime.today())[:10] + '_' + str(randint(1, 999999)) + '.xlsx'

        sheet['A1'] = 'Altura do Aparelho'
        sheet['B1'] = 'Estação'
        sheet['C1'] = 'Ponto Visado'
        sheet['D1'] = 'Ângulo Horizontal'
        sheet['E1'] = 'Leitura na Mira: Fio Inferior'
        sheet['F1'] = 'Leitura na Mira: Fio Médio'
        sheet['G1'] = 'Leitura na Mira: Fio Superior'
        sheet['H1'] = 'Ângulo Vertical'
        sheet['I1'] = 'Distância Reduzida'
        sheet['J1'] = 'Cota'
        sheet['K1'] = 'Observações'
        sheet['L1'] = 'Data da Leitura'

        cont = 2
        lista = self.lista_pontos.children
        for vetor in lista:
            vetor = vetor.text.split(';')
            print(vetor)
            sheet['A' + str(cont)] = str(vetor[1])
            sheet['B' + str(cont)] = str(vetor[2])
            sheet['C' + str(cont)] = str(vetor[3])
            sheet['D' + str(cont)] = str(vetor[4])
            sheet['E' + str(cont)] = str(vetor[5])
            sheet['F' + str(cont)] = str(vetor[6])
            sheet['G' + str(cont)] = str(vetor[7])
            sheet['H' + str(cont)] = str(vetor[8])
            sheet['I' + str(cont)] = str(vetor[9])
            sheet['J' + str(cont)] = str(vetor[10])
            sheet['K' + str(cont)] = str(vetor[11])
            sheet['L' + str(cont)] = str(vetor[12])
            cont = cont + 1
        try:
            book.save(nome_xlsx)
            self.lista_pontos.clear_widgets(self.lista_pontos.children)
        except:
            pass

    def build(self):
        self.state = 0
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.primary_hue = "900"
        self.do_rotation = "False"
        self.do_scale = "False"
        self.do_translation = "False"
        self.rotation = "90"
        screen = MDScreen()

        #Toolbar
        self.toolbar = MDToolbar(title="Levantamento Taquiometrico")
        self.toolbar.pos_hint = {"top":1}
        screen.add_widget(self.toolbar)
        self.toolbar.right_action_items = [
            ["file-download", lambda x: self.exporta_excel()]
        ]
        self.cota_input=MDTextField(
            hint_text="Cota (RN)",
            helper_text="Informar a Cota",
            helper_text_mode="on_focus",
            halign="center",
            size_hint=(0.45, 1),
            pos_hint={"center_x": .25, "center_y": .8},
            font_size=22
        )
        screen.add_widget(self.cota_input)
        self.altura_aparelho_input = MDTextField(
            hint_text="Altura Aparelho",
            helper_text="Informar a Altura do Aparelho em Metros",
            helper_text_mode="on_focus",
            halign="center",
            size_hint=(0.15, 1),
            pos_hint={"center_x": .1, "center_y": .7},
            font_size=22
        )
        self.estacao_input=MDTextField(
            hint_text="Estação",
            helper_text="Informar a Estação",
            helper_text_mode="on_focus",
            halign="center",
            size_hint=(0.125, 1),
            pos_hint={"center_x": .27, "center_y": .7},
            font_size=22
        )
        self.ponto_visado_input=MDTextField(
            hint_text="Ponto Visado",
            helper_text="Informar o Ponto Visado",
            helper_text_mode="on_focus",
            halign="center",
            size_hint=(0.125, 1),
            pos_hint={"center_x": .41, "center_y": .7},
            font_size=22
        )
        screen.add_widget(self.altura_aparelho_input)
        screen.add_widget(self.estacao_input)
        screen.add_widget(self.ponto_visado_input)
        self.ang_horizontal=MDTextField(
            hint_text="Ângulo Horizontal (x)",
            helper_text="Exemplo: 122 10 20",
            helper_text_mode="on_focus",
            halign="center",
            size_hint=(0.21, 1),
            pos_hint={"center_x": .13, "center_y": .6},
            font_size=22
        )

        self.ang_vertical=MDTextField(
            hint_text="Ângulo Vertical (y)",
            helper_text="Exemplo: 122 10 20",
            helper_text_mode="on_focus",
            halign="center",
            size_hint=(0.21, 1),
            pos_hint={"center_x": .37, "center_y": .6},
            font_size=22
        )
        screen.add_widget(self.ang_horizontal)
        screen.add_widget(self.ang_vertical)
        self.fio_inferior = MDTextField(
            hint_text="Fio Inferior",
            helper_text="Informar a altura Fio Inferior em metros",
            helper_text_mode="on_focus",
            halign="center",
            size_hint=(0.14, 1),
            pos_hint={"center_x": .095, "center_y": .5},
            font_size=22
        )
        self.fio_medio = MDTextField(
            hint_text="Fio Médio",
            helper_text="Informar a altura Fio Médio em metros",
            helper_text_mode="on_focus",
            halign="center",
            size_hint=(0.14, 1),
            pos_hint={"center_x": .25, "center_y": .5},
            font_size=22
        )
        self.fio_superior = MDTextField(
            hint_text="Fio Superior",
            helper_text="Informar a altura Fio Superior em metros",
            helper_text_mode="on_focus",
            halign="center",
            size_hint=(0.14, 1),
            pos_hint={"center_x": .405, "center_y": .5},
            font_size=22
        )
        screen.add_widget(self.fio_inferior)
        screen.add_widget(self.fio_medio)
        screen.add_widget(self.fio_superior)

        # "CALCULAR" button
        screen.add_widget(MDFillRoundFlatButton(
            text="CALCULAR",
            font_size=17,
            pos_hint={"center_x": 0.25, "center_y": 0.4},
            on_press=self.calcula
        ))
        self.label_erro_calcular = MDLabel(
            halign="center",
            pos_hint={"center_x": 0.25, "center_y": 0.34},
            theme_text_color="Secondary",
            font_style="H5"
        )
        screen.add_widget(self.label_erro_calcular)

        self.distancia_reduzida = MDTextField(
            hint_text="Distância Reduzida(DR)",
            helper_text="",
            helper_text_mode="on_focus",
            halign="center",
            size_hint=(0.21, 1),
            pos_hint={"center_x": .13, "center_y": .27},
            font_size=22,
            readonly="True"
        )

        self.cota_nova = MDTextField(
            hint_text="Cota Nova",
            helper_text="",
            helper_text_mode="on_focus",
            halign="center",
            size_hint=(0.21, 1),
            pos_hint={"center_x": .37, "center_y": .27},
            font_size=22,
            readonly="True"
        )
        screen.add_widget(self.distancia_reduzida)
        screen.add_widget(self.cota_nova)

        self.observacoes = MDTextField(
            hint_text="Observações",
            helper_text="",
            helper_text_mode="on_focus",
            halign="auto",
            size_hint=(0.45, 1),
            pos_hint={"center_x": 0.25, "center_y": 0.18},
            font_size=18
        )
        screen.add_widget(self.observacoes)

        self.label_erro_adicionar = MDLabel(
            halign="center",
            pos_hint={"center_x": 0.25, "center_y": 0.12},
            theme_text_color="Secondary",
            font_style="H5"
        )
        screen.add_widget(self.label_erro_adicionar)

        #"ADICIONAR" button
        screen.add_widget(MDFillRoundFlatButton(
            text="ADICIONAR",
            font_size=17,
            pos_hint={"center_x": 0.25, "center_y": 0.06},
            on_press=self.adicionar
        ))

        self.scroll_view = ScrollView(
            size_hint=(0.48, .9),
            pos_hint={"center_x": .74, "top": .9}
        )
        self.lista_pontos = MDList(
            size_hint=(1, 1),
            pos_hint={"center_x": .74, "top": .9},
            adaptive_height="True"
        )
        self.scroll_view.add_widget(self.lista_pontos)
        screen.add_widget(self.scroll_view)

        return screen


if __name__ == '__main__':
    LevantamentoTaquiometrico().run()