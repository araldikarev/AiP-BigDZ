from models.vector import Vector
from models.point import Point
from models.exceptions import DimensionMismatchPointException
from typing import List, Self, Union
import math

class Sphere(Vector):
    def __init__(self, end_cords: List[float], start_cords: List[float] = None):
        """
        Создаёт объект сферы из координат точки конца и начала радиус-вектора.

        :param end_cords: Координаты конечной точки
        :type end_cords: List[float]
        :param start_cords: Координаты начальной точки (центр сферы)
        :type start_cords: List[float]
        :returns: Sphere
        :raises TypeError: Если типы объектов - не список координат.
        :raises DimensionMismatchPointException: Если размер списков не совпадает.
        """
        super().__init__(end_cords, start_cords)

    #region Проверки на содержание
    def contains(self, point: Point):
        """
        Проверяет содержится ли в шаре точка.

        :param point: Точка
        :type point: Point
        :returns: True, если содержит, иначе - False
        :raises TypeError: Если тип point - не точка.
        :raises DimensionMismatchPointException: Если размерность точки и сферы не совпадает.
        """
        
        if type(point) is not Point:
            raise TypeError(f"Невозможно проверить содержание объекта типа {type(point)} в шаре")
        if point.dimension != self.start_point.dimension:
            raise DimensionMismatchPointException(message="Невозможно проверить contains: размерность точки и сферы должны совпадать")
        distance = Vector.from_points(point, self.start_point).length
        
        if distance < self.radius or math.isclose(distance, self.radius, rel_tol=1e-9, abs_tol=1e-9):
            return True
        return False
    
    def on_sphere(self, point: Point):
        """
        Проверяет, лежит ли точка на сфере.

        :param point: Точка
        :type point: Point
        :returns: True, если лежит, иначе - False
        :raises TypeError: Если тип point - не точка.
        :raises DimensionMismatchPointException: Если размерность точки и сферы не совпадает.
        """

        if type(point) is not Point:
            raise TypeError(f"Невозможно проверить принадлежность объекта типа {type(point)} сфере")
        if point.dimension != self.start_point.dimension:
            raise DimensionMismatchPointException(message="Невозможно проверить on_sphere: размерность точки и сферы должны совпадать")
        distance = Vector.from_points(point, self.start_point).length
        if math.isclose(distance, self.radius, rel_tol=1e-9, abs_tol=1e-9):
            return True
        return False
    #endregion
    
    #region Свойства сферы
    @property
    def length(self) -> float:
        """Возвращает радиус."""
        return self.radius

    @property
    def radius(self) -> float:
        """Возвращает радиуса через модуль вектора-радиуса."""
        return Vector.abs(self)

    def area(self) -> float:
        """
        Вычисляет площадь сферы.

        :returns: float
        """
        n = self.dimension
        R = self.radius

        numerator = 2 * (math.pi ** (n/2))
        denominator = math.gamma(n/2)

        return (numerator/denominator) * (R ** (n-1))

    def volume(self) -> float:
        """
        Вычисляет объем шара, сопадающего с этой сферой.

        :returns: float
        """
        n = self.dimension
        R = self.radius

        numerator = math.pi ** (n/2)
        denominator = math.gamma(n/2 + 1)

        return (numerator / denominator) * (R ** n)

    #endregion

    #region Блокировка операций
    def __add__(self, object): 
        raise TypeError("Операция сложения для Sphere запрещена")
    def __radd__(self, object): 
        raise TypeError("Операция сложения для Sphere запрещена")
    def __sub__(self, object):
        raise TypeError("Операция вычитания для Sphere запрещена")
    def __rsub__(self, object):
        raise TypeError("Операция вычитания для Sphere запрещена")
    def __neg__(self):
        raise TypeError("Операция инверсии для Sphere запрещена")
    def __abs__(self):
        raise TypeError("Операция модуля для Sphere запрещена")
    #endregion

    #region Умножение
    def __mul__(self, scalar: Union[int, float]) -> Self:
        """
        Умножение сферы на скаляр.

        :param scalar: Скаляр для умножения
        :type scalar: int, float
        :returns: Sphere
        :raises TypeError: Если тип аргумнета не совместим со скаляром.
        """
        if not isinstance(scalar, (int, float)):
            raise TypeError(f"Невозможно умножить сферу на объект типа {type(scalar)}")
        return super().__mul__(scalar)
    
    def __rmul__(self, scalar: Union[int, float]) -> Self:
        """
        Умножение сферы на скаляр.

        :param scalar: Скаляр для умножения
        :type scalar: int, float
        :returns: Sphere
        :raises TypeError: Если тип аргумнета не совместим со скаляром.
        """

        return self.__mul__(scalar)
    #endregion

    #region Дополнительные операции
    def __str__(self):
        """
        Преобразует сферу в строку для print.

        :returns: str
        """

        return f"Sphere[{self.dimension}](start_point={self.start_point}, radius={self.radius})"
    
    def __eq__(self, sphere: "Sphere"):
        """
        Сравнивает 2 сферы. True - если начальная точка и радиус совпадают, False - если нет.

        :returns: bool
        """
        
        if not isinstance(sphere, Sphere):
            return False
        return self.start_point == sphere.start_point and math.isclose(self.length, sphere.length, rel_tol=1e-9, abs_tol=1e-9) 
    #endregion

    #region CLS-методы
    @classmethod
    def from_vector(cls, vector: Vector) -> "Sphere":
        """
        Создаёт объект сферы из вектора.

        :param vector: Вектор
        :type vector: Vector
        :returns: Sphere
        :raises TypeError: Если тип объекта - не вектор.
        :raises DimensionMismatchPointException: Если размер списков не совпадает.
        """

        if type(vector) is not Vector:
            raise TypeError(f"Невозможно создать сферу из объекта типа {type(vector)}")
        return cls(vector.end_point.values, vector.start_point.values)

    @classmethod
    def from_points(cls, end_point: Point, start_point: Point) -> "Sphere":
        """
        Создаёт объект сферы из 2 точек.

        :param end_point: Точка конца вектора радиуса
        :type end_point: Point
        :param start_point: Точка начала вектора радиуса
        :type start_point: Point
        :returns: Sphere
        :raises TypeError: Если типы объектов - не точка.
        :raises DimensionMismatchPointException: Если размер списков не совпадает.
        """

        if type(end_point) is not Point or type(start_point) is not Point:
            raise TypeError(f"Невозможно создать сферу из объектов типа ({type(end_point)}, {type(start_point)})")
        return cls(end_point.values, start_point.values)
        
    @classmethod
    def from_length(cls, length: Union[int, float], dimension: int) -> "Sphere":
        """
        Создаёт объект сферы из длины радиуса и размерности.

        :param length: Длина радиуса
        :type length: float
        :param dimension: Размерность
        :type dimension: int
        :returns: Sphere
        :raises ValueError: Если размерность меньше единицы
        """
        if not isinstance(length, (int, float)):
            raise TypeError("Тип радиуса должен быть числом (int или float)")
        if not isinstance(dimension, int):
            raise TypeError("Тип размерности должен быть целочисленным значением")
        if dimension < 1:
            raise ValueError("Размерность должна быть >= 1")
        return cls([0.0] * (dimension - 1) + [float(length)], None)
    #endregion