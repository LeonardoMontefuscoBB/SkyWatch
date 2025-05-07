import os, random, sys, unittest
root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root)
from components import Star, Vector, Constellation, Firmament


class ComponentTests(unittest.TestCase):
    def testsIfPagesAreBeingCreated(self):
        f = Firmament.create()
        f.show(3, 1, f"1.png")
        return None
    
    def testsIfVectorsAreBeingCreated(self):
        f = Firmament.create()
        for direction in range(16):
            f.show(4, direction, f"Image {direction + 1}.png")
        return None

if __name__ == "__main__": unittest.main()