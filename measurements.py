from dataclasses import dataclass
from math import sin, cos, asin, atan, pi as PI

@dataclass
class Matrix:
    M: list[list[float]]

    def __str__(self):
        return self.M.__str__()
    
    def __add__(self, other: 'Matrix'):
        A = self.M
        B = other.M
        li: list[list[float]] = [[col + B[r][c]
                                  for c, col in enumerate(row)]
                                  for r, row in enumerate(A)]
        return Matrix(li)
    
    def __mul__(self, other: 'Matrix'):
        A = self.M
        B = Matrix.transpose(other).M
        li: list[list[float]] = []
        li = [[sum([i * col[c]
                    for c, i in enumerate(row)])
                    for col in B]
                    for row in A]
        return Matrix(li)

    @staticmethod
    def transpose(m: 'Matrix'):
        A = m.M
        n_row = len(A)
        n_col = len(A[0])
        li: list[list[float]] = [[A[col][row]
                                  for col in range(n_row)]
                                  for row in range(n_col)]
        return Matrix(li)
    
    @staticmethod
    def toPolar(m: 'Matrix'):
        x, y, z = Matrix.UnpackVector(m)
        rho = (x * x + y * y + z * z) ** 0.5
        theta = atan(y / x) + (x > 0 and y < 0) * 2 * PI + (x <= 0) * PI
        phi = asin(z / rho)
        return Matrix.Vector(rho, theta, phi)
    
    @staticmethod
    def toCartesian(m: 'Matrix'):
        rho, theta, phi = Matrix.UnpackVector(m)
        x = rho * cos(theta) * cos(phi)
        y = rho * sin(theta) * cos(phi)
        z = rho * sin(phi)
        return Matrix.Vector(x, y, z)
    
    @staticmethod
    def Vector(*args: float):
        return Matrix([[arg] for arg in args])
    
    @staticmethod
    def UnpackVector(m: 'Matrix'):
        return tuple((row[0] for row in m.M))
    
    @staticmethod
    def normalize(m: 'Matrix'):
        x, y, z = Matrix.UnpackVector(m)
        rho = (x * x + y * y + z * z) ** 0.5
        return Matrix.Vector(x / rho, y / rho, z / rho)

    @staticmethod    
    def rMatrix(m: 'Matrix'):
        '''
        alpha   y axis
        beta    z axis
        gamma   x axis
        '''
        alpha, beta, gamma = Matrix.UnpackVector(m)
        return Matrix([[cos(alpha) * cos(beta),
                        -sin(beta),
                        sin(alpha) * cos(beta)],
                        [cos(alpha) * sin(beta) * cos(gamma) + sin(alpha) * sin(gamma),
                         cos(beta) * cos(gamma),
                         sin(alpha) * sin(beta) * cos(gamma) - cos(alpha) * sin(gamma)],
                         [cos(alpha) * sin(beta) * sin(gamma) - sin(alpha) * cos(gamma),
                          cos(beta) * sin(gamma),
                          sin(alpha) * sin(beta) * sin(gamma) + cos(alpha) * cos(gamma)]])
    
    @staticmethod
    def rFactors(m: 'Matrix', gamma: float = -(PI / 2)):
        x, y, z = Matrix.UnpackVector(m)
        alpha: float = atan(z / x)
        beta: float = -atan((x * y) / (x * x + z * z) / cos(alpha)) + (x < 0) * PI
        return Matrix.Vector(alpha, beta, gamma)

@dataclass
class Color:
    WHITE: str      = "FFFFFF"
    GRAY: str       = "B2B2B2"
    BLACK: str      = "000000"
    RED: str        = "FF0000"
    ORANGE: str     = "F79D53"
    YELLOW: str     = "FFFF00"
    GREEN: str      = "00B050"
    TURQUOISE: str  = "5DB3CB"
    BLUE: str       = "69D8FF"
    PURPLE: str     = "9E5ECE"
    PINK: str       = "FF66FF"
    BROWN: str      = "BCB48A"
    
    @staticmethod
    def rgb_to_tuple(rgb: int):
        assert 0 <= rgb < 16777216
        r = rgb % 256
        g = (rgb // 256) % 256
        b = ((rgb // 256) // 256) % 256
        return (r, g, b)
    
    @staticmethod
    def hex_to_rgb(hex: str):
        assert len(hex) == 6
        HEX = "0123456789ABCDEF"
        rgb = 0
        for c in f"{hex[4:6]}{hex[2:4]}{hex[0:2]}":
            rgb *= 16
            rgb += HEX.find(c)
        return rgb
    
    @staticmethod
    def tuple_to_hex(r: int, g: int, b: int):
        assert 0 <= r < 256
        assert 0 <= g < 256
        assert 0 <= b < 256
        HEX = "0123456789ABCDEF"
        return HEX[r // 16] + HEX[r % 16] + HEX[g // 16] + HEX[g % 16] + HEX[b // 16] + HEX[b % 16]
    
    @staticmethod
    def tuple_to_rgb(r: int, g: int, b: int):
        assert 0 <= r < 256
        assert 0 <= g < 256
        assert 0 <= b < 256
        return r + g * 256 + b * 256 * 256
    
    @staticmethod
    def rgb_to_hex(rgb: int):
        assert 0 <= rgb < 16777216
        HEX = "0123456789ABCDEF"
        r = rgb % 256
        g = (rgb // 256) % 256
        b = ((rgb // 256) // 256) % 256
        return HEX[r // 16] + HEX[r % 16] + HEX[g // 16] + HEX[g % 16] + HEX[b // 16] + HEX[b % 16]
    
    @staticmethod
    def hex_to_tuple(hex: str):
        assert len(hex) == 6
        HEX = "0123456789ABCDEF"
        rgb = 0
        for c in f"{hex[4:6]}{hex[2:4]}{hex[0:2]}":
            rgb *= 16
            rgb += HEX.find(c)
        r = rgb % 256
        g = (rgb // 256) % 256
        b = ((rgb // 256) // 256) % 256
        return (r, g, b)
