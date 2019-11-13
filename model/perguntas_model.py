from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from dao import perguntas_dao

def criar_abrir_arquivo(caminho):
	arquivo = perguntas_dao.criar_abrir_arquivo(caminho)
	return arquivo

def obter_todas_materias(bd):
	materias = perguntas_dao.obter_todas_materias(bd)
	return materias

def carregar_perguntas(container, nome_materia, perguntas):
	container.clear_widgets()
	containers_perguntas = {}
	
	for numero_pergunta, lista_resposta in perguntas[nome_materia].items():
		if lista_resposta[0] == 'padrão':
			alternativas = []
			for i in lista_resposta[2]: alternativas.append(i)
			
			bt = Builder.load_string(f'''
BoxLayout:
	id: box{numero_pergunta}
	orientation: 'vertical'
	size_hint: 1, None
	height: cabecalho{numero_pergunta}.height + bl{numero_pergunta}.height
	BoxLayout:
		id: cabecalho{numero_pergunta}
		size_hint: 1, None
		height: dp('50')
		ToggleBotao:
			id: tg{numero_pergunta}
			text: "{numero_pergunta}"
			font_size: app.tam_font
			size_hint: .7, 1
			on_state:
				bl{numero_pergunta}.opacity = 0 if tg{numero_pergunta}.state == 'normal' else 1
				bl{numero_pergunta}.height = 0 if tg{numero_pergunta}.state == 'normal' else 200
		SpinnerBotao:
			id: opcao{numero_pergunta}
			text: '...'
			values: "Editar", "Excluir"
			font_size: app.tam_font
			size_hint: .3, 1
			option_cls: "MySpinnerOption2"
			on_text:
				print(self.text, tg{numero_pergunta}.state)
				self.text = '...'
	BoxLayout:
		id: bl{numero_pergunta}
		size_hint: 1, None
		height: 0
		opacity: 0
		orientation: 'vertical'
		canvas.before:
			Color:
				rgba: app.color_container
			Rectangle:
				size: self.size
				pos: self.pos
		LabelPergunta:
			id: pergunta{numero_pergunta}
			text: '{lista_resposta[1]}'
			font_size: app.tam_font
			text_size: self.size
			valign: 'middle'
			halign: 'center'
		SpinnerBotao:
			id: resposta{numero_pergunta}
			text: '{lista_resposta[3]}'
			values: {alternativas}
			font_size: app.tam_font
			size_hint: 1, .3
			option_cls: "MySpinnerOption2"
''')
		elif lista_resposta[0] == 'alternativa':
			alternativas = []
			for i in lista_resposta[2][0]: alternativas.append(lista_resposta[2][0][i])
			bt = Builder.load_string(f'''
BoxLayout:
	id: box{numero_pergunta}
	orientation: 'vertical'
	size_hint: 1, None
	height: cabecalho{numero_pergunta}.height + bl{numero_pergunta}.height
	BoxLayout:
		id: cabecalho{numero_pergunta}
		size_hint: 1, None
		height: dp('50')
		ToggleBotao:
			id: tg{numero_pergunta}
			text: "{numero_pergunta}"
			font_size: app.tam_font
			size_hint: .7, 1
			on_state:
				bl{numero_pergunta}.opacity = 0 if tg{numero_pergunta}.state == 'normal' else 1
				bl{numero_pergunta}.height = 0 if tg{numero_pergunta}.state == 'normal' else 200
		SpinnerBotao:
			id: opcao{numero_pergunta}
			text: '...'
			values: "Editar", "Excluir"
			font_size: app.tam_font
			size_hint: .3, 1
			option_cls: "MySpinnerOption2"
			on_text:
				print(self.text, tg{numero_pergunta}.state)
				self.text = '...'
	BoxLayout:
		id: bl{numero_pergunta}
		size_hint: 1, None
		height: 0
		opacity: 0
		orientation: 'vertical'
		canvas.before:
			Color:
				rgba: app.color_container
			Rectangle:
				size: self.size
				pos: self.pos
		LabelPergunta:
			id: pergunta{numero_pergunta}
			text: '{lista_resposta[1]}'
			font_size: app.tam_font
			text_size: self.size
			valign: 'middle'
			halign: 'center'
		SpinnerBotao:
			id: resposta{numero_pergunta}
			text: '{lista_resposta[2][0][lista_resposta[3]]}'
			values: {alternativas}
			font_size: app.tam_font
			size_hint: 1, .3
			option_cls: "MySpinnerOption2"
''')
		elif lista_resposta[0] == 'dissertativa':
			bt = Builder.load_string(f'''
BoxLayout:
	id: box{numero_pergunta}
	orientation: 'vertical'
	size_hint: 1, None
	height: cabecalho{numero_pergunta}.height + bl{numero_pergunta}.height
	BoxLayout:
		id: cabecalho{numero_pergunta}
		size_hint: 1, None
		height: dp('50')
		ToggleBotao:
			id: tg{numero_pergunta}
			text: "{numero_pergunta}"
			font_size: app.tam_font
			size_hint: .7, 1
			on_state:
				bl{numero_pergunta}.opacity = 0 if tg{numero_pergunta}.state == 'normal' else 1
				bl{numero_pergunta}.height = 0 if tg{numero_pergunta}.state == 'normal' else 200
		SpinnerBotao:
			id: opcao{numero_pergunta}
			text: '...'
			values: "Editar", "Excluir"
			font_size: app.tam_font
			size_hint: .3, 1
			option_cls: "MySpinnerOption2"
			on_text:
				print(self.text, tg{numero_pergunta}.state)
				self.text = '...'
	BoxLayout:
		id: bl{numero_pergunta}
		size_hint: 1, None
		height: 0
		opacity: 0
		orientation: 'vertical'
		canvas.before:
			Color:
				rgba: app.color_container
			Rectangle:
				size: self.size
				pos: self.pos
		MeuLabel:
			id: pergunta{numero_pergunta}
			text: '{lista_resposta[1]}'
			font_size: app.tam_font
			text_size: self.size
			cor_fundo: app.color_caixa_pergunta
		ScrollableLabel:
			id: resposta{numero_pergunta}
			text: '{lista_resposta[3]}'
			font_size: app.tam_font
			text_size: self.size
			cor_fundo: app.color_caixa_resposta
''')
		container.add_widget(bt)
		containers_perguntas[numero_pergunta] = bt
	return containers_perguntas

