import os
import threading
import requests
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform

KV = r"""
<CherryRoot>:
    orientation: "vertical"
    padding: "18dp"
    spacing: "12dp"
    canvas.before:
        Color:
            rgba: (0.12, 0.045, 0.14, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        text: "[b]🍒 CHERRY AI[/b]"
        markup: True
        font_size: "30sp"
        color: (1, .72, .88, 1)
        size_hint_y: None
        height: "62dp"
    Label:
        text: "Your friendly multilingual voice assistant"
        color: (.95, .82, .9, 1)
        size_hint_y: None
        height: "28dp"
    Spinner:
        id: lang
        text: "Tamil"
        values: ["Tamil", "Telugu", "English"]
        size_hint_y: None
        height: "48dp"
        background_color: (.72, .22, .48, 1)
    TextInput:
        id: message
        hint_text: "Type a message for CHERRY AI..."
        multiline: True
        size_hint_y: .32
        background_color: (.19, .10, .20, 1)
        foreground_color: (1, 1, 1, 1)
        cursor_color: (1, .65, .82, 1)
        padding: "12dp"
    TextInput:
        id: key
        hint_text: "Paste your ElevenLabs API key (kept only while app is open)"
        password: True
        multiline: False
        size_hint_y: None
        height: "48dp"
        background_color: (.19, .10, .20, 1)
        foreground_color: (1, 1, 1, 1)
        padding: "12dp"
    TextInput:
        id: voice
        hint_text: "ElevenLabs Voice ID"
        multiline: False
        size_hint_y: None
        height: "48dp"
        background_color: (.19, .10, .20, 1)
        foreground_color: (1, 1, 1, 1)
        padding: "12dp"
    Button:
        text: "Speak with CHERRY AI"
        size_hint_y: None
        height: "54dp"
        background_normal: ""
        background_color: (.82, .22, .52, 1)
        on_release: root.send_message()
    Label:
        id: status
        text: root.status_text
        color: (1, .78, .88, 1)
        text_size: self.width, None
        halign: "center"
    Label:
        text: "Personal testing only. Do not distribute an APK containing your private API key."
        color: (.78, .68, .76, 1)
        font_size: "11sp"
        size_hint_y: None
        height: "36dp"
"""

class CherryRoot(BoxLayout):
    status_text = StringProperty("Choose a language, enter text, and add your voice details.")

    def reply_text(self, text, lang):
        if lang == "Tamil":
            return "நீங்கள் சொன்னது: " + text
        if lang == "Telugu":
            return "మీరు చెప్పింది: " + text
        return "You said: " + text

    def send_message(self):
        text = self.ids.message.text.strip()
        key = self.ids.key.text.strip()
        voice_id = self.ids.voice.text.strip()
        lang = self.ids.lang.text
        if not text:
            self.status_text = "Please type something first."
            return
        if not key or not voice_id:
            self.status_text = "Enter your ElevenLabs API key and Voice ID."
            return
        self.status_text = "CHERRY AI is preparing your voice..."
        threading.Thread(
            target=self._tts_worker,
            args=(text, key, voice_id, lang),
            daemon=True
        ).start()

    def _tts_worker(self, text, key, voice_id, lang):
        codes = {"Tamil": "ta", "Telugu": "te", "English": "en"}
        # Eleven v3 supports multilingual output; access may depend on account.
        url = "https://api.elevenlabs.io/v1/text-to-speech/" + voice_id
        headers = {"xi-api-key": key, "Content-Type": "application/json"}
        payload = {
            "text": text,
            "model_id": "eleven_v3",
            "language_code": codes[lang]
        }
        try:
            response = requests.post(
                url, headers=headers, json=payload,
                params={"output_format": "mp3_22050_32"}, timeout=90
            )
            response.raise_for_status()
            path = os.path.join(App.get_running_app().user_data_dir, "cherry_reply.mp3")
            with open(path, "wb") as f:
                f.write(response.content)
            Clock.schedule_once(lambda dt: self._play_audio(path), 0)
        except Exception as exc:
            msg = "Voice request failed: " + str(exc)[:220]
            Clock.schedule_once(lambda dt: setattr(self, "status_text", msg), 0)

    def _play_audio(self, path):
        try:
            from kivy.core.audio import SoundLoader
            sound = SoundLoader.load(path)
            if sound:
                sound.play()
                self.status_text = "CHERRY AI is speaking."
            else:
                self.status_text = "Audio playback unavailable on this device."
        except Exception as exc:
            self.status_text = "Playback error: " + str(exc)[:180]

class CherryAIApp(App):
    def build(self):
        Builder.load_string(KV)
        return CherryRoot()

if __name__ == "__main__":
    CherryAIApp().run()
