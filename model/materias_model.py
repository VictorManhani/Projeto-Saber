from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from dao import materias_dao

def criar_abrir_arquivo(caminho):
	arquivo = materias_dao.criar_abrir_arquivo(caminho)
	return arquivo

def salvar_materia(bd, materia, perguntas):
	return materias_dao.salvar_materia(bd, materia, perguntas)

def obter_todas_materias(bd):
	perguntas = materias_dao.obter_todas_materias(bd)
	return perguntas

def excluir_materia(bd, nome_materia):
	resultado = materias_dao.excluir_materia(bd, nome_materia)
	return resultado

def editar_materia():
	self.perguntas = {}

def criar_materia(container, nome_materia, bd):
	pass

def carregar_materia(container, materias):
	container.clear_widgets()
	for nome_materia in materias.keys():
		materia = Builder.load_string(f'''
BoxLayout:
	id: box
	size_hint: 1, None
	height: dp('60')
	Botao:
		text: "{nome_materia}"
		size_hint: .7, 1
		cor_fundo: app.color_button
		cor_fundo_pressionado: app.color_button_pressed
		on_release:
			app.screen_manager.current = "perguntas"
			app.screen_manager.transition.direction = "left"
			app.screen_manager.get_screen("perguntas").ids.materia_nome.text = "{nome_materia}"
			app.screen_manager.get_screen("perguntas").carregar_perguntas("{nome_materia}")
	SpinnerBotao:
		text: '...'
		values: "Editar", "Excluir", "Compartilhar"
		font_size: app.tam_font
		size_hint: .3, 1
		option_cls: "MySpinnerOption2"
		padding: dp('10'), dp('10')
		spacing: dp('5')
		on_text:
			if self.text == "Editar": app.screen_manager.get_screen("materias").editar_materia("{nome_materia}")
			elif self.text == "Excluir": app.screen_manager.get_screen("materias").excluir_materia("{nome_materia}")
			elif self.text == "Compartilhar": app.screen_manager.get_screen("materias").compartilhar_materia("{nome_materia}")
			self.text = '...'
''')
		container.add_widget(materia)

def popup_criar_materia():
	popup = Builder.load_string('''
Popup:
	id: popup
	title: 'Criar Matéria'
	size_hint: .8, .8
	auto_dismiss: False
	BoxLayout:
		orientation: 'vertical'
		TextInput:
			id: texto_materia
			size_hint: 1, .7
			hint_text: 'Nome da Matéria'
			font_size: app.tam_font
			on_text:
				pg_bar.value = texto_materia.cursor_offset()
				if texto_materia.cursor[1] < 5: pass
				elif texto_materia.cursor[1] > 5 and texto_materia.cursor[1] < 10: texto_materia.size_hint_y += .01
				else: pass
		ProgressBar:
			id: pg_bar
			size_hint: 1, .1
			value: 0
			max: texto_materia.width
		Widget:
			size_hint: 1, .1
		BoxLayout:
			size_hint: 1, .1
			Botao:
				text: 'Cancelar'
				cor_fundo: app.color_button
				cor_fundo_pressionado: app.color_button_pressed
				on_release:
					popup.dismiss()
			Botao:
				id: criar
				text: 'Criar'
				cor_fundo: app.color_button
				cor_fundo_pressionado: app.color_button_pressed
				on_release:
					popup.dismiss()
''')
	return popup
	
def popup_editar_materia(nome):
	popup = Builder.load_string(f'''
Popup:
	id: popup
	title: 'Editar Matéria'
	size_hint: .8, .8
	auto_dismiss: False
	BoxLayout:
		orientation: 'vertical'
		TextInput:
			id: texto_materia
			text: '{nome}'
			size_hint: 1, .9
			hint_text: 'Nome da Matéria'
			font_size: app.tam_font
		BoxLayout:
			size_hint: 1, .1
			Botao:
				text: 'Cancelar'
				cor_fundo: app.color_button
				cor_fundo_pressionado: app.color_button_pressed
				on_release:
					popup.dismiss()
			Botao:
				id: editar
				text: 'Editar'
				cor_fundo: app.color_button
				cor_fundo_pressionado: app.color_button_pressed
				on_release:
					popup.dismiss()
''')
	return popup

def popup_excluir_materia(nome):
	popup = Builder.load_string(f'''
Popup:
	id: popup
	title: 'Confirmação de Exclusão'
	size_hint: .8, .8
	auto_dismiss: False
	BoxLayout:
		orientation: 'vertical'
		Label:
			id: texto_materia
			text: 'Tem certeza que deseja excluir a matéria {nome}?'
			size_hint: 1, .9
			font_size: app.tam_font
			text_size: self.size
			valign: 'middle'
			halign: 'center'
		BoxLayout:
			size_hint: 1, .1
			Botao:
				text: 'Não'
				cor_fundo: app.color_button
				cor_fundo_pressionado: app.color_button_pressed
				on_release:
					popup.dismiss()
			Botao:
				id: excluir
				text: 'Sim'
				cor_fundo: app.color_button
				cor_fundo_pressionado: app.color_button_pressed
				on_release:
					popup.dismiss()
''')
	return popup
