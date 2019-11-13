  # https://mindminers.com/blog/tipos-de-perguntas-usados-em-questionarios/

import os, json
#os.environ['KIVY_AUDIO'] = 'ffpyplayer'
#os.environ['KIVY_VIDEO'] = 'ffpyplayer'
#os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

from kivy.uix.screenmanager import ScreenManager, SlideTransition, NoTransition
#from kivy.core.window import Window
#Window.size = (400, 600)

#from kivy.loader import Loader
#from kivy.core.asyncimage import AsyncImage
#Loader.loading_image = AsyncImage('./img/image.gif')

from kivy.storage.jsonstore import JsonStore

from conf import *
from widgets_personalizados import RippleButton, ToggleCheckBox, Toast

from dao import materias_dao
from dao import perguntas_dao
from dao import estudar_dao

from model import materias_model
from model import perguntas_model
from model import estudar_model

from controller import materias_controller
from controller import perguntas_controller
from controller import estudar_controller

from view.inicio_view import Inicio
from view.materias_view import Materias
from view.perguntas_view import Perguntas
from view.estudar_view import Estudar
from view.sobre_view import Sobre
from view.configuracao_view import Configuracao
from view.baixar_view import Baixar
from view.prova_view import Prova
from view.resultado_view import Resultado
from view.comentario_view import Comentario
from view.nota_view import Nota

for kvfile in ['widgets_personalizados.kv', 'view/inicio_view.kv', 
'view/estudar_view.kv', 'view/materias_view.kv', 'view/perguntas_view.kv', 
'view/configuracao_view.kv', 'view/sobre_view.kv', 'view/baixar_view.kv',
'view/prova_view.kv','view/resultado_view.kv', 'view/comentario_view.kv',
'view/nota_view.kv']:
	with open(kvfile, encoding='utf8') as f:
		Builder.load_string(f.read())

def criar_abrir_arquivo(caminho):
	bd = JsonStore(caminho, indent=4, sort_keys=False)
	return bd

#from jnius import autoclass
from kivy.utils import platform

if platform=="android": print('hello android')
else: print(f'hello {platform}')

