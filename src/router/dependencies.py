from io import BytesIO

import numpy as np
import matplotlib.pyplot as plt

discrete = "bo--"


def save_svg(image_bytes: BytesIO):
    with open('aboba.svg', 'wb') as svg_file:
        svg_file.write(image_bytes.getvalue())


def get_graph(x: list[int], y: list[int]):
    fig, ax = plt.subplots()
    ax.plot(x, y, discrete)

    image_bytes = BytesIO()
    plt.savefig(image_bytes, format="svg", backend="svg")
    save_svg(image_bytes)
    return image_bytes.getvalue()


def get_spectrum(x: list[int], y: list[int]):
    fig, ax = plt.subplots()
    ax.plot(x, y, discrete)



if __name__ == '__main__':
    x_vals = [0, 0, 1, 2, 2, 3, 4, 4]
    y_vals = [0, 1, 1, 1, 0, 0, 0, 1]
    get_graph(x_vals, y_vals)
