from ..asr_abc import ASR


class SenseVoice(ASR):
    def __init__(self):
        super().__init__()

    def transcribe(self, audio_file_bytes, language):
        return {'text': 'This is sensevoice'}
    
    def supported_languages(self):
        return ['auto', 'zh', 'yue', 'en']