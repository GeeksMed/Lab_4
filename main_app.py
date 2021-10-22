from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout


class ProjectName(GridLayout):
    def __init__(self, **kwargs):
        super(ProjectName, self).__init__(**kwargs)

        g = "Esto es un mensaje guardado en una variable"
        self.ids['textInp2'].text = g


class MyApp(App):
    def build(self):
        return ProjectName()


if __name__ in ('__main__', '__android__'):
    MyApp().run()