import os

from config import Config
from src.ransac import RANSAC


def main() -> None:
    ransac = RANSAC("RANSACdata16.txt")
    ransac.run()


if __name__ == "__main__":
    main()
