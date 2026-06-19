class Punto:
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self._x = x
        self._y = y

    def getX(self) -> float:
        return self._x

    def setX(self, x: float):
        self._x = x

    def getY(self) -> float:
        return self._y

    def setY(self, y: float):
        self._y = y

    def __str__(self) -> str:
        return f"({self._x}, {self._y})"
