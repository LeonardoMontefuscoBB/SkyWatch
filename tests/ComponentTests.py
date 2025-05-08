import os, random, sys, unittest
root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root)
from components import Star, Vector, Constellation, Firmament


class ComponentTests(unittest.TestCase):
    def testsIfPrintablePagesAreBeingCreated(self):
        f = Firmament.create()
        for page in range(16):
            f.show(3, page, f"Page {'0' if page < 9 else ''}{page + 1}.png")
        return None
    
    def testsIfVectorsAreBeingCreated(self):
        f = Firmament.create()
        for direction in range(16):
            f.show(4, direction, f"Image {'0' if direction < 9 else ''}{direction + 1}.png")
        return None

if __name__ == "__main__": unittest.main()