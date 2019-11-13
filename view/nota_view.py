from kivy.uix.screenmanager import Screen

class Nota(Screen):
	def __init__(self, **kwargs):
		super(Nota, self).__init__(**kwargs)
	
	def calcular_media(self, quantidade_perguntas, pontos_totais):
		erros = pontos_totais['erros']
		acertos = pontos_totais['acertos']
		nao_respondidas = pontos_totais['nao_respondidas']
		media = (acertos / quantidade_perguntas) * 10
		
		self.ids.erros.text = str(erros)
		self.ids.acertos.text = str(acertos)
		self.ids.nao_respondidas.text = str(nao_respondidas)
		self.ids.media.text = f'{media:.2f}'
