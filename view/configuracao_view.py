from kivy.uix.screenmanager import Screen
from widgets_personalizados import Toast

class Configuracao(Screen):
	def __init__(self, **kwargs):
		super(Configuracao, self).__init__(**kwargs)

	def toast(self, msg):
		Toast.show(msg)
	
