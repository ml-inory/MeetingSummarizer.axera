from abc import ABC, abstractmethod
from typing import List


class ASR(ABC):
    @abstractmethod
    def transcribe(self, audio_file_bytes, language) -> dict:
        """Implementation of transcription"""
        """Return {'text': asr result, 'timestamp': optional}"""
        pass

    @abstractmethod
    def supported_languages(self) -> List[str]:
        pass
    