def criar_pergunta_nova(container, numero_pergunta):
	bt = Builder.load_string(f'''
BoxLayout:
	id: box{numero_pergunta}
	orientation: 'vertical'
	size_hint: 1, None
	height: tg{numero_pergunta}.height + bl{numero_pergunta}.height
	ToggleBotao:
		id: tg{numero_pergunta}
		text: "{numero_pergunta}"
		size_hint: 1, None
		height: dp('50')
		font_size: app.tam_font
	BoxLayout:
		id: bl{numero_pergunta}
		orientation: 'vertical'
		size_hint: 1, None
		opacity: 0 if tg{numero_pergunta}.state == 'normal' else 1
		height: 0 if tg{numero_pergunta}.state == 'normal' else dp('450')
		spacing: dp('5')
		padding: dp('5')
		canvas.before:
			Color:
				rgba: app.color_caixa_pergunta
			Rectangle:
				size: self.size
				pos: self.pos
		SpinnerBotao:
			id: modo{numero_pergunta}
			text: 'Selecione Modo'
			values: "padrão", "alternativa", "dissertativa"
			option_cls: "MySpinnerOption"
			size_hint: 1, .1
			on_text:
				app.screen_manager.get_screen("perguntas").modo_pergunta(container{numero_pergunta}, '{numero_pergunta}', modo{numero_pergunta}.text)
		BoxLayout:
			id: container{numero_pergunta}
			orientation: 'vertical'
			size_hint: 1, .9
			spacing: dp('5')
			padding: dp('5')
''')
	container.add_widget(bt)
	return bt

def modo_padrao(numero_pergunta):
	pergunta = Builder.load_string(f'''
Texto:
	id: pergunta{numero_pergunta}
	size_hint: 1, .6
	font_size: app.tam_font
	multiline: True
	text: 'Açaí é bom?'
	hint_text: 'Pergunta'
''')
	modos = Builder.load_string(f'''
BoxLayout:
	size_hint: 1, .2
	spacing: dp('5')
	ToggleCheckBox:
		id: resposta_nao{numero_pergunta}
		group: 'resposta_padrao'
		text: 'Não'
		font_size: app.tam_font
	ToggleCheckBox:
		id: resposta_sim{numero_pergunta}
		group: 'resposta_padrao'
		text: 'Sim'
		font_size: app.tam_font
''')
	return pergunta, modos

