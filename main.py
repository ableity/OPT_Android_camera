from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
import time
from os import getcwd

class CameraClick(FloatLayout):
    def __init__(self):
        super(CameraClick, self).__init__()
        self.flag = 0
        self.zoom = 30

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        if self.flag == 0:
            camera = self.ids['camera']
            camera.export_to_png(getcwd()+"/"+"IMG.png")
            print("Captured")

    def showpic(self):
        if self.flag == 0:
            self.ids.led.source = getcwd()+"/"+"IMG.png"
            self.ids.led.reload()
            self.ids.led.size_hint = (2, 2)
            self.flag = 1
            self.ids.camera.play = False
        else:
            self.ids.led.size_hint = (0, 0)
            self.flag = 0
            self.ids.camera.play = True

    def zoomadd(self):
        if self.zoom < 90 and self.flag == 0:
            self.zoom = self.zoom+10
            self.ids.camera.zoom = self.zoom
            #self.ids['camera'].play = True

    def zoomdev(self):
        if self.zoom >= 10 and self.flag==0:
            self.zoom = self.zoom-10
            self.ids.camera.zoom = self.zoom


class TestCamera(App):

    def build(self):
        return CameraClick()


TestCamera().run()
