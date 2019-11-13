from functools import partial
from model import materias_model

def carregar_materia(container, materias):
	materias_model.carregar_materia(container, materias)

def criar_funcionalidade(bd, materias, pops, container, botao):
	materia = pops[0].ids.texto_materia.text
	materias[materia] = {}
	materias_model.salvar_materia(bd, materia, {})
	carregar_materia(container, materias)

def criar_materia(bd, pops, materias, container):
	popup = materias_model.popup_criar_materia()
	popup.ids.criar.bind(on_release=partial(criar_funcionalidade, bd, materias, pops, container))
	popup.open()
	del pops[:]
	pops.append(popup)

def editar_funcionalidade(bd, materias, pops, nome_materia, container, botao):
	materia = pops[0].ids.texto_materia.text
	materias[materia] = materias[nome_materia]
	materias_model.salvar_materia(bd, materia, materias[nome_materia])
	materias_model.excluir_materia(bd, nome_materia)
	materias.pop(nome_materia)
	carregar_materia(container, materias)

def editar_materia(bd, pops, materias, nome_materia, container):
	popup = materias_model.popup_editar_materia(nome_materia)
	popup.ids.editar.bind(on_release = partial(editar_funcionalidade, bd, materias, pops, nome_materia, container))
	popup.open()
	del pops[:]
	pops.append(popup)

def excluir_materia(bd, pops, materias, nome_materia, container):
	popup = materias_model.popup_excluir_materia(nome_materia)
	popup.ids.excluir.bind(on_release = partial(excluir_funcionalidade, bd, materias, nome_materia, container))
	popup.open()
	del pops[:]
	pops.append(popup)

def excluir_funcionalidade(bd, materias, nome_materia, container, botao):
	materias_model.excluir_materia(bd, nome_materia)
	materias.pop(nome_materia)
	carregar_materia(container, materias)
