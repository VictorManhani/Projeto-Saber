from functools import partial
from model import perguntas_model
from widgets_personalizados import Toast

def carregar_perguntas(container, materia_atual, materia_atual2, perguntas_ids, perguntas):
	#if materia_atual == materia_atual2:
	#	return perguntas, materia_atual
	#elif materia_atual != materia_atual2:
	bd = perguntas_model.criar_abrir_arquivo('./materias_bd.json')
	materias = perguntas_model.obter_todas_materias(bd)
	{k:v for k,v in perguntas_ids.items() if v}
	perguntas = materias[materia_atual]
	perguntas_ids = perguntas_model.carregar_perguntas(container, materia_atual, materias)
	return perguntas, materia_atual

def verifica_perguntas_disponiveis(perguntas):
	nomes_disponiveis = perguntas_model.verifica_perguntas_disponiveis(perguntas)
	return nomes_disponiveis

def criar_pergunta_nova(container, numero_pergunta):
	bt = perguntas_model.criar_pergunta_nova(container, numero_pergunta)
	return bt

def modo_pergunta(container, numero_pergunta, modo):
	container.clear_widgets()
	pergunta = None
	
	if modo == 'padrão':
		pergunta, modos = perguntas_model.modo_padrao(numero_pergunta)
	elif modo == 'alternativa':
		pergunta, modos = perguntas_model.modo_alternativa(numero_pergunta)
	elif modo == 'dissertativa':
		pergunta, modos = perguntas_model.modo_dissertativa(numero_pergunta)
		
	perguntas_model.criar_modo_novo(container, numero_pergunta, pergunta, modos)

	return {numero_pergunta:[pergunta, modos]}

def salvar_pergunta(container, modo, pergunta, numero_pergunta, 
	ids_dinamicos, perguntas, materia_atual, perguntas_ids):
	if pergunta != '' and pergunta != None and len(pergunta) > 3:
		if modo == 'padrão':
			nao = ids_dinamicos[numero_pergunta][1].ids[f'resposta_nao{numero_pergunta}']
			sim = ids_dinamicos[numero_pergunta][1].ids[f'resposta_sim{numero_pergunta}']
			if nao.state == 'down': resposta_correta = 'nao'
			elif sim.state == 'down': resposta_correta = 'sim'
			else:
				Toast.show('Selecione Sim ou Não!')
				return
			possibilidades = ['nao', 'sim']
		elif modo == 'alternativa':
			A = ids_dinamicos[numero_pergunta][1].ids[f'respostaA{numero_pergunta}']
			B = ids_dinamicos[numero_pergunta][1].ids[f'respostaB{numero_pergunta}']
			C = ids_dinamicos[numero_pergunta][1].ids[f'respostaC{numero_pergunta}']
			textoA = ids_dinamicos[numero_pergunta][1].ids[f'textoA{numero_pergunta}']
			textoB = ids_dinamicos[numero_pergunta][1].ids[f'textoB{numero_pergunta}']
			textoC = ids_dinamicos[numero_pergunta][1].ids[f'textoC{numero_pergunta}']
			if A.state == 'down': resposta_correta = A.text
			elif B.state == 'down': resposta_correta = B.text
			elif C.state == 'down': resposta_correta = C.text
			else:
				Toast.show('Selecione A, B ou C!')
				return
			possibilidades = [{'A':textoA.text, 'B':textoB.text, 'C':textoC.text}]
		elif modo == 'dissertativa':
			resposta_correta = ids_dinamicos[numero_pergunta][1].text
			if resposta_correta == '':
				Toast.show('Escreva a resposta correta')
				return
			possibilidades = []

		bd = perguntas_model.criar_abrir_arquivo('./materias_bd.json')
		perguntas[numero_pergunta] = [modo, pergunta, possibilidades, resposta_correta]

		if perguntas_model.salvar_pergunta(bd, materia_atual, perguntas):
			carregar_perguntas(container, materia_atual, materia_atual, perguntas_ids, perguntas)
		else: Toast.show('Falha ao salvar no bd')
	else:
		Toast.show('Escreva uma pergunta!')

def editar_funcionalidade(bd, perguntas, pops, nome_pergunta, container, botao):
	pergunta = pops[0].ids.texto_pergunta.text
	perguntas[pergunta] = perguntas[nome_pergunta]
	perguntas_model.salvar_pergunta(bd, pergunta)
	
	perguntas_model.excluir_pergunta(bd, nome_pergunta)
	perguntas.pop(nome_pergunta)
	
	carregar_pergunta(container, perguntas)

def editar_pergunta(bd, pops, perguntas, nome_pergunta, container):
	popup = perguntas_model.popup_editar_pergunta(nome_pergunta)
	popup.ids.editar.bind(on_release = partial(editar_funcionalidade, bd, perguntas, pops, nome_pergunta, container))
	popup.open()
	del pops[:]
	pops.append(popup)

def excluir_pergunta(bd, pops, perguntas, nome_pergunta, container):
	popup = perguntas_model.popup_excluir_pergunta(nome_pergunta)
	popup.ids.excluir.bind(on_release = partial(excluir_funcionalidade, bd, perguntas, nome_pergunta, container))
	popup.open()
	del pops[:]
	pops.append(popup)

def excluir_funcionalidade(bd, perguntas, nome_pergunta, container, botao):
	perguntas_model.excluir_pergunta(bd, nome_pergunta)
	perguntas.pop(nome_pergunta)
	carregar_pergunta(container, perguntas)
