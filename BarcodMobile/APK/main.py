from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.graphics.texture import Texture
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
import cv2


class CameraScreen(Screen):
    def initer(self, camera_id):
        self.camera_id = camera_id
    def on_enter(self, **kwargs):
        super(CameraScreen, self).on_enter(**kwargs)
        self.capture = cv2.VideoCapture(self.camera_id)

        # Проверка, удалась ли инициализация камеры
        if not self.capture.isOpened():
            print("Unable to connect to the camera.")
        else:
            self.capture.set(cv2.CAP_PROP_AUTOFOCUS, 1)
            Clock.schedule_interval(self.update_img, 1.0/30.0)

    def on_leave(self):
        # Вызывается, когда пользователь покидает этот экран
        super(CameraScreen, self).on_leave()
        self.capture.release()

    def update_img(self, dt):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.flip(frame, 0)
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            texture.blit_buffer(frame_rgb.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
            self.ids.image.texture = texture



class StartScreen(Screen):
    def stringer(self):
        camera_id = self.ids.camera_id.text
        print(camera_id)
        App.get_running_app().root.get_screen('Camera').initer(camera_id)

    def integer(self):
        camera_id = int(self.ids.camera_id.text)
        App.get_running_app().root.get_screen('Camera').initer(camera_id)

    def sound_clic(self):
        SoundLoader.load('sound.mp3').play()


class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)
        self.transition = NoTransition()

class Myapp(App):
    def build(self):
        return WindowManager()

if __name__ == '__main__':
	Myapp().run()