def modo_alternativa(numero_pergunta):
	pergunta = Builder.load_string(f'''
TextInput:
	id: pergunta{numero_pergunta}
	text: 'Como se deve comer uma sopa?'
	size_hint: 1, .4
	font_size: app.tam_font
	multiline: True
''')
	modos = Builder.load_string(f'''
BoxLayout:
	id: alternativa{numero_pergunta}
	size_hint: 1, .4
	spacing: dp('5')
	orientation: 'vertical'
	BoxLayout:
		spacing: dp('5')
		ToggleCheckBox:
			id: respostaA{numero_pergunta}
			group: 'resposta_alternativa'
			size_hint: .2, 1
			text: 'A'
			font_size: app.tam_font
		Texto:
			id: textoA{numero_pergunta}
			text: 'Com garfo.'
			font_size: app.tam_font
	BoxLayout:
		spacing: dp('5')
		ToggleCheckBox:
			id: respostaB{numero_pergunta}
			group: 'resposta_alternativa'
			size_hint: .2, 1
			text: 'B'
			font_size: app.tam_font
		Texto:
			id: textoB{numero_pergunta}
			text: 'Com colher.'
			font_size: app.tam_font
	BoxLayout:
		spacing: dp('5')
		ToggleCheckBox:
			id: respostaC{numero_pergunta}
			group: 'resposta_alternativa'
			size_hint: .2, 1
			text: 'C'
			font_size: app.tam_font
		Texto:
			id: textoC{numero_pergunta}
			text: 'Com foice.'
			font_size: app.tam_font
''')
	return pergunta, modos

def modo_dissertativa(numero_pergunta):
	pergunta = Builder.load_string(f'''
Texto:
	id: pergunta{numero_pergunta}
	text_hint: 'Pergunta'
	size_hint: 1, .4
	font_size: app.tam_font
	multiline: True
	text: 'Como se escreve vida em inglês?'
''')
	modos = Builder.load_string(f'''
Texto:
	id: texto{numero_pergunta}
	text: 'Açaí'
	text_hint: 'Resposta'
	size_hint: 1, .4
	font_size: app.tam_font
	multiline: True
''')
	return pergunta, modos

def criar_modo_novo(container, numero_pergunta, pergunta, modos):
	container.add_widget(pergunta)
	container.add_widget(modos)
	container.add_widget(Builder.load_string(f'''
BoxLayout:
	size_hint: 1, .2
	spacing: dp('5')
	Botao:
		text: 'Cancelar'
		cor_fundo: app.color_button
		cor_fundo_pressionado: app.color_button_pressed
		on_release:
			nome_materia = root.parent.parent.parent.parent.parent.parent.parent.parent.materia_atual
			root.parent.parent.parent.parent.parent.parent.parent.parent.carregar_perguntas(nome_materia)
	Botao:
		text: 'Salvar'
		cor_fundo: app.color_button
		cor_fundo_pressionado: app.color_button_pressed
		on_release:
			app.screen_manager.get_screen("perguntas").salvar_pergunta('{numero_pergunta}')
'''))

def salvar_pergunta(bd, materia_atual, perguntas):
	resultado = perguntas_dao.salvar_pergunta(bd, materia_atual, perguntas)
	return resultado

def excluir_pergunta(bd, nome_pergunta):
	resultado = perguntas_dao.excluir_pergunta(bd, nome_pergunta)
	return resultado

def editar_pergunta():
	self.perguntas = {}

def criar_pergunta(container, nome_pergunta, bd):
	pass

def carregar_pergunta(container, perguntas):
	container.clear_widgets()
	for nome_pergunta in perguntas.keys():
		pergunta = Builder.load_string(f'''
BoxLayout:
	id: box
	size_hint: 1, None
	height: dp('60')
	Botao:
		text: "{nome_pergunta}"
		size_hint: .7, 1
		cor_fundo: app.color_button
		cor_fundo_pressionado: app.color_button_pressed
		on_release:
			app.screen_manager.current = "perguntas"
			app.screen_manager.transition.direction = "left"
			app.screen_manager.get_screen("perguntas").ids.pergunta_nome.text = "{nome_pergunta}"
			app.screen_manager.get_screen("perguntas").carregar_perguntas("{nome_pergunta}", {perguntas})
	SpinnerBotao:
		text: '...'
		values: "Editar", "Excluir"
		font_size: app.tam_font
		size_hint: .3, 1
		option_cls: "MySpinnerOption"
		on_text:
			if self.text == "Editar": app.screen_manager.get_screen("perguntas").editar_pergunta("{nome_pergunta}")
			elif self.text == "Excluir": app.screen_manager.get_screen("perguntas").excluir_pergunta("{nome_pergunta}")
			self.text = '...'
''')
		container.add_widget(pergunta)

