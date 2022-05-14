"""
Functions for modifying images.
"""
from PIL import Image
from image_functions import *


def singleThreshold(image: Image, threshold: int):
    """
    Converts given image to black & white
    using single threshold.
    """
    width, height = image.size()
    pixel_map = image.load()

    for x in range(width):
        for y in range(height):
            if sum(pixel_map[x, y])/3 > threshold:
                pixel_map[x, y] = (255, 255, 255)
            else:
                pixel_map[x, y] = (0, 0, 0)


def doubleThreshold(image: Image, lower_threshold: int, upper_threshold: int):
    """
    Converts given image to black & white
    using double threshold.
    """
    width, height = image.size
    pixel_map = image.load()

    for x in range(width):
        for y in range(height):
            if upper_threshold > sum(pixel_map[x, y])/3 > lower_threshold:
                pixel_map[x, y] = (255, 255, 255)
            else:
                pixel_map[x, y] = (0, 0, 0)


def to_grayscale(image: Image):
    """
    Converts given image to grayscale
    using average value of RGB for each pixel.
    """
    width, height = image.size
    pixel_map = image.load()

    for x in range(width):
        for y in range(height):
            pixel_map[x, y] = (sum(pixel_map[x, y]) // 3, ) * 3


def to_gray_enchance_constarst(image: Image, save_histograms=False):
    """
    Converts given image to grayscale
    and enchances contrast using
    cumulative distribution function.
    """
    to_grayscale(image)
    gray_levels = get_gray_levels(image)

    if save_histograms:
        save_plot(gray_levels, 'hist_before')

    new_levels = [int(x * 255) for x in cdf(image, gray_levels)]
    width, height = image.size
    pixel_map = image.load()

    for x in range(width):
        for y in range(height):
            pixel_map[x, y] = (new_levels[pixel_map[x, y][0]], ) * 3

    if save_histograms:
        save_plot(get_gray_levels(image), 'hist_after')


def mean_filter(image: Image):
    """
    Converts image to grayscale
    and applies mean filter
    with square mask of size 71x71.
    """
    to_grayscale(image)
    mask_size = 71
    half_mask = (mask_size // 2)
    sum_area = get_summed_area(image)

    width, height = image.size
    pixel_map = image.load()

    for x in range(half_mask + 1, width - half_mask):
        for y in range(half_mask + 1, height - half_mask):
            pixel_sum = sum_area[x+half_mask][y+half_mask] - \
                        sum_area[x-half_mask][y+half_mask] - \
                        sum_area[x+half_mask][y-half_mask] + \
                        sum_area[x-half_mask][y-half_mask]
            pixel_map[x, y] = (pixel_sum // (mask_size ** 2), ) * 3
