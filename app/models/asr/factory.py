from .asr_abc import ASR

from .sensevoice.sensevoice import SenseVoice


class ASRFactory():

    supported_models = [
        'sensevoice'
    ]

    model_class_map = {
        'sensevoice': SenseVoice
    }

    @staticmethod
    def create(model_type) -> ASR:
        assert model_type in ASRFactory.supported_models, f'Currently support models are: {ASRFactory.supported_models}'

        return ASRFactory.model_class_map[model_type]()