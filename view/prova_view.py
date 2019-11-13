from kivy.uix.screenmanager import Screen
from kivy.storage.jsonstore import JsonStore
from kivy.lang import Builder
from widgets_personalizados import Toast
import random

class Prova(Screen):
	modo = ''
	materia = ''
	caminho = './materias_bd.json'
	modos = ['Tudo', 'Padrão', 'Alternativa', 'Dissertativa', 'Aleatório', 'Mais Erradas']
	perguntas = {}

	def __init__(self, **kwargs):
		super(Prova, self).__init__(**kwargs)

	def carregar_prova(self, modo, materia):
		container = self.ids.container
		container._index = 0
		
		bd = JsonStore(self.caminho, indent = 4, sort_keys = False)
		self.perguntas = {}

		container.clear_widgets()

		chaves = bd.keys()
		todas_materias = [bd.get(i) for i in chaves]
		p = dict()
		for i in range(len(chaves)):
			p[chaves[i]] = todas_materias[i]['perguntas']
		materia_atual = p[materia].copy()

		if modo == 'Tudo': self.tudo(container, materia_atual)
		elif modo == 'Padrão': self.padrao(container, materia_atual)
		elif modo == 'Alternativa': self.alternativa(container, materia_atual)
		elif modo == 'Dissertativa': self.dissertativa(container, materia_atual)
		elif modo == 'Aleatório': self.aleatorio(container, materia_atual)
		elif modo == 'Mais Erradas': self.mais_erradas(container, materia_atual)

	def tudo(self, container, materia_atual):
		contagem = self.contagem(materia_atual, 'padrão')
		contagem += self.contagem(materia_atual, 'alternativa')
		contagem += self.contagem(materia_atual, 'dissertativa')

		if contagem >= 1:
			for numero_pergunta, lista_pergunta in materia_atual.items():
				if lista_pergunta[0] == 'padrão':
					materia = Builder.load_string(f'''
BoxLayout:
	orientation: 'vertical'
	padding: 10, 10
	spacing: dp('10')
	LabelPergunta:
		id: '{numero_pergunta}'
		text: '{numero_pergunta}'
		size_hint: 1, .1
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
				elif lista_pergunta[0] == 'alternativa':
					materia = Builder.load_string(f'''
BoxLayout:
	orientation: 'vertical'
	padding: 10, 10
	spacing: dp('10')
	LabelPergunta:
		id: '{numero_pergunta}'
		text: '{numero_pergunta}'
		size_hint: 1, .1
	BoxLayout:
		orientation: 'vertical'
		size_hint: 1, .4
		ScrollableLabel:
			text: '{lista_pergunta[1]}'
			cor_fundo: app.color_caixa_pergunta
	BoxLayout:
		spacing: dp('5')
		size_hint: 1, .133
		ToggleCheckBox:
			id: respostaA{numero_pergunta}
			group: '{numero_pergunta}'
			size_hint: .2, 1
			text: 'A'
			font_size: app.tam_font
		TextInput:
			id: textoA{numero_pergunta}
			text: '{lista_pergunta[2][0]["A"]}'
			font_size: app.tam_font
	BoxLayout:
		spacing: dp('5')
		size_hint: 1, .133
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
		size_hint: 1, .133
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
				elif lista_pergunta[0] == 'dissertativa':
					materia = Builder.load_string(f'''
BoxLayout:
	orientation: 'vertical'
	padding: 10, 10
	spacing: dp('10')
	ScrollableLabel:
		id: '{numero_pergunta}'
		text: '{numero_pergunta}'
		size_hint: 1, .1
		cor_fundo: app.color_caixa_pergunta
	LabelResposta:
		text: '{lista_pergunta[1]}'
		size_hint: 1, .45
		text_size: self.size
		halign: 'center'
		valign: 'middle'
	Texto:
		id: resposta{numero_pergunta}
		hint_text: 'Resposta'
		text_hint: 'Resposta'
		size_hint: 1, .45
		font_size: app.tam_font
		multiline: True
''')
				container.add_widget(materia)
				self.perguntas[numero_pergunta] = materia
			finalizar_prova = self.finalizar_prova(materia_atual)
			container.add_widget(finalizar_prova)
		else:
			Toast.show('Não há perguntas nessa matéria!!')

	def padrao(self, container, materia_atual):
		contagem = self.contagem(materia_atual, 'padrão')
		if contagem >= 1:
			for numero_pergunta, lista_pergunta in materia_atual.items():
				if lista_pergunta[0] == 'padrão':
					materia = Builder.load_string(f'''
BoxLayout:
	orientation: 'vertical'
	padding: 10, 10
	spacing: dp('10')
	LabelPergunta:
		id: '{numero_pergunta}'
		text: '{numero_pergunta}'
		size_hint: 1, .1
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
					container.add_widget(materia)
					self.perguntas[numero_pergunta] = materia
			finalizar_prova = self.finalizar_prova(materia_atual)
			container.add_widget(finalizar_prova)
		else:
			Toast.show('Não há perguntas padrão nessa matéria!!')

	def alternativa(self, container, materia_atual):
		contagem = self.contagem(materia_atual, 'alternativa')
		if contagem >= 1:
			for numero_pergunta, lista_pergunta in materia_atual.items():
				if lista_pergunta[0] == 'alternativa':
					materia = Builder.load_string(f'''
BoxLayout:
	orientation: 'vertical'
	padding: 10, 10
	spacing: dp('10')
	LabelPergunta:
		id: '{numero_pergunta}'
		text: '{numero_pergunta}'
		size_hint: 1, .1
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
					container.add_widget(materia)
					self.perguntas[numero_pergunta] = materia
			finalizar_prova = self.finalizar_prova(materia_atual)
			container.add_widget(finalizar_prova)
		else:
			Toast.show('Não há perguntas alternativa nessa matéria!!')

	def dissertativa(self, container, materia_atual):
		contagem = self.contagem(materia_atual, 'dissertativa')
		if contagem >= 1:			
			for numero_pergunta, lista_pergunta in materia_atual.items():
				if lista_pergunta[0] == 'dissertativa':
					materia = Builder.load_string(f'''
BoxLayout:
	orientation: 'vertical'
	padding: 10, 10
	spacing: dp('10')
	LabelPergunta:
		text: '{numero_pergunta}'
		size_hint: 1, .1
	LabelResposta:
		text: '{lista_pergunta[1]}'
		size_hint: 1, .4
	Texto:
		id: resposta{numero_pergunta}
		size_hint: 1, .5
		font_size: app.tam_font
		multiline: True
		hint_text: 'resposta'
''')
					container.add_widget(materia)
					self.perguntas[numero_pergunta] = materia
			finalizar_prova = self.finalizar_prova(materia_atual)
			container.add_widget(finalizar_prova)
		else:
			Toast.show('Não há perguntas dissertativas nessa matéria!!')

	def aleatorio(self, container, perguntas):
		contagem = self.contagem(perguntas, 'padrão')
		contagem += self.contagem(perguntas, 'alternativa')
		contagem += self.contagem(perguntas, 'dissertativa')

		perguntas2 = list(perguntas.keys())
		perguntas3 = random.shuffle(perguntas2)
		
		materia_atual = {}
		
		for i in perguntas2:
			materia_atual[i] = perguntas[i]
		
		if contagem >= 1:
			for numero_pergunta, lista_pergunta in materia_atual.items():
				if lista_pergunta[0] == 'padrão':
					materia = Builder.load_string(f'''
BoxLayout:
	orientation: 'vertical'
	padding: 10, 10
	spacing: dp('10')
	LabelPergunta:
		id: '{numero_pergunta}'
		text: '{numero_pergunta}'
		size_hint: 1, .1
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
				elif lista_pergunta[0] == 'alternativa':
					materia = Builder.load_string(f'''
BoxLayout:
	orientation: 'vertical'
	padding: 10, 10
	spacing: dp('10')
	LabelPergunta:
		id: '{numero_pergunta}'
		text: '{numero_pergunta}'
		size_hint: 1, .1
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
				elif lista_pergunta[0] == 'dissertativa':
					materia = Builder.load_string(f'''
BoxLayout:
	orientation: 'vertical'
	padding: 10, 10
	spacing: dp('10')
	LabelPergunta:
		id: '{numero_pergunta}'
		text: '{numero_pergunta}'
		size_hint: 1, .1
	LabelResposta:
		text: '{lista_pergunta[1]}'
		size_hint: 1, .45
		text_size: self.size
		halign: 'center'
		valign: 'middle'
	Texto:
		id: resposta{numero_pergunta}
		hint_text: 'Resposta'
		text_hint: 'Resposta'
		size_hint: 1, .45
		font_size: app.tam_font
		multiline: True
''')
					container.add_widget(materia)
					self.perguntas[numero_pergunta] = materia
			finalizar_prova = self.finalizar_prova(materia_atual)
			container.add_widget(finalizar_prova)
		else:
			Toast.show('Não há perguntas nessa matéria!!')

	def mais_erradas(self, container, materia_atual):
		pass

	def contagem(self, materia_atual, nome):
		contagem = 0
		for i in materia_atual:
			if materia_atual[i][0] == nome: contagem += 1
		return contagem

	def finalizar_prova(self, todas_perguntas):
		return Builder.load_string(f'''
BoxLayout:
	orientation: 'vertical'
	size_hint: 1, 1
	padding: 10, 10
	spacing: dp('10')
	Botao:
		text: 'Desistir?'
		font_size: app.tam_font
		size_hint: 1, .5
		cor_fundo: app.color_button
		cor_fundo_pressionado: app.color_button_pressed
		on_release:
			app.screen_manager.current = "estudar"
			app.screen_manager.transition.direction = "right"
	Botao:
		text: 'Finalizar Prova?'
		font_size: app.tam_font
		size_hint: 1, .5
		cor_fundo: app.color_button
		cor_fundo_pressionado: app.color_button_pressed
		on_release:
			app.screen_manager.current = "resultado"
			app.screen_manager.transition.direction = "left"
			app.screen_manager.get_screen('resultado').resultado({todas_perguntas})
''')
