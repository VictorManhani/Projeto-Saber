from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from widgets_personalizados import Toast

import requests

#from model import materias_model
#from controller import materias_controller

class Baixar(Screen):
	def __init__(self, **kwargs):
		super(Baixar, self).__init__(**kwargs)
		
	def pesquisar_materias_web(self):		
		container = self.ids.container
		container.clear_widgets()
		url = "http://localhost:8080/materias/nomes"
		url2 = "https://victormanhani.github.io/projeto-saber/materias_bd.json"
		nomes = []
	
		try:
			materias = requests.get(url)
			nomes = materias.json()['nomes']
		except:
			try:
				materias = requests.get(url2)
				nomes = [materia for materia in materias.json()]
			except:
				Toast.show('Problemas no servidor!')
		if not nomes:
			Toast.show('Não há matérias!')

		for i in nomes:
			bt = Builder.load_string(f'''
Botao:
	text: "{i}"
	size_hint: 1, None
	height: dp('50')
	on_release:
		print(self.text)
''')
			container.add_widget(bt)
		
