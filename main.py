from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import mainthread
from textwrap import fill
from gestures4kivy import CommonGestures
from android_permissions import AndroidPermissions
from speech_events import SpeechEvents

# Touch event layout
####################
class TouchBoxLayout(BoxLayout, CommonGestures):

    def cgb_primary(self, touch, focus_x, focus_y):
        App.get_running_app().start_listening()

    def cgb_select(self, touch, focus_x, focus_y, long_press):
        if long_press:
            App.get_running_app().copy_text()
            

class MyApp(App):

    # Layout
    ########
    def build(self):
        layout = TouchBoxLayout(orientation = 'vertical')
        instructions = Label(
            text= 'Tap anywhere to Listen.\nLong Press anywhere to Copy.',
            size_hint = (1.0, 0.1))
        self.status = Label(text = 'Status: Not Listening',
                            size_hint = (1.0, 0.05))
        self.speech = Label(size_hint = (1.0, 0.85))
        layout.add_widget(instructions)
        layout.add_widget(self.status)
        layout.add_widget(self.speech)
        return layout

    # Permissions
    #############
    def on_start(self):
        self.unwrapped = ''
        self.dont_gc = AndroidPermissions(self.create_recognizer)

    # Speech Recognizer
    ###################
    def create_recognizer(self):
        self.dont_gc = None
        self.speech_events = SpeechEvents()
        self.speech_events.create_recognizer(self.recognizer_event_handler)

    @mainthread
    def recognizer_event_handler(self, key, value):
        if key == 'onReadyForSpeech':
            self.status.text = 'Status: Listening.' 
        elif key == 'onBeginningOfSpeech':
            self.status.text = 'Status: Speaker Detected.'
        elif key == 'onEndOfSpeech':
            self.status.text = 'Status: Not Listening.' 
        elif key == 'onError':
            self.status.text = 'Status: ' + value + ' Not Listening.'
        elif key in ['onPartialResults', 'onResults']:
            self.unwrapped = str(value)
            self.speech.text = fill(value, 40)
        elif key in ['onBufferReceived', 'onEvent','onRmsChanged']:
            pass

    # Touch event handlers
    ######################
    def start_listening(self):
        if self.speech_events:
            self.speech.text = ''
            self.unwrapped = ''
            self.speech_events.start_listening()

    def copy_text(self):
        if self.unwrapped:
            self.speech_events.share_text_with_clipboard(self.unwrapped)

MyApp().run()



                         
