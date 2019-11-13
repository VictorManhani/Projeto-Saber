from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

class Comentario(Screen):
	
	def __init__(self, **kwargs):
		super(Comentario, self).__init__(**kwargs)		
	
	def carregar_pergunta(self, numero_pergunta, todas_perguntas, respostas_dadas, status):
		container = self.ids.container
		container.clear_widgets()

		if status == 'errado':
			titulo = Builder.load_string(f'''
MeuLabel:
	text: "{numero_pergunta}"
	size_hint: 1, .2
	cor_fundo: [.6,0,0,1]
''')
		elif status == 'certo':
			titulo = Builder.load_string(f'''
MeuLabel:
	text: "{numero_pergunta}"
	size_hint: 1, .2
	cor_fundo: [0,.6,0,1]
''')
		container.add_widget(titulo)
		container.add_widget(self.estrutura_da_pergunta(numero_pergunta, respostas_dadas, todas_perguntas))
		
	def estrutura_da_pergunta(self, nome_pergunta, respostas_dadas, todas_perguntas):
		resposta_pergunta = respostas_dadas[nome_pergunta]
		
		for numero_pergunta, lista_pergunta in todas_perguntas.items():
			if nome_pergunta == numero_pergunta:
				if lista_pergunta[0] == 'padrão':
					materia = Builder.load_string(f'''
BoxLayout:
	orientation: 'vertical'
	padding: 10, 10
	spacing: dp('10')
	LabelResposta:
		text: '{lista_pergunta[1]}'
		size_hint: 1, .7
		text_size: self.size
		halign: 'center'
		valign: 'middle'
	BoxLayout:
		size_hint: 1, .2
		spacing: dp('5')
		ToggleCheckBox:
			id: resposta_nao{numero_pergunta}
			group: '{numero_pergunta}'
			text: 'Não'
			font_size: app.tam_font
		ToggleCheckBox:
			id: resposta_sim{numero_pergunta}
			group: '{numero_pergunta}'
			text: 'Sim'
			font_size: app.tam_font
''')
					if resposta_pergunta == 'sim':
						materia.ids[f'resposta_sim{numero_pergunta}'].state = 'down'
					else:
						materia.ids[f'resposta_nao{numero_pergunta}'].state = 'down'

				elif lista_pergunta[0] == 'alternativa':
					materia = Builder.load_string(f'''
BoxLayout:
	orientation: 'vertical'
	padding: 10, 10
	spacing: dp('10')
	LabelResposta:
		text: '{lista_pergunta[1]}'
		size_hint: 1, .4
		text_size: self.size
		halign: 'center'
		valign: 'middle'
	BoxLayout:
		spacing: dp('5')
		size_hint: 1, .1
		ToggleCheckBox:
			id: respostaA{numero_pergunta}
			group: '{numero_pergunta}'
			size_hint: .2, 1
			text: 'A'
			font_size: app.tam_font
		Texto:
			id: textoA{numero_pergunta}
			text: '{lista_pergunta[2][0]["A"]}'
			font_size: app.tam_font
	BoxLayout:
		spacing: dp('5')
		size_hint: 1, .1
		ToggleCheckBox:
			id: respostaB{numero_pergunta}
			group: '{numero_pergunta}'
			size_hint: .2, 1
			text: 'B'
			font_size: app.tam_font
		Texto:
			id: textoB{numero_pergunta}
			text: '{lista_pergunta[2][0]["B"]}'
			font_size: app.tam_font
	BoxLayout:
		spacing: dp('5')
		size_hint: 1, .1
		ToggleCheckBox:
			id: respostaC{numero_pergunta}
			group: '{numero_pergunta}'
			size_hint: .2, 1
			text: 'C'
			font_size: app.tam_font
		Texto:
			id: textoC{numero_pergunta}
			text: '{lista_pergunta[2][0]["C"]}'
			font_size: app.tam_font
''')
					if resposta_pergunta == 'A':
						materia.ids[f'respostaA{numero_pergunta}'].state = 'down'
					elif resposta_pergunta == 'B':
						materia.ids[f'respostaB{numero_pergunta}'].state = 'down'
					else:
						materia.ids[f'respostaC{numero_pergunta}'].state = 'down'
				elif lista_pergunta[0] == 'dissertativa':
					materia = Builder.load_string(f'''
BoxLayout:
	orientation: 'vertical'
	padding: 10, 10
	spacing: dp('10')
	LabelResposta:
		text: '{lista_pergunta[1]}'
		size_hint: 1, .45
		text_size: self.size
		halign: 'center'
		valign: 'middle'
	Texto:
		id: resposta{numero_pergunta}
		hint_text: 'Resposta'
		#text_hint: 'Resposta'
		text: '{resposta_pergunta}'
		size_hint: 1, .45
		font_size: app.tam_font
		multiline: True
''')
		return materia
