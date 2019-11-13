# https://stackoverflow.com/questions/23077338/share-image-and-text-through-whatsapp-or-facebook
# https://gist.github.com/kived/0f450e738bf79c003253
# https://stackoverflow.com/questions/31988452/kivy-start-android-intent-with-pre-filled-contact-fields
# https://python4dads.wordpress.com/2014/07/23/kivy-android-intent-filters/
# https://stackoverflow.com/questions/38983649/kivy-android-share-image
# https://stackoverflow.com/questions/26749684/send-email-with-attachment-from-kivy-app-on-android-preferably-by-opening-email
# https://stackoverflow.com/questions/6814268/android-share-on-facebook-twitter-mail-ecc

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

import os

from model import materias_model
from controller import materias_controller

class Materias(Screen):
	caminho = './materias_bd.json'
	bd = materias_model.criar_abrir_arquivo(caminho)
	materias = materias_model.obter_todas_materias(bd)
	pops = []
	
	def __init__(self, **kwargs):
		super(Materias, self).__init__(**kwargs)
		self.carregar_materia()

	def criar_materia(self):
		materias_controller.criar_materia(self.bd, self.pops, self.materias, self.ids.container)

	def excluir_materia(self, nome_materia):
		materias_controller.excluir_materia(self.bd, self.pops, self.materias, nome_materia, self.ids.container)

	def editar_materia(self, nome_materia):
		materias_controller.editar_materia(self.bd, self.pops, self.materias, nome_materia, self.ids.container)
		
	def carregar_materia(self):
		materias_controller.carregar_materia(self.ids.container, self.materias)
	
	def compartilhar_materia(self):
		#materias_controller.compartilhar_materia(self.ids.container, self.materias)
		intent = Intent()
		intent.setAction(Intent.ACTION_SEND)
		intent.putExtra(Intent.EXTRA_TEXT, String('test share text'))
		intent.setType('text/plain')
		chooser = Intent.createChooser(intent, String('Share...'))
		PythonActivity.mActivity.startActivity(chooser)

