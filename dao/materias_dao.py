from kivy.storage.jsonstore import JsonStore

def criar_abrir_arquivo(caminho):
	bd = JsonStore(caminho, indent=4, sort_keys=False)
	return bd

def salvar_materia(bd, nome_materia, perguntas):
	dicionario_perguntas = {} if perguntas == None else perguntas
	bd.put(nome_materia, materia=nome_materia, perguntas=dicionario_perguntas)
	return True

def obter_todas_materias(bd):
	chaves = bd.keys()
	materias = [bd.get(i) for i in chaves]
	chaves2 = [i for i in chaves]
	p = dict()
	for i in range(len(chaves)): 
		p[chaves2[i]] = materias[i]['perguntas']
	perguntas = p.copy()
	return perguntas

def obter_materia(bd, nome):
	materia = bd.get(nome)
	return materia

def excluir_materia(bd, nome):
	try: bd.delete(nome)
	except error: return error
	finally: return True

def selecionar_materia(bd, nome):
	for item in bd.find(name='Gabriel'):
		print('tshirtmans index key is', item[0])
		print('his key value pairs are', str(item[1]))

def obter_nome_materias(bd):
	return materias.keys()
