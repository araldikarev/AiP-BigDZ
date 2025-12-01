

class NullPointException(Exception):
    def __init__(self, expression: str = "Не удалось создать точку.", message: str = "Невозможно создать точку из пустого списка."):
        super().__init__(expression, message)

class DimensionMismatchPointException(Exception):
    def __init__(self, expression: str = "Не удалось провести операцию", message: str = "Невозможно провести операцию с векторами разной размерности."):
        super().__init__(expression, message)
