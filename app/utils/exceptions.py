class TokenizerNotFoundException(Exception):
    """Исключение для кейсов когда не обнаружен токенайзер по указанному пути"""


class ModelNotFoundException(Exception):
    """Исключение для кейсов когда не обнаружена модель по указанному пути"""


class ProviderNotFoundException(Exception):
    """Исключение для кейсов когда не обнаружен указанный провайдер"""
