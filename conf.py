# Filechooser
# https://stackoverflow.com/questions/43452697/browse-an-image-file-and-display-it-in-a-kivy-window
# https://kivy.org/doc/stable/api-kivy.uix.filechooser.html

# Button
# https://stackoverflow.com/questions/19005182/rounding-button-corners-in-kivy
# https://github.com/kivy/kivy/issues/4263

# Color
# https://stackoverflow.com/questions/39976475/python-kivy-language-color-property
# https://www.materialui.co/flatuicolors

# Spinner
# https://github.com/kivy/kivy/wiki/Styling-a-Spinner-and-SpinnerOption-in-KV
# https://kivy.org/doc/stable/api-kivy.uix.spinner.html

# Barra de Progresso
# https://www.geeksforgeeks.org/python-progress-bar-widget-in-kivy/

# Menubar e ScreenManager
# https://alwaysemmyhope.com/es/python/696837-kivy-with-menubar-python-kivy.html

# Códigos EXIF
# https://www.awaresystems.be/imaging/tiff/tifftags/privateifd/exif.html

# Métrics
# https://kivy.org/doc/stable/api-kivy.metrics.html

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.config import Config
from kivy.metrics import dp, sp
#from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.filechooser import FileChooserIconView
from kivy.properties import ListProperty
from kivy.properties import BooleanProperty
#from kivy.uix.progressbar import ProgressBar 
#from kivy.clock import Clock 
#from kivy.uix.widget import Widget
#import os
#from os import listdir
#from os.path import isfile, join, basename
#import shutil
#from PIL import Image
#from pathlib import Path
#from pytz import timezone
#from datetime import datetime
#import json

#os.environ['KIVY_AUDIO'] = 'ffpyplayer'
#os.environ['KIVY_IMAGE'] = 'img_ffpyplayer'
#os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
#os.environ['KIVY_GRAPHICS'] = 'angle_sdl2'

#Config.read("config.ini")

# VARIAVEIS
SWITCH = BooleanProperty(True)

quase_preto = (0.17254901960784313, 0.24313725490196078, 0.3137254901960784, 1)
quase_branco = (0.9254901960784314, 0.9411764705882353, 0.9450980392156862, 1)
azul_escuro = (0.19215686274509805, 0.7764705882352941, 0.9098039215686274, 1)
azul_claro = (0.19215686274509805, 0.9098039215686274, 0.9098039215686274, 1)
verde_claro = (0.19215686274509805, 0.9098039215686274, 0.6235294117647059, 1)
verde_escuro = (0.15294117647058825, 0.6823529411764706, 0.3764705882352941, 1)

teste = (0.4117647058823529,0.8235294117647058,0.9215686274509803,1)
teste2 = (0.2549019607843137,0.9098039215686274,0.7098039215686275,1)
teste3 = (0.2117647058823529,0.4235294117647058,0.5215686274509803,1)
teste4 = (0.451, 0.451, 0.451, 1)
teste5 = (0.1803921568627451, 0.8, 0.44313725490196076, 1)
teste6 = (0.08627450980392157, 0.6274509803921569, 0.5215686274509804,1)
teste7 = (0.751, 0.751, 0.751, 1)

dia = {
	# BACKGROUND
	'cor_fundo1': teste,
	'cor_fundo2': quase_branco,
	'bg_color_back': quase_branco,
	'bg_color_front': quase_preto,
	
	# FONT
	'fg_color1': quase_preto,

	# BUTTON
	'bt_color': teste2,
	'bt_color_pressed': teste,
	'bt_color_pressed2': teste3,
	
	# MENUBAR
	'menubar_color': teste4,
	
	# PERGUNTA
	'color_container': teste5,
	'color_caixa_pergunta': quase_branco,
	'color_caixa_resposta': teste5,
	'toast_color': teste7
}

noite = {
	# BACKGROUND
	'cor_fundo1': teste6,
	'cor_fundo2': quase_preto,
	'bg_color_back': teste6,
	'bg_color_front': quase_preto,
	
	# FONT
	'fg_color1': quase_branco,
	'fg_color2': quase_preto,
	
	# BUTTON
	'bt_color': azul_escuro,
	'bt_color_pressed': teste,
	'bt_color_pressed2': teste3,
	
	# MENUBAR
	'menubar_color': teste7,
	
	# PERGUNTA
	'color_container': teste5,
	'color_caixa_pergunta': verde_escuro,
	'color_caixa_resposta': verde_escuro,
	'toast_color': teste6
}

# SIZES
font_size = sp('30')

# PATHS
ICON = "./img/logo.png"

