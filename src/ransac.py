import os
from typing import Callable

import numpy as np
from matplotlib import pyplot as plt

from config import Config
from src.node import Node


class RANSAC:
    __filename: str
    __points: list[Node]
    __inliers: list[Node]
    __outliers: list[Node]

    def __init__(self, filename: str) -> None:
        filepath = os.path.join(Config.DATASET_DIR.value, filename)
        self.__filename = filename[:-4]

        self.points = []
        self.inliers = []
        self.outliers = []

        with open(filepath, "r") as file:
            lines = file.readlines()
            for line in lines:
                x, y = line.split()
                self.points.append(Node(float(x), float(y)))

        print(f"Loaded {len(self.points)} points from {filename}.")

    @property
    def points(self) -> list[Node]:
        return self.__points

    @points.setter
    def points(self, points: list[Node]) -> None:
        self.__points = points

    @property
    def inliers(self) -> list[Node]:
        return self.__inliers

    @inliers.setter
    def inliers(self, inliers: list[Node]) -> None:
        self.__inliers = inliers

    @property
    def outliers(self) -> list[Node]:
        return self.__outliers

    @outliers.setter
    def outliers(self, outliers: list[Node]) -> None:
        self.__outliers = outliers

    def run(self) -> None:
        for i in range(1, Config.NO_PROGRAM_RUNS.value + 1):
            for _ in range(Config.NO_ITERATIONS.value):
                inliers = []
                outliers = []

                p1, p2, p3 = self.__select_random_points()
                R, dist_from_center = RANSAC.dist_from_center(p1=p1, p2=p2, p3=p3)
                for point in self.points:
                    d = dist_from_center(point.x, point.y)
                    if R - Config.R_THRESHOLD.value <= d <= R + Config.R_THRESHOLD.value:
                        inliers.append(point)
                    else:
                        outliers.append(point)

                if len(inliers) > len(self.inliers):
                    self.inliers = inliers
                    self.outliers = outliers

            print(f"Found {len(self.inliers)} inliers and {len(self.outliers)} outliers.")
            x_inliers = np.array([point.x for point in self.inliers])
            y_inliers = np.array([point.y for point in self.inliers])

            x_outliers = np.array([point.x for point in self.outliers])
            y_outliers = np.array([point.y for point in self.outliers])

            title = os.path.join(Config.FIGURE_DIR.value, f"{self.__filename}_{i}")

            plt.plot(x_inliers, y_inliers, "o", color="blue", label=f"Inliers: {len(self.inliers)}")
            plt.plot(x_outliers, y_outliers, "o", color="red", label=f"Outliers: {len(self.outliers)}")
            plt.title(f"RANSAC - Iteration {i}")
            plt.legend()
            plt.savefig(title, dpi=400)

            if Config.DISPLAY_FIGURE.value:
                plt.show()
            else:
                plt.close()

    def __select_random_points(self) -> tuple[Node, Node, Node]:
        return tuple(np.random.choice(self.points, 3, replace=False))

    @staticmethod
    def dist_from_center(p1: Node, p2: Node, p3: Node) -> tuple[float, Callable[[float, float], float]]:
        a = np.array(
            [
                [p1.x - p2.x, p1.y - p2.y],
                [p3.x - p2.x, p3.y - p2.y]
            ]
        )

        b = np.array(
            [
                (p1.x ** 2 - p2.x ** 2 + p1.y ** 2 - p2.y ** 2) / 2,
                (p3.x ** 2 - p2.x ** 2 + p3.y ** 2 - p2.y ** 2) / 2
            ]
        )

        center = np.linalg.solve(a, b)
        radius = np.sqrt((p1.x - center[0]) ** 2 + (p1.y - center[1]) ** 2)

        return radius, lambda x, y: (x - center[0]) ** 2 + (y - center[1]) ** 2 - radius ** 2
