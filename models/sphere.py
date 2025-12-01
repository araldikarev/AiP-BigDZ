from models.vector import Vector
from models.point import Point
from typing import List, Self
import math

class Sphere(Vector):
    def __init__(self, vector: Vector):
        super().__init__(vector.values, vector.start_point.values if not vector.is_radius_vector() else None)

    #region Проверки на содержание
    def contains(self, point: Point):
        # Возможно сделать проверку на мерность? или не стоит?

        if Vector.from_point(point.point).length <= self.radius:
            return True
        return False
    
    def on_sphere(self, point: Point):
        # Возможно сделать проверку на мерность? или не стоит?

        if Vector.from_point(point.point).length == self.radius:
            return True
        return False
    #endregion
    
    #region Свойства сферы
    @property
    def radius(self) -> float:
        return self.length

    def area(self) -> float:
        """Площадь сферы"""
        n = self.dimension
        R = self.radius

        numerator = 2 * (math.pi ** (n/2))
        denominator = math.gamma(n/2)

        return (numerator/denominator) * (R ** (n-1))

    def volume(self) -> float:
        """Объём шара"""
        n = self.dimension
        R = self.radius

        numerator = math.pi ** (n/2)
        denominator = math.gamma(n/2 + 1)

        return (numerator / denominator) * (R ** n)

    #endregion

    #region Блокировка операций
    __add__ = None
    __sub__ = None
    __neg__ = None
    __abs__ = None
    #endregion

    #region Умножение
    def __mul__(self, scalar: float) -> Self:
        if not isinstance(scalar, float):
            raise TypeError(f"Невозможно произвести скалярное произведение Сферы на объект типа {type(scalar)}")
        return super().__mul__(scalar)
    
    def __rmul__(self, scalar) -> Self:
        return self.__mul__(scalar)
    #endregion

    #region Дополнительные операции
    def __str__(self):
        return f"Sphere({", ".join(map(str, self.values))})"
    #endregion

    #region CLS-методы
    @classmethod
    def from_values(cls, end_values: List[float], start_values: List[float] = None) -> "Sphere":
        return cls(end_values, start_values if start_values != None else [0.0] * len(end_values))

    @classmethod
    def from_points(cls, end_point: Point, start_point: Point) -> "Sphere":
        return cls(Vector(start_point.values, end_point.values))
    
    @classmethod
    def from_length(cls, length: float, dimension: int) -> "Sphere":
        if dimension < 1:
            raise ValueError("Размерность должна быть >= 1")
        return cls(Vector([0.0] * (dimension - 1) + [float(length)], [0.0] * dimension))
    #endregion