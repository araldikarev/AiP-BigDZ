from typing import List, Union, Self, overload
from models.exceptions import DimensionMismatchPointException

class Point():
    def __init__(self, values: Union[List[int], List[float]]):

        if not isinstance(values, list):
            raise TypeError("Не удалось создать точку", f"Невозможно создать объект типа \"Point\" с объектом типа {type(values)}")
        
        if any(not isinstance(element, (int, float)) for element in values):
            raise TypeError("Не удалось создать точку", f"Невозможно создать объект типа \"Point\", так как не все элементы списка - числа.")
        self._values = [*values]
    
    @property
    def values(self):
        return self._values
    
    @property
    def dimension(self):
        return len(self.values)
    
    @property
    def point(self):
        return Point(self.values)
    
    @overload
    def __add__(self, object: "Point") -> Self:
        ...

    @overload
    def __add__(self, object: List[float]) -> Self:
        ...
        
    def __add__(self, object: Union["Point", List[float]]) -> Self:
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
        return self.values == point.values
    
    def __str__(self):
        return f"Point[{self.dimension}]({', '.join(map(str, self.values))})"