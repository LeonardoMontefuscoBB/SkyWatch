import sys, os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from measurements import Matrix, Color
import random
def VectorTest():
    v1 = random.randrange(0, 100)
    v2 = random.randrange(0, 100)
    v3 = random.randrange(0, 100)
    v4 = random.randrange(0, 100)
    v5 = random.randrange(0, 100)
    v = (v1, v2, v3, v4, v5)

    vector = Matrix.Vector(v1, v2, v3, v4, v5)
    unpacked = Matrix.UnpackVector(vector)

    assert v == unpacked
    assert len(v) == len(vector.M)

    return None

def ColorTest():
    r = random.randrange(0, 256)
    g = random.randrange(0, 256)
    b = random.randrange(0, 256)

    hex1 = Color.tuple_to_hex(r, g, b)
    int1 = Color.hex_to_rgb(hex1)
    tup1 = Color.rgb_to_tuple(int1)
    int2 = Color.tuple_to_rgb(tup1[0], tup1[1], tup1[2])
    hex2 = Color.rgb_to_hex(int2)
    tup2 = Color.hex_to_tuple(hex2)

    assert tup1 == tup2 == (r, g, b)
    assert hex1 == hex2
    assert int1 == int2

    return None

if __name__ == "__main__":
    VectorTest()
    ColorTest()
