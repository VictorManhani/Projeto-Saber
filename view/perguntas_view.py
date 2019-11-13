from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

from model import perguntas_model
from controller import perguntas_controller
import os

class Perguntas(Screen):
	perguntas = {}
	perguntas_ids = {}
	ids_dinamicos = {}
	materia_atual = ''
	
	def __init__(self, **kwargs):
		super(Perguntas, self).__init__(**kwargs)

	def carregar_perguntas(self, materia_atual):
		self.perguntas, self.materia_atual = perguntas_controller.carregar_perguntas(
			self.ids.container, materia_atual,
			self.materia_atual, self.perguntas_ids,
			self.perguntas
		)
		
	def criar_pergunta_nova(self):
		perguntas_disponiveis = perguntas_controller.verifica_perguntas_disponiveis(self.perguntas)
		numero_pergunta = perguntas_disponiveis[0]
		self.perguntas_ids[numero_pergunta] = perguntas_controller.criar_pergunta_nova(self.ids.container, numero_pergunta)
		self.perguntas[numero_pergunta] = []

	def modo_pergunta(self, container, numero_pergunta, modo):
		self.ids_dinamicos = perguntas_controller.modo_pergunta(container, numero_pergunta, modo)

	def salvar_pergunta(self, numero_pergunta):
		container =  self.ids.container # Container que estao todas as perguntas
		container2 = self.perguntas_ids[numero_pergunta] # container da pergunta
		container3 = container2.ids[f'container{numero_pergunta}'] 

		modo = container2.ids[f'modo{numero_pergunta}'].text
		pergunta = self.ids_dinamicos[numero_pergunta][0].text
		
		perguntas_controller.salvar_pergunta(
			container, modo, pergunta, 
			numero_pergunta, self.ids_dinamicos, self.perguntas,
			self.materia_atual, self.perguntas_ids
		)





	def excluir_pergunta(self, nome_pergunta):
		perguntas_controller.excluir_pergunta(self.bd, self.pops, self.perguntas, nome_pergunta, self.ids.container)

	def editar_pergunta(self, nome_pergunta):
		perguntas_controller.editar_pergunta(self.bd, self.pops, self.perguntas, nome_pergunta, self.ids.container)

	def cancelar_pergunta_nova(self):
		pass
		
	def deletar_pergunta(self, numero_pergunta):
		#bd = json_bd.criar_abrir_arquivo('./materias/materias.json')
		#materias = json_bd.obter_todas_materias(bd)
		#materia_atual = self.ids.materia_nome.text
		estrutura.deletar_pergunta(bd, numero_pergunta, self.ids.container, materias, estrutura.atualizar_perguntas)#, self.dynamic_ids)

	def atualizar_perguntas(self):
		materia_atual = self.ids.materia_nome.text
		bd = json_bd.criar_abrir_arquivo('./materias/materias.json')
		materias = json_bd.obter_todas_materias(bd)
		{k:v for k,v in self.perguntas.items() if v}
		{k:v for k,v in self.perguntas_ids.items() if v}
		self.perguntas = materias[materia_atual]
		self.perguntas_ids = estrutura.carregar_pergunta(self.ids.container, materia_atual, materias)
