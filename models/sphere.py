from models.vector import Vector
from models.point import Point
from models.exceptions import DimensionMismatchPointException
from typing import List, Self
import math

class Sphere(Vector):
    def __init__(self, end_cords: List[float], start_cords: List[float] = None):
        super().__init__(end_cords, start_cords)

    #region Проверки на содержание
    def contains(self, point: Point):
        if point.dimension != self.start_point.dimension:
            raise DimensionMismatchPointException("Невозможно проверить contains", "Размерность точки и сферы должны совпадать")
        distance = Vector.from_points(point, self.start_point).length
        
        if distance < self.radius or math.isclose(distance, self.radius, abs_tol=1e-9):
            return True
        return False
    
    def on_sphere(self, point: Point):
        if point.dimension != self.start_point.dimension:
            raise DimensionMismatchPointException("Невозможно проверить on_sphere", "Размерность точки и сферы должны совпадать")
        distance = Vector.from_points(point, self.start_point).length
        if math.isclose(distance, self.radius, abs_tol=1e-9):
            return True
        return False
    #endregion
    
    #region Свойства сферы
    @property
    def length(self) -> float: 
        return self.radius

    @property
    def radius(self) -> float:
        return Vector.abs(self)

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
        if not isinstance(scalar, (int, float)):
            raise TypeError(f"Невозможно произвести скалярное произведение Сферы на объект типа {type(scalar)}")
        return super().__mul__(scalar)
    
    def __rmul__(self, scalar) -> Self:
        return self.__mul__(scalar)
    #endregion

    #region Дополнительные операции
    def __str__(self):
        return f"Sphere[{self.dimension}](start_point={self.start_point}, radius={self.radius})"
    
    def __eq__(self, sphere: "Sphere"):
        return self.start_point == sphere.start_point and self.point == sphere.point 
    #endregion

    #region CLS-методы
    @classmethod
    def from_vector(cls, vector: Vector) -> "Sphere":
        return cls(vector.end_point.values, vector.start_point.values)

    @classmethod
    def from_points(cls, end_point: Point, start_point: Point) -> "Sphere":
        return cls(end_point.values, start_point.values)
        
    @classmethod
    def from_length(cls, length: float, dimension: int) -> "Sphere":
        if dimension < 1:
            raise ValueError("Размерность должна быть >= 1")
        return cls([0.0] * (dimension - 1) + [float(length)], None)
    #endregion