class MyApp(App):
	title = "Projeto Saber"
	icon = ICON
	screen_manager = ObjectProperty()
	bd = criar_abrir_arquivo('./config.json')
	modo = bd['modo']['modo']
	switch = True if modo == 'noite' else False
	configuracoes = bd['modo']['configuracoes']

	def open_settings(self, *largs): pass # EVITA ABRIR O MENU DE CONFIGURAÇÃO COM O F1

	def __init__(self, **kwargs):
		super(MyApp, self).__init__(**kwargs)

	def recreate(self):	
		self.bd = criar_abrir_arquivo('./config.json')
		self.configuracoes = self.bd['modo']['configuracoes']
		self.color_background1 =  self.configuracoes['color_background1']
		self.color_background2 = self.configuracoes['color_background2']
		self.color_font = self.configuracoes['color_font']
		self.color_button = self.configuracoes['color_button']
		self.color_button_pressed = self.configuracoes['color_button_pressed']
		self.color_button_pressed2 = self.configuracoes['color_button_pressed2']
		self.color_menubar = self.configuracoes['color_menubar']
		self.color_container = self.configuracoes['color_container']
		self.color_caixa_pergunta = self.configuracoes['color_caixa_pergunta']
		self.color_caixa_resposta = self.configuracoes['color_caixa_resposta']
		self.toast_color = self.configuracoes['toast_color']
		self.tam_font = self.configuracoes['font_size']

		'''
		from kivy.base import stopTouchApp, EventLoop
		app = App.get_running_app()
		self.screen_manager.clear_widgets()
		EventLoop.window.canvas.clear()
		root = app.build()
		EventLoop.window.add_widget(root)

		self.screen_manager.transition = NoTransition()
		self.screen_manager.current = 'configuracao'
		self.screen_manager.transition = SlideTransition()
		'''

	def build(self):
		self.color_background1 =  self.configuracoes['color_background1']
		self.color_background2 = self.configuracoes['color_background2']
		self.color_font = self.configuracoes['color_font']
		self.color_button = self.configuracoes['color_button']
		self.color_button_pressed = self.configuracoes['color_button_pressed']
		self.color_button_pressed2 = self.configuracoes['color_button_pressed2']
		self.color_menubar = self.configuracoes['color_menubar']
		self.color_container = self.configuracoes['color_container']
		self.color_caixa_pergunta = self.configuracoes['color_caixa_pergunta']
		self.color_caixa_resposta = self.configuracoes['color_caixa_resposta']
		self.toast_color = self.configuracoes['toast_color']
		self.tam_font = self.configuracoes['font_size']

		self.screen_manager = ScreenManager()

		self.screen_manager.add_widget(Inicio(name = "inicio"))
		self.screen_manager.add_widget(Materias(name = "materias"))
		self.screen_manager.add_widget(Perguntas(name = "perguntas"))
		self.screen_manager.add_widget(Configuracao(name = "configuracao"))
		self.screen_manager.add_widget(Sobre(name = "sobre"))
		self.screen_manager.add_widget(Estudar(name = "estudar"))
		self.screen_manager.add_widget(Baixar(name = "baixar"))
		self.screen_manager.add_widget(Prova(name = "prova"))
		self.screen_manager.add_widget(Resultado(name = "resultado"))
		self.screen_manager.add_widget(Comentario(name = "comentario"))
		self.screen_manager.add_widget(Nota(name = "nota"))

		return self.screen_manager

	def salvar_configuracoes(self):
		modo = 'noite' if self.switch == True else 'dia'
		configuracoes = {
			'color_background1': self.color_background1,
			'color_background2': self.color_background2, 
			'color_font': self.color_font,
			'color_button': self.color_button, 
			'color_button_pressed': self.color_button_pressed,
			'color_button_pressed2': self.color_button_pressed2,
			'color_menubar': self.color_menubar,
			'color_container': self.color_container,
			'color_caixa_pergunta': self.color_caixa_pergunta,
			'color_caixa_resposta': self.color_caixa_resposta,
			'toast_color': self.toast_color,
			'font_size': self.tam_font
		}
		self.bd.put('modo', modo = self.modo, configuracoes = configuracoes)
		self.recreate()

	def change_color(self):

		quase_branco = (0.9254901960784314, 0.9411764705882353, 0.9450980392156862, 1)
		cinza_claro = (0.751, 0.751, 0.751, 1)
		cinza_escuro = (0.451, 0.451, 0.451, 1)

		azul_escuro = (0.17254901960784313, 0.24313725490196078, 0.3137254901960784, 1)
		azul_escuro2 = (0.2117647058823529, 0.4235294117647058, 0.5215686274509803,1)
		azul_escuro3 = (0.20392156862745098, 0.596078431372549, 0.8588235294117647, 1)
		azul_escuro4 = (0.1607843137254902, 0.5019607843137255, 0.7254901960784313, 1)

		azul_claro1 = (0.19215686274509805, 0.9098039215686274, 0.9098039215686274, 1)
		azul_claro2 = (0.19215686274509805, 0.7764705882352941, 0.9098039215686274, 1)
		azul_claro3 = (0.4117647058823529,0.8235294117647058,0.9215686274509803,1)

		verde_claro1 = (0.19215686274509805, 0.9098039215686274, 0.6235294117647059, 1)
		verde_claro2 = (0.2549019607843137,0.9098039215686274,0.7098039215686275,1)
		verde_claro3 = (0.1803921568627451, 0.8, 0.44313725490196076, 1)

		verde_escuro1 = (0.08627450980392157, 0.6274509803921569, 0.5215686274509804,1)
		verde_escuro2 = (0.15294117647058825, 0.6823529411764706, 0.3764705882352941, 1)

		if self.switch:
			self.modo = 'noite'
			self.color_background1 = azul_escuro
			self.color_background2 = verde_escuro2
			self.color_font = quase_branco
			self.color_button = azul_escuro
			self.color_button_pressed = azul_escuro3
			self.color_button_pressed2 = azul_escuro3
			self.color_container = 0,0,0,0
			self.color_caixa_pergunta = azul_escuro4
			self.color_caixa_resposta = azul_escuro3
			self.toast_color = azul_escuro2
			self.tam_font = 30
		else:
			self.modo = 'dia'
			self.color_background1 = azul_claro2
			self.color_background2 = verde_claro2
			self.color_font = quase_branco
			self.color_button = azul_claro3
			self.color_button_pressed = azul_claro1
			self.color_button_pressed2 = azul_claro1
			self.color_container = 0,0,0,0
			self.color_caixa_pergunta = verde_claro3
			self.color_caixa_resposta = verde_claro2
			self.toast_color = azul_escuro
			self.tam_font = 30

	def on_start(self):
		pass

	def on_pause(self):
		return True

	def on_resume(self):
		pass
        
	def change_size_window(self, ativado, width, height):
		pass
		#Window.size = (400, 600) if ativado == True else (800, 600)

if __name__ == '__main__':
	MyApp().run()