def popup_criar_pergunta():
	popup = Builder.load_string('''
Popup:
	id: popup
	title: 'Criar Matéria'
	size_hint: .8, .8
	auto_dismiss: False
	BoxLayout:
		orientation: 'vertical'
		TextInput:
			id: texto_pergunta
			size_hint: 1, .7
			hint_text: 'Nome da Matéria'
			font_size: app.tam_font
			on_text:
				pg_bar.value = texto_pergunta.cursor_offset()
				if texto_pergunta.cursor[1] < 5: pass
				elif texto_pergunta.cursor[1] > 5 and texto_pergunta.cursor[1] < 10: texto_pergunta.size_hint_y += .01
				else: pass
		ProgressBar:
			id: pg_bar
			size_hint: 1, .1
			value: 0
			max: texto_pergunta.width
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
	
def popup_editar_pergunta(nome):
	popup = Builder.load_string(f'''
Popup:
	id: popup
	title: 'Editar Matéria'
	size_hint: .8, .8
	auto_dismiss: False
	BoxLayout:
		orientation: 'vertical'
		TextInput:
			id: texto_pergunta
			text: '{nome}'
			size_hint: 1, .9
			hint_text: 'Nome da Matéria'
			font_size: app.tam_font
		BoxLayout:
			size_hint: 1, .1
			Botao:
				cor_fundo: app.color_button
				cor_fundo_pressionado: app.color_button_pressed
				text: 'Cancelar'
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

def popup_excluir_pergunta(nome):
	popup = Builder.load_string(f'''
Popup:
	id: popup
	title: 'Confirmação de Exclusão'
	size_hint: .8, .8
	auto_dismiss: False
	BoxLayout:
		orientation: 'vertical'
		Label:
			id: texto_pergunta
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

# PERGUNTAS UTILS
# recebe as perguntas e retorna uma lista com os nomes das perguntas
def obter_nome_perguntas(perguntas):
	nome_perguntas = []
	for i in perguntas.keys():
		nome_perguntas.append(i)
	return nome_perguntas

# recebe uma lista de perguntas e retorna a quantidade
def quantidade_de_perguntas(perguntas):
	return len(perguntas)

# retorna os slots de perguntas disponíveis
def verifica_perguntas_disponiveis(perguntas):
	nomes = obter_nome_perguntas(perguntas)
	quantidade = quantidade_de_perguntas(nomes)
	nomes_disponiveis = []
	
	for i in range(1, (quantidade+1), 1):
		if nomes[i-1] != f'Pergunta{i}':
			nomes_disponiveis.append(f'Pergunta{i}')
	
	# Se não tiver nenhuma pergunta e os nomes disponiveis for vazio
	# então atribuir a pergunta 1 ao nome disponível
	if quantidade == 0 and nomes_disponiveis == []:
		nomes_disponiveis = ['Pergunta1']
	# Se tiver alguma pergunta e os nomes disponiveis for vazio
	# então atribuir a pergunta de proximo numero ao nome disponível
	elif quantidade > 0 and nomes_disponiveis == []:
		nomes_disponiveis = [f'Pergunta{quantidade+1}']
	# Se tiver perguntas e os nomes disponiveis não forem vazios
	# então atribuir a pergunta um ao nome disponível
	else:
		pass
	return nomes_disponiveis

# PERGUNTAS ESTRUTURA
def deletar_pergunta(bd, numero_pergunta, container, materias, atualizar_perguntas): #, dynamic_ids):
	#bd.deletar_materia(bd, numero_pergunta)
	#container.clear_widgets()
	#{k:v for k,v in dynamic_ids.items() if v}
	#perguntas = materias[materia_atual]
	#atualizar_perguntas(container, banco['iniciais'])
	print('hello')
	
def editar_pergunta(self):
	self.perguntas = {}

def excluir_pergunta(self):
	self.perguntas = {}
