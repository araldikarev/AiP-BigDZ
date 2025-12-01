from models.point import Point
from models.vector import Vector
from models.sphere import Sphere

if __name__ == "__main__":
    point_a = Vector([1, 1, 1])

    a = Vector([1, 2, 3, 4, 0])
    b = Vector([1, 6, 5, 1, 1])
    c = Vector([1, 6, 5, 1, 1])

    print("_"*40 + "\n")

    print(f"Вектор a: {str(a)}, его модуль: {abs(a)}\n")
    print(f"Вектор b: {str(b)}, его модуль: {abs(b)}\n")
    print(f"Вектор с: {str(c)}, его модуль: {abs(c)}\n")

    print(f"Равенство b и c: {b == c}")

    print("\n" + "_"*40 + "\n")

    print(f"Сложение векторов {str(a)} и {str(b)} = {a+b}\n")
    print(f"Вычитание вектора {str(a)} из {str(b)} = {b-a}\n")
    print(f"Умножение на число {str(a)} * 5: {a * 5}\n")
    
    print(f"Скалярное произведение {str(a)} * {str(b)} (вариант через \"*\"): {a * b}\n")
    print(f"Скалярное произведение {str(a)} * {str(b)} (вариант через вызов статического метода): {Vector.scalar_multiply(a, b)}\n")
    print(f"Коллинеарность {str(a)} и {str(a*-2.001)}: {Vector.is_collinear(a, a*5)}\n")
    print(f"Коллинеарность {str(a)} и {str(b)}: {Vector.is_collinear(a, b)}\n")
    
    d = Vector([1, 1])
    e = Vector([-1, 1])
    h = Vector([0, 1])

    print(f"Ортогональность {str(d)} и {str(e)}: {Vector.is_orthogonal(d, e)}\n")
    print(f"Ортогональность {str(d)} и {str(h)}: {Vector.is_orthogonal(d, h)}\n")

    
    print("\n" + "_"*40 + "\n")


    
    