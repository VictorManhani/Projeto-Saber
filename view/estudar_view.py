from kivy.uix.screenmanager import Screen
from kivy.storage.jsonstore import JsonStore
from kivy.lang import Builder

class Estudar(Screen):
	modo = ''
	materia = ''
	caminho = './materias_bd.json'
	modos = ['Tudo', 'Aleatório', 'Padrão', 'Alternativa', 'Dissertativa', 'Mais Erradas']
	
	def __init__(self, **kwargs):
		super(Estudar, self).__init__(**kwargs)
		self.carregar_conteudo()

	def carregar_conteudo(self):
		container = self.ids.container
		container.clear_widgets()

		titulo1 = Builder.load_string(f'''
LabelPergunta:
	text: 'Modo de Estudo'
	size_hint: 1, None
	height: dp('50')
''')
		container.add_widget(titulo1)

		for nome_modo in self.modos:
			modo = Builder.load_string(f'''
ToggleCheckBox:
	text: '{nome_modo}'
	group: 'modo'
	size_hint: 1, None
	height: dp('50')
	cor_fundo_pressionado: [0.95,0.61,0.07,1]
	on_release:
		app.root.get_screen('estudar').modo = '{nome_modo}'
''')
			container.add_widget(modo)
		titulo2 = Builder.load_string(f'''
LabelPergunta:
	text: 'Selecionar Matéria'
	size_hint: 1, None
	height: dp('50')
''')
		container.add_widget(titulo2)
		bd = JsonStore(self.caminho, indent=4, sort_keys=False)
		chaves = bd.keys()
		chaves1 = [bd.get(i) for i in chaves]
		chaves2 = [i for i in chaves]
		p = dict()
		for i in range(len(chaves)): 
			p[chaves2[i]] = chaves1[i]['perguntas']
		materias = p.copy()
		for nome_materia in materias.keys():
			materia = Builder.load_string(f'''
ToggleCheckBox:
	text: "{nome_materia}"
	group: 'materia'
	size_hint: 1, None
	height: dp('50')
	cor_fundo_pressionado: [0.95,0.61,0.07,1]
	on_release:
		app.root.get_screen('estudar').materia = self.text
''')
			container.add_widget(materia)

		bt_final = Builder.load_string(f'''
Botao:
	text: "Iniciar Prova"
	size_hint: 1, None
	height: dp('50')
	cor_fundo: app.color_button_pressed
	cor_fundo_pressionado: app.color_button
	on_release:
		app.root.get_screen('estudar').iniciar_prova()
''')
		container.add_widget(bt_final)

	def iniciar_prova(self):
		modo, materia = self.modo, self.materia
		self.parent.current = 'prova'
		self.parent.transition.direction = "left"
		self.parent.get_screen('prova').carregar_prova(modo, materia)
