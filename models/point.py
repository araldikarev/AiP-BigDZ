from typing import List, Union, Self, overload
from models.exceptions import DimensionMismatchPointException, NullPointException

class Point():
    def __init__(self, values: List[float]):
        """
        Создаёт объект точки из координат.

        :param end_cords: Координаты точки
        :type end_cords: List[float]
        :returns: Point
        :raises TypeError: Если тип аргумента - не список координат.
        :raises NullPointException: Если список пустой.
        """

        if not isinstance(values, list):
            raise TypeError("Не удалось создать точку", f"Невозможно создать объект типа \"Point\" с объектом типа {type(values)}")
        
        if len(values) == 0:
            raise NullPointException("Не удалось создать точку", "Невозможно создать точку из 0 координат")

        if any(not isinstance(element, (int, float)) for element in values):
            raise TypeError("Не удалось создать точку", f"Невозможно создать объект типа \"Point\", так как не все элементы списка - числа.")
        self._values = [*values]
    
    @property
    def values(self):
        """
        Возвращает координаты точки.

        :returns: List[float]
        """
        return self._values
    
    @property
    def dimension(self):
        """
        Возвращает размерность точки.

        :returns: int
        """
        return len(self.values)
    
    @property
    def point(self):
        """
        Возвращает инстанс точки.

        :returns: Point
        """
        return Point(self.values)
    
    @overload
    def __add__(self, object: "Point") -> Self:
        ...

    @overload
    def __add__(self, object: List[float]) -> Self:
        ...
        
    def __add__(self, object: Union["Point", List[float]]) -> Self:
        """
        Сложение точки с точкой/координатами

        :params object: Объект для сложения
        :type object: Union["Point", List[float]]
        :returns: Point
        :raises TypeError: Если типы объектов не совместимы с точкой.
        :raises DimensionMismatchPointException: Если размерность координат не совпадает.
        """

        if isinstance(object, Point):
            values = object.values
        elif isinstance(object, list):
            values = object
        else:
            raise TypeError(f"Невозможно сложить точку с объектом типа \"{type(object)}\"")

        length = len(values)
        if length != self.dimension:
            raise DimensionMismatchPointException("Невозможно провести операцию сложения.", "Невозможно провести операцию сложения из-за несоответствия размерностей.")
        return self.__class__([self.values[i] + values[i] for i in range(length)])
    
    def __eq__(self, point: "Point"):
        """
        Сравнивает 2 точки. True - если координаты точки совпадают, False - если нет.

        :returns: str
        """
        if not isinstance(point, Point):
            return False
        return self.values == point.values
    
    def __str__(self):
        """
        Преобразует точку в строку для print.

        :returns: str
        """
        return f"Point[{self.dimension}]({', '.join(map(str, self.values))})"