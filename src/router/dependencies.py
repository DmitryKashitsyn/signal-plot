import re
from dataclasses import dataclass

from io import BytesIO

from fastapi import Depends
import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt
from sympy import sympify


RANGE_REGEX = re.compile(r'(-?\d+.?\d*):(\d+.?\d*):(-?\d+.?\d*)')

NDArrayFloat64 = npt.NDArray[np.float64]


@dataclass
class Coordinates:
    x: NDArrayFloat64
    y: NDArrayFloat64


def save_svg(image_bytes: BytesIO):
    with open('aboba.svg', 'wb') as svg_file:
        svg_file.write(image_bytes.getvalue())


def plot_return_svg_bytes(
    x: NDArrayFloat64,
    y: NDArrayFloat64,
    timestep: float | None = None,
    discrete: bool = False,
):
    fig, ax = plt.subplots()
    if discrete:
        for idx, x_val in enumerate(x):
            if timestep:
                ax.set_title("Discrete magnitude spectrum")
                ax.set_xlabel("Frequency")
                ax.set_ylabel("Magnitude (energy)")
            else:
                ax.set_title("Signal")
                ax.set_xlabel("Time (s)")
                ax.set_ylabel("Amplitude")
            ax.plot([x_val, x_val], [0, y[idx]], 'bo-', markersize=2, linewidth=1)
    else:
        if timestep:
            ax.set_title("Magnitude spectrum")
            ax.magnitude_spectrum(y, Fs=timestep)
        else:
            ax.set_title("Signal")
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Amplitude")
            ax.plot(x, y)
    image_bytes = BytesIO()
    plt.savefig(image_bytes, format="svg", backend="svg")
    save_svg(image_bytes)

    return image_bytes.getvalue()


def get_range_from_range_string(x_range: str):
    start, step, finish = [float(match) for match in re.findall(RANGE_REGEX, x_range)[0]]
    x_vals: list[float] = []
    for i in np.arange(start, finish, step):
        x_vals.append(i)
    print(x_vals)
    return np.array(x_vals, np.float64)


def get_formula_from_string(formula: str):
    return sympify(formula)


def get_coordinates_from_formula_and_range(
    x: NDArrayFloat64 = Depends(get_range_from_range_string),
    formula: any = Depends(get_formula_from_string),
):
    y = np.array([formula.subs('x', x_val) for x_val in x], np.float64)
    return Coordinates(x, y)


def get_graph(
    coordinates: Coordinates = Depends(get_coordinates_from_formula_and_range),
    discrete: bool = False,
):
    x, y = coordinates.x, coordinates.y
    # style = discrete_style if discrete else ""
    return plot_return_svg_bytes(x, y, discrete=discrete)


def get_spectrum(
    coordinates: Coordinates = Depends(get_coordinates_from_formula_and_range),
    discrete: bool = False,
):
    x, y = coordinates.x, coordinates.y
    y = np.fft.fft(y)
    timestep = float(1/(x[1] - x[0]))
    x = np.fft.fftfreq(x.size, timestep)
    # style = discrete_style if discrete else ""
    return plot_return_svg_bytes(x, y, timestep, discrete)
