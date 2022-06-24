from dataclasses import dataclass
from typing import List


@dataclass
class Segment:
    start: int
    end: int
    A: float
    B: float


@dataclass
class ExperimentConfig:
    duration: int
    cycles: int
    upper: List[Segment]
    lower: List[Segment]


DEVICE1 = "28-3c01f0957154"
DEVICE2 = "28-3c01f095d551"
RASPBERRY_PI = False
DATABASE = "pythonsqlite.db"
EXPERIMENT = {
    "1": ExperimentConfig(
        duration=24,
        cycles=28,
        upper=[
            Segment(start=0, end=5, A=-27.0 / 5, B=24),
            Segment(start=5, end=12, A=-12.0 / 7, B=39.0 / 7),
            Segment(start=12, end=16, A=-3.0 / 4, B=-6),
            Segment(start=16, end=18, A=17.0 / 2, B=-154),
            Segment(start=18, end=22, A=25.0 / 4, B=-227.0 / 2),
        ],
        lower=[
            Segment(start=0, end=3, A=-7, B=16),
            Segment(start=3, end=12, A=-17.0 / 9, B=2.0 / 3),
            Segment(start=12, end=16, A=0, B=-22),
            Segment(start=16, end=20, A=21.0 / 4, B=-106),
            Segment(start=20, end=24, A=17.0 / 4, B=-86),
        ],
    ),
    "2": ExperimentConfig(
        duration=24,
        cycles=28,
        upper=[
            Segment(start=0, end=2, A=-10, B=22),
            Segment(start=2, end=4, A=0, B=2),
            Segment(start=4, end=14, A=-3.0 / 2, B=8),
            Segment(start=14, end=16, A=0, B=-13),
            Segment(start=16, end=24, A=0, B=22),
        ],
        lower=[
            Segment(start=0, end=2, A=-10, B=18),
            Segment(start=2, end=4, A=0, B=-2),
            Segment(start=4, end=14, A=-3.0 / 2, B=4),
            Segment(start=14, end=16, A=0, B=-17),
            Segment(start=16, end=24, A=0, B=18),
        ],
    ),
    "3": ExperimentConfig(
        duration=24,
        cycles=28,
        upper=[
            Segment(start=0, end=4, A=-81.0 / 8, B=21),
            Segment(start=4, end=7, A=0, B=-39.0 / 2),
            Segment(start=7, end=11, A=81.0 / 8, B=-723.0 / 8),
            Segment(start=11, end=12, A=0, B=21),
            Segment(start=12, end=16, A=-81.0 / 8, B=-285.0 / 2),
            Segment(start=16, end=19, A=0, B=-39.0 / 2),
            Segment(start=19, end=23, A=81.0 / 8, B=-1695.0 / 8),
            Segment(start=23, end=24, A=0, B=21),
        ],
        lower=[
            Segment(start=0, end=4, A=-79.0 / 8, B=19),
            Segment(start=4, end=7, A=0, B=-41.0 / 2),
            Segment(start=7, end=11, A=79.0 / 8, B=-717.0 / 8),
            Segment(start=11, end=12, A=0, B=19),
            Segment(start=12, end=16, A=-79.0 / 8, B=275.0 / 2),
            Segment(start=16, end=19, A=0, B=-41.0 / 2),
            Segment(start=19, end=23, A=79.0 / 8, B=-1665.0 / 8),
            Segment(start=23, end=24, A=0, B=19),
        ],
    ),
}
RELAY_GPIO_PIN = 21
