import os
from enum import Enum


class Config(Enum):
    # Path to the dataset
    DATASET_DIR = os.path.join(os.getcwd(), "datasets")
    FIGURE_DIR = os.path.join(os.getcwd(), "figures")

    DISPLAY_FIGURE = False
    NO_PROGRAM_RUNS = 15

    R_THRESHOLD = 35
    NO_ITERATIONS = 25
