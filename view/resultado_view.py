from kivy.uix.screenmanager import Screen
from kivy.storage.jsonstore import JsonStore
from kivy.lang import Builder
import re, math
from collections import Counter
from difflib import SequenceMatcher

class Resultado(Screen):
	todas_perguntas = {}
	perguntas_respondidas = {}
	perguntas_corrigidas = {}
	respostas_dadas = {}
	pontos_totais = {}
	quantidade_total_perguntas = 0
	
	def __init__(self, **kwargs):
		super(Resultado, self).__init__(**kwargs)

	def checa_similaridade(self, txt1, txt2):
		def distancia_levenshtein(s1, s2):
			if len(s1) > len(s2): s1, s2 = s2, s1
			distancias = range(len(s1) + 1)
			for i2, c2 in enumerate(s2):
				distancias_ = [i2+1]
				for i1, c1 in enumerate(s1):
					if c1 == c2:
						distancias_.append(distancias[i1])
					else:
						distancias_.append(1 + min((distancias[i1], distancias[i1 + 1], distancias_[-1])))
				distancias = distancias_
			return distancias[-1]

		def ferramenta_similaridade(s1, s2):
			def pares_letras(string):
				num_pares, pares = len(string), {}
				for i in range(0, num_pares): pares[i] = string[i:2]
				return pares

			def pares_letras_palavras(string):
				todos_pares = []
				palavras = string.split(' ')
				for w in range(0, len(palavras)):
					if palavras[w] != None and palavras[w] != '':
						pares_em_palavra = pares_letras(palavras[w])
						for p in range(0, len(pares_em_palavra)): todos_pares.append(pares_em_palavra[p])
				return todos_pares

			def compare_strings(str1, str2):
				pares1 = pares_letras_palavras(str1.upper())
				pares2 = pares_letras_palavras(str2.upper())
				interseccao = 0
				uniao = len(pares1) + len(pares2)
				for i in range(0, len(pares1)):
					for j in range(0, len(pares2)):
						if pares1[i] == pares2[j]:
							interseccao += 1
							pares2.pop(j)
							break
				return (2.0 * interseccao) / uniao
			return compare_strings(s1, s2)
 
		def texto_para_vetor(text):
			WORD = re.compile(r'\w+')
			words = WORD.findall(text)
			return Counter(words)
	
		def cosine(t1, t2): 
			vec1 = texto_para_vetor(t1)
			vec2 = texto_para_vetor(t2)
			intersection = set(vec1.keys()) & set(vec2.keys())
			numerator = sum([vec1[x] * vec2[x] for x in intersection])
			sum1 = sum([vec1[x]**2 for x in vec1.keys()])
			sum2 = sum([vec2[x]**2 for x in vec2.keys()])
			denominator = math.sqrt(sum1) * math.sqrt(sum2)
			if not denominator:
			   return 0.0
			else:
			   return float(numerator) / denominator

		def jaccard(t1, t2):  
			vec1 = texto_para_vetor(t1)
			vec2 = texto_para_vetor(t2)
			numerator = len(set(vec1.keys()).intersection(set(vec2.keys())))
			denominator = float(len(set(vec1.keys())) + len(set(vec2.keys())) -numerator)
			if not denominator: return 0.0
			else: return float(numerator) / denominator
			
		def sim_min_edit(s1, s2):
			dict1 = texto_para_vetor(s1)
			dict2 = texto_para_vetor(s2)
			dict_diff_1_2 = {k : dict2[k] for k in set(dict2) - set(dict1)}
			dict_diff_2_1 = {k : dict1[k] for k in set(dict1) - set(dict2)}
			dict_comm_1_2 = {k : abs(dict2[k] - dict1[k]) for k in set(dict2).intersection(set(dict1))}
			numerator = sum(dict_diff_1_2.values()) + sum(dict_diff_2_1.values()) + sum(dict_comm_1_2.values())
			denominator = sum(dict1.values()) + sum(dict2.values())
			if not denominator: return 0.0
			else: return 1 - (float(numerator) / denominator)
	
		def string_similar(a, b):
			ratio = SequenceMatcher(None, a, b).ratio()
			return ratio
		
		ponto = 0.0
		dl = distancia_levenshtein(txt1, txt2)
		fs = ferramenta_similaridade(txt1, txt2)
		c = cosine(txt1, txt2)
		j = jaccard(txt1, txt2)
		s = sim_min_edit(txt1, txt2)
		ss = string_similar(txt1, txt2)
		
		if dl < 30: ponto += 1.6666
		if fs > 0.6: ponto += 1.6666
		if c > 0.6: ponto += 1.6666
		if j > 0.6: ponto += 1.6666
		if s > 0.6: ponto += 1.6666
		if ss > 0.6: ponto += 1.6666
		return ponto

	def corrigir(self, perguntas_respondidas, todas_perguntas):
		perguntas_corrigidas = {}
		acertos, erros = 0, 0
		self.pontos_totais['erros'] = 0
		self.pontos_totais['acertos'] = 0
		self.pontos_totais['nao_respondidas'] = 0
		
		for numero_pergunta in perguntas_respondidas.keys():
			if todas_perguntas[numero_pergunta][0] == 'padrão':
				nao_botao = perguntas_respondidas[numero_pergunta].ids[f'resposta_nao{numero_pergunta}'].state
				sim_botao = perguntas_respondidas[numero_pergunta].ids[f'resposta_sim{numero_pergunta}'].state
				resposta_correta = todas_perguntas[numero_pergunta][3]
				resposta_dada = ''

				if nao_botao == 'down' and sim_botao == 'normal':
					resposta_dada = 'nao'
				elif nao_botao == 'normal' and sim_botao == 'down':
					resposta_dada = 'sim'
	
			elif todas_perguntas[numero_pergunta][0] == 'alternativa':
				a_botao = perguntas_respondidas[numero_pergunta].ids[f'respostaA{numero_pergunta}'].state
				b_botao = perguntas_respondidas[numero_pergunta].ids[f'respostaB{numero_pergunta}'].state
				c_botao = perguntas_respondidas[numero_pergunta].ids[f'respostaC{numero_pergunta}'].state
				resposta_correta = todas_perguntas[numero_pergunta][3]
				resposta_dada = ''
				
				if a_botao == 'down' and b_botao == 'normal' and c_botao == 'normal':
					resposta_dada = 'A'
				elif a_botao == 'normal' and b_botao == 'down' and c_botao == 'normal':
					resposta_dada = 'B'
				elif a_botao == 'normal' and b_botao == 'normal' and c_botao == 'down':
					resposta_dada = 'C'
			
			elif todas_perguntas[numero_pergunta][0] == 'dissertativa':
				texto_resposta = perguntas_respondidas[numero_pergunta].ids[f'resposta{numero_pergunta}']
				resposta_correta = todas_perguntas[numero_pergunta][3]
				resposta_dada = texto_resposta.text
			
			if todas_perguntas[numero_pergunta][0] == 'dissertativa':
				pontos = self.checa_similaridade(resposta_correta, resposta_dada)
				if resposta_dada == '':
					perguntas_corrigidas[numero_pergunta] = ''
					self.pontos_totais['nao_respondidas'] += 1
				elif pontos >= 6.0:
					acertos += 1
					perguntas_corrigidas[numero_pergunta] = 'certo'
					self.pontos_totais['acertos'] += pontos
				elif pontos < 4.0:
					erros += 1
					perguntas_corrigidas[numero_pergunta] = 'errado'
					self.pontos_totais['erros'] += pontos
			else:
				if resposta_dada == '':
					perguntas_corrigidas[numero_pergunta] = ''
					self.pontos_totais['nao_respondidas'] += 1
				else:
					if resposta_dada == resposta_correta:
						acertos += 1
						perguntas_corrigidas[numero_pergunta] = 'certo'
						self.pontos_totais['acertos'] += 1
					else:
						erros += 1
						perguntas_corrigidas[numero_pergunta] = 'errado'
						self.pontos_totais['erros'] += 1

			self.respostas_dadas[numero_pergunta] = resposta_dada
		return erros, acertos, perguntas_corrigidas

	def resultado(self, todas_perguntas):
		container = self.ids.container
		container.clear_widgets()
		self.respostas_dadas = {}
		self.todas_perguntas = {}
		self.perguntas_respondidas = {}
		self.perguntas_corrigidas = {}

		perguntas_respondidas = self.parent.get_screen('prova').perguntas
		self.quantidade_total_perguntas = len(perguntas_respondidas.keys())
		erros, acertos, perguntas_corrigidas = self.corrigir(perguntas_respondidas, todas_perguntas)

		self.perguntas_respondidas = perguntas_respondidas
		self.perguntas_corrigidas = perguntas_corrigidas
		self.todas_perguntas = todas_perguntas
		
		container.add_widget(Builder.load_string(f'''
MeuLabel:
	text: 'Erradas - {erros}'
	size_hint: 1, None
	height: dp('50')
	cor_fundo: [.4,0,0,1]
'''))

		for numero_pergunta in perguntas_corrigidas.keys():
			if perguntas_corrigidas[numero_pergunta] == 'errado':
				pergunta = Builder.load_string(f'''
Botao:
	text: "{numero_pergunta}"
	size_hint: 1, None
	height: dp('50')
	cor_fundo: [.6,0,0,1]
	cor_fundo_pressed: [.4,0,0,1]
	on_release:
		app.screen_manager.current = 'comentario'
		app.screen_manager.transition.direction = 'left'
		app.screen_manager.get_screen('comentario').carregar_pergunta("{numero_pergunta}", {self.todas_perguntas}, {self.respostas_dadas}, "errado")
''')
				container.add_widget(pergunta)

		container.add_widget(Builder.load_string(f'''
MeuLabel:
	text: 'Corretas - {acertos}'
	size_hint: 1, None
	height: dp('50')
	cor_fundo: [0,.4,0,1]
'''))

		for numero_pergunta in perguntas_corrigidas.keys():
			if perguntas_corrigidas[numero_pergunta] == 'certo':
				pergunta = Builder.load_string(f'''
Botao:
	text: "{numero_pergunta}"
	size_hint: 1, None
	height: dp('50')
	cor_fundo: [0,.6,0,1]
	cor_fundo_pressed: [0,.4,0,1]
	on_release:
		app.screen_manager.current = 'comentario'
		app.screen_manager.transition.direction = 'left'
		app.screen_manager.get_screen('comentario').carregar_pergunta("{numero_pergunta}", {self.todas_perguntas}, {self.respostas_dadas}, "certo")
''')
				container.add_widget(pergunta)
