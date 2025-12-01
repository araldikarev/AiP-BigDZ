from models.point import Point
from models.exceptions import DimensionMismatchPointException
from typing import List, Union, Self, overload

class Vector(Point):
    def __init__(self, end_cords: List[float], start_cords: List[float] = None):
        self.start_point = Point(start_cords) if start_cords != None else Point([0.0] * len(end_cords))
        super().__init__([end_cords[i] - self.start_point.values[i] for i in range(len(end_cords))])
        self.end_point = self.start_point + self.point

    @property
    def length(self):
        return abs(self)
    
    def is_radius_vector(self):
        return True if self.start_point.values == [0.0] * self.dimension else False

    #region Сложение
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
            raise TypeError(f"Невозможно сложить вектор с объектом типа \"{type(object)}\"")

        length = len(values)
        if length != self.dimension:
            raise DimensionMismatchPointException("Невозможно провести операцию сложения.", "Невозможно провести операцию сложения из-за несоответствия размерностей.")
        return self.__class__((self.end_point + values).values, self.start_point.values)
    #endregion

    #region Вычитание
    @overload
    def __sub__(self, object: Union["Point"]) -> Self:
        ...

    @overload
    def __sub__(self, object: List[float]) -> Self:
        ...
    
    def __sub__(self, object: Union["Point", List[float]]) -> Self:
        if isinstance(object, Point):
            values = object.values
        elif isinstance(object, list):
            values = object
        else:
            raise TypeError(f"Невозможно произвести вычитание с вектором и с объектом типа \"{type(object)}\"")
        
        return self.__add__([-coord for coord in values])
    #endregion

    #region Умножение
    @overload
    def __mul__(self, scalar: float) -> Self:
        ...

    @overload
    def __mul__(self, object: "Vector") -> "float":
        ...

    def __mul__(self, object: Union["Vector", float]):
        if isinstance(object, Vector):
            return Vector.scalar_multiply(self, object)
        elif not isinstance(object, (int, float)):
            raise TypeError("Не удалось выполнить операцию", f"Невозможно умножить объект типа \"Vector\" на тип \"{type(object)}\"")

        scalar = object
        new_values = [self.values[i] * scalar for i in range(self.dimension)]
        new_end_cords = [self.start_point.values[i] + new_values[i] for i in range(self.dimension)]
        return self.__class__(new_end_cords, self.start_point.values)
    
    def __rmul__(self, scalar: Union[int, float]) -> Self:
        return self.__mul__(scalar)
    #endregion

    #region Дополнительные операции
    def __neg__(self):
        return Vector([-coord for coord in self.values])
    
    def __abs__(self) -> float:
        return sum(coord**2 for coord in self.values)**0.5

    def __str__(self):
        return f"Vector(({", ".join(map(str, self.start_point.values))}), ({", ".join(map(str, self.end_point.values))}))"
    
    def __eq__(self, point: Point):
        return self.point == point
    #endregion

    #region Статические методы
    @staticmethod
    def scalar_multiply(a: "Vector", b: "Vector"):
        if not isinstance(a, Vector) or not isinstance(b, Vector):
            raise TypeError("Невозможно произвести операцию скалярного умножения без объекта типа Vector")
        length_1 = a.dimension
        length_2 = b.dimension
        if length_1 != length_2:
            raise DimensionMismatchPointException("Невозможно провести операцию скалярного произведения.", "Невозможно провести скалярного произведения из-за несоответствия размерностей.")
        
        return sum(a.values[i] * b.values[i] for i in range(length_1))
    

    @staticmethod
    def abs(vector: "Vector"):
        return sum(coord**2 for coord in vector.values)**0.5
    
    @staticmethod
    def is_collinear(a: "Vector", b: "Vector"):
        """
        Проверяет, являются ли векторы коллинеарными через свойство рангов матрицы
        
        Если все ранги матрицы 2xN = 0, то векторы коллинеарны
        
        """
        if not isinstance(a, Vector) or not isinstance(b, Vector):
            raise TypeError(f"Невозможно произвести операцию скалярного умножения объектов типа {(type(a), type(b))}, оба объекты должны быть объектами типа \"Vector\"")
        
        length_1 = a.dimension
        length_2 = b.dimension
        if length_1 != length_2:
            raise DimensionMismatchPointException("Невозможно проверить на коллинеарность.", "Невозможно проверить векторы на коллинеарность из-за несоответствия размерностей.")
        if length_1 <= 1:
            return True


        matrix_elements = list(zip(a.values, b.values))
        for i in range(length_1):
            for j in range(i+1, length_1):
                first = matrix_elements[i]
                second = matrix_elements[j]
                if first[0] * second[1] - first[1] * second[0] != 0:
                    return False
                
        return True

    @staticmethod
    def is_orthogonal(a: "Vector", b: "Vector"):
        """
        Проверяет, являются ли векторы ортогональными через скалярное произведение векторов.
        
        Если скалярное произведение равно 0, то векторы отрогональны. В ином случае - нет.
        
        :param a: Первый вектор
        :type a: Vector
        :param b: Второй вектор
        :type b: Vector
        :returns: True - если векторы ортогональны, иначе - False
        :raises TypeError: Если типы объектов - не Вектор.
        :raises DimensionMismatchPointException: Если размерность векторов не совпадает.
        """
        if not isinstance(a, Vector) or not isinstance(b, Vector):
            raise TypeError(f"Невозможно проверить объекты типа {(type(a), type(b))} на ортогональность, оба объекты должны быть объектами типа \"Vector\"")

        length_1 = a.dimension
        length_2 = b.dimension
        if length_1 != length_2:
            raise DimensionMismatchPointException("Невозможно проверить на ортогональность.", "Невозможно проверить векторы на ортогональность из-за несоответствия размерностей.")
        if length_1 <= 1:
            return False
        
        if Vector.scalar_multiply(a, b) == 0:
            return True
        
        return False

    #endregion

    #region CLS-методы
    @classmethod
    def from_point(cls, point: Point) -> "Vector":
        return cls(point.values)
    
    @classmethod
    def from_points(cls, start_point: Point, end_point: Point) -> "Vector":
        return cls(end_point.values, start_point.values) 
    #endregion