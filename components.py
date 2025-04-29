from dataclasses import dataclass
from measurements import Matrix, Color
from math import pi as PI

@dataclass
class Star:
    def __init__(self, index: str, cindex: str, sindex: str, x: str, y: str, z: str, rgb: str, designation:str, magnitude: str):
        self.index:  int = int(index)
        self.cindex: int = int(cindex)
        self.sindex: int = int(sindex)
        
        self.x:     float = float(x)
        self.x_var: float = float(self.x)
        self.y:     float = float(y)
        self.y_var: float = float(self.y)
        self.z:     float = float(z)
        self.z_var: float = float(self.z)

        self.rgb:   str = rgb
        
        self.designation:   str   = designation
        self.magnitude:     float = float(magnitude)
        self.rgb_des:       str   = Star.designationColor(self.designation)
        self.size:          float = Star.starSize(self.magnitude)
        return None
    
    @classmethod
    def designationColor(designation: str):
        match designation[-1]:
            case 'A':
                return Color.RED
            case 'B':
                return Color.ORANGE
            case 'G':
                return Color.YELLOW
            case 'D':
                return Color.GREEN
            case 'E':
                return Color.TURQUOISE
            case 'Z':
                return Color.BLUE
            case 'H':
                return Color.PURPLE
            case 'V':
                return Color.PINK
            case 'I':
                return Color.BROWN
        if designation[-1] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            return Color.GRAY
        return Color.WHITE
    
    @classmethod
    def starSize(magnitude: float):
        if   magnitude < 0.8: return 10.0
        elif magnitude < 0.0: return  8.0
        elif magnitude < 1.2: return  6.0
        elif magnitude < 2.0: return  5.0
        elif magnitude < 3.0: return  4.0
        elif magnitude < 5.0: return  2.0
        elif magnitude < 6.0: return  1.0
        return 0.5
    
    def rotate(self, R: Matrix = Matrix([1, 0, 0], [0, 1, 0], [0, 0, 1])):
        v = Matrix.Vector(self.x, self.y, self.z)
        self.x_var, self.y_var, self.z_var = Matrix.UnpackVector(R * v)
        return None
    
    def position(self):
        v = Matrix.Vector(self.x_var, self.y_var, self.z_var)
        theta, phi = Matrix.UnpackVector(Matrix.toPolar(v))[1:]
        posX = 1571 - round(((theta + PI / 4) % (2 * PI)) * 1000)
        posY = round((((phi + 3 * PI / 4) % PI) - PI / 2) * 1000)
        if not 0 <= posX < 1572: return None
        if not 0 <= posY < 1572: return None
        return posX, posY

@dataclass
class Vector:
    def __init__(self, A: Star, B: Star, rgb: str):
        self.A: Matrix = Matrix.Vector(A.x, A.y, A.z)
        self.B: Matrix = Matrix.Vector(B.x, B.y, B.z)
        self.rgb: str = rgb
        return None
    
@dataclass
class Constellation:
    def __init__(self, cindex: str, name: str, abbreviation: str,
                 R11: str, R12: str, R13: str,
                 R21: str, R22: str, R23: str,
                 R31: str, R32: str, R33: str,
                 rgb: str):
        self.cindex: int = int(cindex)
        self.name: str = name
        self.abbreviation: str = abbreviation
        self.rgb: str = rgb
        self.starset: dict[str, Star] = {}
        self.vectorset: list[Vector] = []
        self.R: Matrix = Matrix([[float(R11), float(R12), float(R13)],
                                 [float(R21), float(R22), float(R23)],
                                 [float(R31), float(R32), float(R33)]])
    
    def __len__(self):
        return self.starset.__len__()
    
    def populateStarSet(self, s: Star):
        self.starset[s.designation] = s
        return None
    
    def populateVectorSet(self, origin: str, target: str):
        self.vectorset.append(Vector(self.starset[origin],
                                     self.starset[target],
                                     self.rgb))
        return None
    