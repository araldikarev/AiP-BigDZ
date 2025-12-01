from models.point import Point
from models.exceptions import DimensionMismatchPointException
from typing import List, Union, Self, overload
import math

class Vector(Point):
    def __init__(self, end_cords: List[float], start_cords: List[float] = None):
        """
        Создаёт объект вектора из координат.

        :param end_cords: Координаты конечной точки
        :type end_cords: List[float]
        :param start_cords: Координаты начальной точки
        :type start_cords: List[float]
        :returns: Vector
        :raises TypeError: Если типы объектов - не список координат.
        :raises DimensionMismatchPointException: Если размер списков не совпадает.
        """

        if not isinstance(end_cords, list) or (start_cords is not None and not isinstance(start_cords, list) ):
            raise TypeError("Невозможно создать вектор не из списка координат.")
        if start_cords is not None and len(start_cords) != len(end_cords):
            raise DimensionMismatchPointException(message="Начальная и конечная точки имеют разную размерность.")
        self.start_point = Point(start_cords) if start_cords is not None else Point([0.0] * len(end_cords))
        super().__init__([end_cords[i] - self.start_point.values[i] for i in range(len(end_cords))])
        self.end_point = self.start_point + self.point

    @property
    def length(self):
        """
        Длина вектора (модуль вектора).
        """
        return abs(self)
    
    def is_radius_vector(self):
        """
        Проверяет, является ли вектор радиус-вектором (начало в нулевой координате).
        """
        return True if self.start_point.values == [0.0] * self.dimension else False

    #region Сложение
    @overload
    def __add__(self, object: "Vector") -> Self:
        ...

    @overload
    def __add__(self, object: List[float]) -> Self:
        ...
        
    def __add__(self, object: Union["Vector", List[float]]) -> Self:
        """
        Сложение вектора с вектором/координатами

        :param object: Объект для сложения
        :type object: Union["Point", List[float]]
        :returns: Vector
        :raises TypeError: Если типы объектов не совместимы с точкой.
        :raises DimensionMismatchPointException: Если размерность векторов не совпадает.
        """
        if isinstance(object, Vector):
            start_values = object.start_point.values
            end_values = object.end_point.values
        elif isinstance(object, list):
            start_values = object
            end_values = object
        else:
            raise TypeError(f"Невозможно сложить вектор с объектом типа \"{type(object)}\"")

        length = len(start_values)
        if length != self.dimension:
            raise DimensionMismatchPointException(message="Невозможно провести операцию сложения из-за несоответствия размерностей.")
        return self.__class__([self.end_point.values[i] + end_values[i] for i in range(length)], [self.start_point.values[i] + start_values[i] for i in range(length)])
    #endregion

    #region Вычитание
    @overload
    def __sub__(self, object: Union["Vector"]) -> Self:
        ...

    @overload
    def __sub__(self, object: List[float]) -> Self:
        ...
    
    def __sub__(self, object: Union["Vector", List[float]]) -> Self:
        """
        Вычитание вектора/координат из вектора

        :param object: Объект-вычитаемое
        :type object: Union["Point", List[float]]
        :returns: Vector
        :raises TypeError: Если типы объектов не совместимы с точкой.
        :raises DimensionMismatchPointException: Если размерность векторов не совпадает.
        """
        if isinstance(object, Vector):
            start_values = object.start_point.values
            end_values = object.end_point.values
        elif isinstance(object, list):
            start_values = object
            end_values = object
        else:
            raise TypeError(f"Невозможно произвести вычитание с вектором и с объектом типа \"{type(object)}\"")
        
        return self.__add__(Vector([-coord for coord in end_values], [-coord for coord in start_values]))
    #endregion

    #region Умножение
    @overload
    def __mul__(self, scalar: Union[int, float]) -> Self:
        ...

    @overload
    def __mul__(self, object: "Vector") -> "float":
        ...

    def __mul__(self, object: Union["Vector", int, float]):
        """
        Умножение вектора на скаляр или скалярное произведение.

        :param object: Объект для умножения
        :type object: Union["Vector", float]
        :returns: float, если объект для умножения вектор, иначе Vector
        :raises TypeError: Если типы объектов не совместимы со скаляром или вектором.
        :raises DimensionMismatchPointException: Если размерность векторов не совпадает.
        """
        if isinstance(object, Vector):
            return Vector.scalar_multiply(self, object)
        elif not isinstance(object, (int, float)):
            raise TypeError("Не удалось выполнить операцию", f"Невозможно умножить объект типа \"Vector\" на тип \"{type(object)}\"")

        scalar = object
        new_values = [self.values[i] * scalar for i in range(self.dimension)]
        new_end_cords = [self.start_point.values[i] + new_values[i] for i in range(self.dimension)]
        return self.__class__(new_end_cords, self.start_point.values)
    
    def __rmul__(self, object: Union["Vector", int, float]) -> Self:
        """
        Умножение вектора/скаляра на вектор или скалярное произведение.

        :param object: Объект для умножения
        :type object: Union["Vector", int, float]
        :returns: float, если объект для умножения вектор, иначе Vector
        :raises TypeError: Если типы объектов не совместимы со скаляром или вектором.
        :raises DimensionMismatchPointException: Если размерность векторов не совпадает.
        """
        return self.__mul__(object)
    #endregion

    #region Дополнительные операции
    def __neg__(self):
        """
        Возвращает развернутый вокруг точки вектор.

        :returns: Vector
        """
        new_end_cords = [self.start_point.values[i] - self.values[i] for i in range(self.dimension)]
        return self.__class__(new_end_cords, self.start_point.values)
    
    def __abs__(self) -> float:
        """
        Возвращает модуль вектора (его длину)

        :returns: float
        """
        return sum(coord**2 for coord in self.values)**0.5

    def __str__(self):
        """
        Преобразует вектор в строку для print.

        :returns: str
        """
        return f"Vector[{self.dimension}](({', '.join(map(str, self.start_point.values))}), ({', '.join(map(str, self.end_point.values))}))"
    
    def __eq__(self, vector: "Vector"):
        """
        Сравнивает 2 вектора. True - если координаты сдвига и начальная точка совпадают, False - если нет.

        :returns: bool
        """
        
        if not isinstance(vector, Vector):
            return False
        return self.point == vector.point and self.start_point == vector.start_point 
    #endregion

    #region Статические методы
    @staticmethod
    def scalar_multiply(a: "Vector", b: "Vector"):
        """
        Скалярное произведение векторов.

        :param a: Первый вектор
        :type a: Vector
        :param b: Второй вектор
        :type b: Vector
        :returns: float
        :raises TypeError: Если типы объектов - не Вектор.
        :raises DimensionMismatchPointException: Если размерность векторов не совпадает.
        """
        if not isinstance(a, Vector) or not isinstance(b, Vector):
            raise TypeError("Невозможно произвести операцию скалярного умножения без объекта типа Vector")
        length_1 = a.dimension
        length_2 = b.dimension
        if length_1 != length_2:
            raise DimensionMismatchPointException(message="Невозможно провести скалярное произведение из-за несоответствия размерностей.")
        
        return sum(a.values[i] * b.values[i] for i in range(length_1))
    

    @staticmethod
    def abs(vector: "Vector"):
        """
        Вычисляет модуль вектора (его длину).

        :param vector: Вектор
        :type vector: Vector
        :returns: float
        :raises TypeError: Если типы объектов - не Вектор.
        :raises DimensionMismatchPointException: Если размерность векторов не совпадает.
        """
        if not isinstance(vector, Vector):
            raise TypeError(f"Невозможно получить модуль вектора из объекта типа {type(vector)}")
        return sum(coord**2 for coord in vector.values)**0.5
    
    @staticmethod
    def is_collinear(a: "Vector", b: "Vector"):
        """
        Проверяет, являются ли векторы коллинеарными через свойство рангов матрицы
        
        Если все ранги матрицы 2xN = 0, то векторы коллинеарны
        
        :param a: Первый вектор
        :type a: Vector
        :param b: Второй вектор
        :type b: Vector
        :returns: True - если векторы коллинеарны, иначе - False
        :raises TypeError: Если типы объектов - не Вектор.
        :raises DimensionMismatchPointException: Если размерность векторов не совпадает.
        """
        if not isinstance(a, Vector) or not isinstance(b, Vector):
            raise TypeError(f"Невозможно проверить на коллинеарность объекты типов ({type(a), type(b)}), оба объекты должны быть объектами типа \"Vector\"")
        
        length_1 = a.dimension
        length_2 = b.dimension
        if length_1 != length_2:
            raise DimensionMismatchPointException(message="Невозможно проверить векторы на коллинеарность из-за несоответствия размерностей.")
        if length_1 == 1:
            return True


        matrix_elements = list(zip(a.values, b.values))
        for i in range(length_1):
            for j in range(i+1, length_1):
                first = matrix_elements[i]
                second = matrix_elements[j]
                det = first[0] * second[1] - first[1] * second[0]
                if not math.isclose(det, 0.0, rel_tol=1e-9, abs_tol=1e-9):
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
            raise TypeError(f"Невозможно проверить объекты типа ({type(a), type(b)}) на ортогональность, оба объекты должны быть объектами типа \"Vector\"")

        length_1 = a.dimension
        length_2 = b.dimension
        if length_1 != length_2:
            raise DimensionMismatchPointException(message="Невозможно проверить векторы на ортогональность.")
        
        if math.isclose(Vector.scalar_multiply(a, b), 0.0, rel_tol=1e-9, abs_tol=1e-9):
            return True
        
        return False

    #endregion

    #region CLS-методы
    @classmethod
    def from_point(cls, point: Point) -> "Vector":
        """
        Создаёт объект вектора (радиус-вектора) из точки.

        :param point: Точка
        :type point: Point
        :returns: Vector
        :raises TypeError: Если типы объектов - не точка.
        :raises DimensionMismatchPointException: Если размер списков не совпадает.
        """
        if not isinstance(point, Point):
            raise TypeError(f"Невозможно создать объект вектора из объекта типа {type(point)}")
        return cls(point.values)
    
    @classmethod
    def from_points(cls, end_point: Point, start_point: Point) -> "Vector":
        """
        Создаёт объект вектора из 2 точек.

        :param end_point: Точка конца вектора
        :type end_point: Point
        :param start_point: Точка начала вектора
        :type start_point: Point
        :returns: Vector
        :raises TypeError: Если типы объектов - не точка.
        :raises DimensionMismatchPointException: Если размер списков не совпадает.
        """
        
        if not isinstance(end_point, Point) or not isinstance(start_point, Point):
            raise TypeError(f"Невозможно создать объект вектора из объектов типа ({type(end_point)}, {type(start_point)})")
        return cls(end_point.values, start_point.values) 
    #endregion