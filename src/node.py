class Node:
    __x: float
    __y: float

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    @property
    def x(self) -> float:
        return self.__x

    @x.setter
    def x(self, x: float) -> None:
        self.__x = x

    @property
    def y(self) -> float:
        return self.__y

    @y.setter
    def y(self, y: float) -> None:
        self.__y = y

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"
