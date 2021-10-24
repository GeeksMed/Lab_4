from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from calculos_planilha import exemplo_vetor as ex


class ProjectName(GridLayout):
    def __init__(self, **kwargs):
        super(ProjectName, self).__init__(**kwargs)

    #['222', 1.65, 'A', 'B', '0', 1.185, 1.43, 1.675, '120 10 20', 36.62222564810101, -21.07088174164053, 200.92911825835947]
    #   0      1    2    3    4      5     6     7         8               9                   10               11
    def adicionar_calculando(self, vetor=[]):
        vetor.append(ex())
        aux = ""
        for valores in vetor:
            for i, valor in enumerate(valores):
                if i in (1, 5, 6, 7, 9, 11):
                    aux += str(valor).replace(".",",") + "; "
                elif i in (2, 3, 4, 8):
                    aux += valor + "; "
                else:
                    pass
            aux += "\n"
            self.ids['textInp2'].text = aux


class MyApp(App):
    def build(self):
        return ProjectName()


if __name__ in ('__main__', '__android__'):
    MyApp().run()