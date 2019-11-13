from kivy.uix.behaviors import TouchRippleBehavior
from kivy.uix.button import Button
from kivy.clock import Clock 
from kivy.properties import AliasProperty, StringProperty, ListProperty
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.checkbox import CheckBox
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.uix.modalview import ModalView
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView

class ScrollableLabel(ScrollView):
	text = StringProperty('')
	cor_fundo = ListProperty([])

class RippleButton(TouchRippleBehavior, Button):
	def on_touch_down(self, touch):
		collide_point = self.collide_point(touch.x, touch.y)
		if collide_point:
			touch.grab(self)
			self.transparency = self.background_color[3]
			self.background_color[3] = 0.5
			self.ripple_show(touch)
			self.dispatch('on_press')
			return True
		return False
	
	def on_touch_up(self, touch):
		if touch.grab_current is self:
			touch.ungrab(self)
			self.ripple_fade()
			
			def defer_release(dt):
				self.background_color[3] = self.transparency
				self.dispatch('on_release')
			Clock.schedule_once(defer_release, 0.1)
			return True
		return False

class Botao(Button):
	cor_fundo_normal = ListProperty([])
	cor_fundo_pressionado = ListProperty([])

class ToggleCheckBox(ToggleButton):
	cor_fundo_normal = ListProperty([])
	cor_fundo_pressionado = ListProperty([])
	
	def _get_active(self):
		return self.state == 'down'
	
	def _set_active(self, value):
		self.state = 'down' if value else 'normal'

	active = AliasProperty(
		_get_active, _set_active, bind=('state', ), cache=True)

	def __init__(self, **kwargs):
		self.fbind('state', self._on_state)
		super(ToggleCheckBox, self).__init__(**kwargs)

	def _on_state(self, instance, value):
		if self.group and self.state == 'down':
			self._release_group(self)
	
	def on_group(self, *largs):
		super(ToggleCheckBox, self).on_group(*largs)
		if self.active:
			self._release_group(self)

class Toast(ModalView):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.size_hint = (None, None)
		self.pos_hint = {"center_x": 0.5, "center_y": 0.1}
		self.background_color = [0, 0, 0, 0]
		self.background = "./img/transparent.png"
		self.opacity = 0
		self.auto_dismiss = True
		self.label_toast = Label(size_hint=(None, None), opacity=0)
		self.label_toast.bind(texture_size=self.label_check_texture_size)
		self.add_widget(self.label_toast)
	
	def label_check_texture_size(self, instance, texture_size):
		texture_width, texture_height = texture_size
		if texture_width > Window.width:
			instance.text_size = (Window.width - dp(10), None)
			instance.texture_update()
			texture_width, texture_height = instance.texture_size
		self.size = (texture_width + 25, texture_height + 25)
	
	def toast(self, text_toast):
		self.label_toast.text = text_toast
		self.open()
	
	def on_open(self):
		self.fade_in()
		Clock.schedule_once(self.fade_out, 2.5)
	
	def fade_in(self):
		Animation(opacity=1, duration=0.4).start(self.label_toast)
		Animation(opacity=1, duration=0.4).start(self)
	
	def fade_out(self, interval):
		Animation(opacity=0, duration=0.4).start(self.label_toast)
		anim_body = Animation(opacity=0, duration=0.4)
		anim_body.bind(on_complete=lambda * x: self.dismiss())
		anim_body.start(self)
	
	def on_touch_down(self, touch):
		if not self.collide_point(*touch.pos):
			if self.auto_dismiss:
				self.dismiss()
				return False
		super(ModalView, self).on_touch_down(touch)
		return True

	def show(text, length_long = False):
		Toast().toast(text)
	
