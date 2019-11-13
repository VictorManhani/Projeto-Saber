from kivy.storage.jsonstore import JsonStore

def criar_abrir_arquivo(caminho):
	bd = JsonStore(caminho, indent=4, sort_keys=False)
	return bd

def obter_todas_materias(bd):
	chaves = bd.keys()
	materias = [bd.get(i) for i in chaves]
	chaves2 = [i for i in chaves]
	p = dict()
	for i in range(len(chaves)): 
		p[chaves2[i]] = materias[i]['perguntas']
	materias = p.copy()
	return materias

def salvar_pergunta(bd, materia_atual, perguntas):
	resultado = bd.put(materia_atual, materia=materia_atual, perguntas=perguntas)
	return resultado

def obter_pergunta(bd, nome):
	pergunta = bd.get(nome)
	return pergunta

def excluir_pergunta(bd, nome):
	try: bd.delete(nome)
	except error: return error
	finally: return True

def selecionar_pergunta(bd, nome):
	for item in bd.find(name='Gabriel'):
		print('tshirtmans index key is', item[0])
		print('his key value pairs are', str(item[1]))

def obter_nome_perguntas(bd):
	return perguntas.keys()
