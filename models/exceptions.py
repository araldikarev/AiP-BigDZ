

class NullPointException(Exception):
    def __init__(self, expression: str = "Не удалось создать точку.", message: str = "Невозможно создать точку из пустого списка."):
        super().__init__(expression, message)

class DimensionMismatchPointException(Exception):
    def __init__(self, expression: str = "Ошибка размерности объектов", message: str = "Невозможно провести операцию разной размерности."):
        super().__init__(expression, message)
