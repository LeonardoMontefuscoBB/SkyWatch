from dataclasses import dataclass
from PIL import Image, ImageDraw
from measurements import Color

@dataclass
class Table:
    def __init__(self, filepath: str):
        with open(filepath, "r") as ifile:
            self.li: list[list] = [[value
                                    for value in line.strip().split(",")]
                                    for line in ifile]
        return None
    
    def size(self):
        x: int = len(self.li)
        y: int = len(self.li[0])
        return x, y
    
    def floatsubset(self, x0: int, xn: int = 0, y0: int = 0, yn: int = 0):
        if not x0 < xn: xn = xn + self.size()[0]
        if not y0 < yn: yn = yn + self.size()[1]
        return [[float(x) for x in y[x0:xn]] for y in self.li[y0:yn]]
    
    def subset(self, x0: int, xn: int = 0, y0: int = 0, yn: int = 0):
        if not x0 < xn: xn = xn + self.size()[0]
        if not y0 < yn: yn = yn + self.size()[1]
        return [[x for x in y[x0:xn]] for y in self.li[y0:yn]]
    
    def value(self, x: int, y:int):
        return self.li[y][x]
    
    def get(self):
        return self.li

@dataclass
class Canva:
    @staticmethod
    def create(x: int = 1572, y: int = 1572):
        return Image.new("RGB", (x, y), Color.hex_to_tuple(Color.BLACK))
    
    @staticmethod
    def drawCircle(img: Image.Image, x: int, y: int, size: int, rgb: str):
        ImageDraw.Draw(img).ellipse((y - size, x - size, y + size, x + size),
                                    fill = Color.hex_to_tuple(rgb))
        return None
    
    @staticmethod
    def drawLine(img: Image.Image, x0: int, y0: int, x1: int, y1: int, size: int, rgb: str):
        ImageDraw.Draw(img).line((x0, y0, x1, y1),
                                 fill = Color.hex_to_tuple(rgb),
                                 width = size)
        return None
    