from models.point import Point
from models.vector import Vector
from models.sphere import Sphere

if __name__ == "__main__":

    a = Vector([1, 2, 3, 4, 0])
    b = Vector([1, 6, 5, 1, 1])
    c = Vector([1, 6, 5, 1, 1])

    print("_"*40 + "\n")

    print(f"Вектор a: {a}, его модуль: {abs(a)}\n")
    print(f"Вектор b: {b}, его модуль: {abs(b)}\n")
    print(f"Вектор с: {c}, его модуль: {abs(c)}\n")

    print(f"Равенство b и c: {b == c}")

    print("\n" + "_"*40 + "\n")

    print(f"Сложение векторов {str(a)} и {str(b)} = {a+b}\n")
    print(f"Вычитание вектора {str(a)} из {str(b)} = {b-a}\n")
    print(f"Умножение на число {str(a)} * 5: {a * 5}\n")
    
    print(f"Скалярное произведение {str(a)} * {str(b)} (вариант через \"*\"): {a * b}\n")
    print(f"Скалярное произведение {str(a)} * {str(b)} (вариант через вызов статического метода): {Vector.scalar_multiply(a, b)}\n")
    print(f"Коллинеарность {str(a)} и {str(a*-2.001)}: {Vector.is_collinear(a, a*-2.001)}\n")
    print(f"Коллинеарность {str(a)} и {str(b)}: {Vector.is_collinear(a, b)}\n")
    
    d = Vector([1, 1])
    e = Vector([-1, 1])
    h = Vector([0, 1])

    print(f"Ортогональность {str(d)} и {str(e)}: {Vector.is_orthogonal(d, e)}\n")
    print(f"Ортогональность {str(d)} и {str(h)}: {Vector.is_orthogonal(d, h)}\n")

    
    print("\n" + "_"*40 + "\n")

    
    point_a = Point([1, 1, 1])
    point_b = Point([5, 5, 5])
    point_c = Point([7, 7, 7])
    point_d = Point([12, 12, 12])

    print(f"Точка a: {point_a}")
    print(f"Точка b: {point_b}")
    print(f"Точка c: {point_c}")
    print(f"Точка d: {point_d}")

    vector_ab = Vector.from_points(point_b, point_a)
    print(f"Вектор из точек a и b: {vector_ab}")
    
    sphere = Sphere.from_vector(vector_ab)

    print(f"Сфера из вектора ab: {sphere}")
    print(f"Принадлежит ли точка {point_c} шару: {sphere.contains(point_c)}")
    print(f"Принадлежит ли точка {point_d} шару: {sphere.contains(point_d)}")
    print(f"Принадлежит ли точка {point_c} сфере: {sphere.on_sphere(point_c)}")
    print(f"Принадлежит ли точка {point_d} сфере: {sphere.on_sphere(point_d)}")
    print(f"Принадлежит ли точка {point_a} сфере: {sphere.on_sphere(point_a)}")
    print(f"Принадлежит ли точка {point_b} сфере: {sphere.on_sphere(point_b)}")




    