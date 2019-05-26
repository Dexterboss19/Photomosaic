import os

import image_slicer
import pandas as pd
from PIL import Image
from math import sqrt
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000


def create_data_frame(name, path):
    df = pd.DataFrame(columns=["red", "green", "blue", "name"])

    reds = []
    greens = []
    blues = []
    names = []

    for i, filename in enumerate(os.listdir(path)):
        r, g, b = compute_average_image_color('{}/{}'.format(path, filename))
        reds.append(r)
        greens.append(g)
        blues.append(b)
        names.append(filename)
        print('Data {} processed'.format(i))

    df["red"] = reds
    df["green"] = greens
    df["blue"] = blues
    df["name"] = names
    df.to_csv(name)

    print('Dataframe {} created'.format(names))


def resize_pictures(size_x, size_y, path_to_resize, path_to_save):
    cols, rows = get_cols_and_rows_of_slices('slices')
    temp = int((cols * rows) / 1000)
    new_size_x = size_x * temp
    new_size_y = size_y * temp
    for i, filename in enumerate(os.listdir(path_to_resize)):
        img = Image.open('{}/{}'.format(path_to_resize, filename))
        img = img.convert('RGB')
        img2 = img.resize((new_size_x, new_size_y), Image.ANTIALIAS)
        img2.save('{}/{}'.format(path_to_save, filename))
        print('{} picture(s) done'.format(i + 1))


def subdivide_photo(filename, subdivisions, path_to_save):
    tiles = image_slicer.slice(filename, subdivisions, save=False)
    image_slicer.save_tiles(tiles, directory=path_to_save)
    print('Subdivided in {} slices'.format(subdivisions))


def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i + n]


def get_cols_and_rows_of_slices(path):
    rows = []
    cols = []

    for filename in os.listdir(path):
        temp = filename.strip(".png").split("_")
        rows.append(int(temp[2]))
        cols.append(int(temp[1]))

    col_nr = max(cols)
    row_nr = max(rows)

    return col_nr, row_nr


def get_size_x_and_size_y_of_slices(path):
    img = Image.open(path + "/" + os.listdir(path)[0])
    width_of_slice, height_of_slice = img.size
    return width_of_slice, height_of_slice


def ensure_dir(directory):
    if os.path.exists(directory):
        return True
    else:
        os.makedirs(directory)
        return False


def get_size_x_and_size_y_of_resized(path):
    img = Image.open(path + "/" + os.listdir(path)[0])
    width_of_slice, height_of_slice = img.size
    return width_of_slice, height_of_slice


def compute_average_image_color(path_to_img):
    img = Image.open(path_to_img)
    width, height = img.size

    r_total = 0
    g_total = 0
    b_total = 0

    count = 0
    for x in range(0, width):
        for y in range(0, height):
            r, g, b = img.getpixel((x, y))
            r_total += r
            g_total += g
            b_total += b
            count += 1

    return int(r_total / count), int(g_total / count), int(b_total / count)


def color_distance_lab(r1, g1, b1, r2, g2, b2):
    color1_rgb = sRGBColor(r1, g1, b1)
    color2_rgb = sRGBColor(r2, g2, b2)

    color1_lab = convert_color(color1_rgb, LabColor)

    color2_lab = convert_color(color2_rgb, LabColor)

    delta_e = delta_e_cie2000(color1_lab, color2_lab)

    return delta_e


def color_distance_euclidean(r1, g1, b1, r2, g2, b2):
    delta = sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)
    return delta
