from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from calculos_planilha import exemplo_vetor as ex


class ProjectName(GridLayout):
    def __init__(self, **kwargs):
        super(ProjectName, self).__init__(**kwargs)

        g = "Esto es un mensaje guardado en una variable"
        #['222', 1.65, 'A', 'B', '0', 1.185, 1.43, 1.675, '120 10 20', 36.62222564810101, -21.07088174164053, 200.92911825835947]
        #   0      1    2    3    4      5     6     7         8               9                   10               11
        vetor = ex()
        aux = ""
        for i, valores in enumerate(vetor):
            if i in (1, 5, 6, 7, 9, 11):
                aux += str(valores).replace(".",",") + "; "
            elif i in (2, 3, 4, 8):
                aux += valores + "; "
            else:
                pass
        self.ids['textInp2'].text = aux


class MyApp(App):
    def build(self):
        return ProjectName()


if __name__ in ('__main__', '__android__'):
    MyApp().run()