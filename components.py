from dataclasses import dataclass
from math import pi as PI
import os
from measurements import Color, Matrix
from utilities import Canvas, Table

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
        self.rgb_des:       str   = Star.designationColor(designation)
        self.size:          float = Star.starSize(self.magnitude)
        return None
    
    @staticmethod
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
    
    @staticmethod
    def starSize(magnitude: float):
        if   magnitude < 0.8: return 10.0
        elif magnitude < 0.0: return  8.0
        elif magnitude < 1.2: return  6.0
        elif magnitude < 2.0: return  5.0
        elif magnitude < 3.0: return  4.0
        elif magnitude < 5.0: return  2.0
        elif magnitude < 6.0: return  1.0
        return 0.5
    
    def rotate(self, R: Matrix = Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])):
        v = Matrix.Vector(self.x, self.y, self.z)
        # print(R.M)
        # print(v.M)
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
    
    def populateVectorSet(self, origin: Star, target: Star):
        self.vectorset.append(Vector(origin,
                                     target,
                                     self.rgb))
        return None
    
    def get(self, designation: str):
        return self.starset[designation]

@dataclass
class Firmament:
    def __init__(self, stars: Table, vectors: Table, constellations: Table):
        self.set: dict[int, Constellation] = {}
        self.populateConstellations(constellations)
        self.populateStars(stars)
        self.populateVectors(vectors)
        return None
    
    @staticmethod
    def create():
        cur_folder = os.path.dirname(__file__)
        return Firmament(Table(f"{cur_folder}/data/stellar-catalogue.csv"),
                         Table(f"{cur_folder}/data/vectoral-catalogue.csv"),
                         Table(f"{cur_folder}/data/aggregational-catalogue.csv"))
        
    def populateConstellations(self, dataset: Table):
        for c in dataset: self.set[int(c[0])] = Constellation(*c)
        return None
    
    def populateStars(self, dataset: Table):
        for s in dataset: self.set[int(s[1])].populateStarSet(Star(*s))
        return None
    
    def populateVectors(self, dataset: Table):
        for v in dataset:
            origin = self.set[int(v[1])].get(v[2])
            target = self.set[int(v[3])].get(v[4])
            self.set[int(v[0])].populateVectorSet(origin, target)
        return None
    
    def show(self, option: int = 0, reference: int = -1, filename: str = "out.png"):
        match option:
            case 0: self.showRealistic(reference, filename)
            case 1: self.showConstellation(reference, filename)
            case 2: self.showDesignation(reference, filename)
            case 3: self.showPages(reference, filename)
        return None
    
    def showRealistic(self, reference: int, filename: str):
        if reference < 0: return None
        R = self.set[reference].R
        img = Canvas.create()
        for c in self.set.values():
            for s in c.starset.values():
                rgb = s.rgb
                s.rotate(R)
                if s.position():
                    x, y = s.position()
                    size = s.size
                    Canvas.drawCircle(img, x, y, size, str, rgb)
        img.save(f"{os.path.dirname(__file__)}/{filename}")
        return None
    
    def showConstellation(self, reference: int, filename: str):
        if reference < 0: return None
        R = self.set[reference].R
        img = Canvas.create()
        for c in self.set.values():
            rgb = c.rgb
            for s in c.starset.values():
                s.rotate(R)
                if s.position():
                    x, y = s.position()
                    size = s.size
                    Canvas.drawCircle(img, x, y, size, str, rgb)
        img.save(f"{os.path.dirname(__file__)}/{filename}")
        return None
    
    def showDesignation(self, reference: int, filename: str):
        if reference < 0: return None
        R = self.set[reference].R
        img = Canvas.create()
        for c in self.set.values():
            for s in c.starset.values():
                if c.cindex == reference: rgb = s.rgb_des
                else: rgb = Color.WHITE
                s.rotate(R)
                if s.position():
                    x, y = s.position()
                    size = s.size
                    Canvas.drawCircle(img, x, y, size, str, rgb)
        img.save(f"{os.path.dirname(__file__)}/{filename}")
    
    def showPages(self, reference: int, filename: str):
        from PIL import Image
        if reference < 0: return None
        R = [[[1,0,0],[0,0,1],[0,-1,0]],
             [[0.5,0.866025403784,0],[0,0,1],[0.866025403784,-0.5,0]],
             [[-0.5,0.866025403784,0],[0,0,1],[0.866025403784,0.5,0]],
             [[-1,0,0],[0,0,1],[0,1,0]],
             [[-0.5,-0.866025403784,0],[0,0,1],[-0.866025403784,0.5,0]],
             [[0.5,-0.866025403784,0],[0,0,1],[-0.866025403784,-0.5,0]],
             [[0.57735026919,0.57735026919,0.57735026919],[-0.707106781187,0,0.707106781187],[0.408248290464,-0.816496580928,0.408248290464]],
             [[-0.57735026919,0.57735026919,0.57735026919],[0.707106781187,0,0.707106781187],[0.408248290464,0.816496580928,-0.408248290464]],
             [[-0.57735026919,-0.57735026919,0.57735026919],[0.707106781187,0,0.707106781187],[-0.408248290464,0.816496580928,0.408248290464]],
             [[0.57735026919,-0.57735026919,0.57735026919],[-0.707106781187,0,0.707106781187],[-0.408248290464,-0.816496580928,-0.408248290464]],
             [[0.57735026919,0.57735026919,-0.57735026919],[0.707106781187,0,0.707106781187],[0.408248290464,-0.816496580928,-0.408248290464]],
             [[-0.57735026919,0.57735026919,-0.57735026919],[-0.707106781187,0,0.707106781187],[0.408248290464,0.816496580928,0.408248290464]],
             [[-0.57735026919,-0.57735026919,-0.57735026919],[-0.707106781187,0,0.707106781187],[-0.408248290464,0.816496580928,-0.408248290464]],
             [[0.57735026919,-0.57735026919,-0.57735026919],[0.707106781187,0,0.707106781187],[-0.408248290464,-0.816496580928,0.408248290464]],
             [[0,0,1],[-1,0,0],[0,-1,0]],
             [[0,0,-1],[1,0,0],[0,-1,0]]][reference]
        img = Image.new("RGB", (1572, 1572), Color.hex_to_tuple(Color.WHITE))
        for c in self.set.values():
            for s in c.starset.values():
                rgb = Color.BLACK
                s.rotate(Matrix(R))
                if s.position():
                    x, y = s.position()
                    size = s.size
                    Canvas.drawCircle(img, x, y, size, str, rgb)
        img.save(f"{os.path.dirname(__file__)}/{filename}")
        return None