"""
Functions used by image_processing.
"""
import matplotlib.pyplot as plt
from PIL import Image


def get_gray_levels(image: Image):
    """
    Returns an array of size 256
    with number of occurances of each gray level.
    """
    width, height = image.size
    pixel_map = image.load()
    levels = [0] * 256

    for x in range(width):
        for y in range(height):
            levels[pixel_map[x, y][0]] += 1

    return levels


def pdf(image: Image, gray_levels):
    """
    Probability density function.
    Returns an array of size 256
    with probability of an occurrence of each gray level.
    """
    width, height = image.size
    number_of_pixels = width * height
    pdf_values = [0] * 256

    for i, gray_lvl in enumerate(gray_levels):
        pdf_values[i] = gray_lvl / number_of_pixels

    return pdf_values


def cdf(image: Image, gray_levels):
    """
    Cumulative distribution function.
    Returns an array of size 256
    with sum of all previous pdf levels.
    """
    cdf_values = [0] * 256
    pdf_values = pdf(image, gray_levels)

    cdf_values[0] = pdf_values[0]
    for i in range(1, 256):
        cdf_values[i] = cdf_values[i-1] + pdf_values[i]

    return cdf_values


def get_summed_area(image: Image):
    """
    Returns array of size width * height
    such that:
    array[x][y] = sum( array[< x][< y] )
    """
    width, height = image.size
    pixel_map = image.load()
    sum_area = [[0] * height for i in range(width)]

    for x in range(width):
        for y in range(height):
            pixel_avg = sum(pixel_map[x, y]) // 3
            sum_area[x][y] = pixel_avg + sum_area[x-1][y] + sum_area[x][y-1] - sum_area[x-1][y-1]

    return sum_area


def save_plot(data, name):
    """
    Saves histogram for given data.
    """
    fig, ax = plt.subplots()
    ax.bar(
        range(256),
        data,
        width=1,
        edgecolor="white",
        linewidth=0.7)
    ax.set(ylim=(0, max(data)))
    plt.savefig(f'{name}.png')
