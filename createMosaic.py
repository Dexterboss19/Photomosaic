import sys

import cv2
import pandas as pd
from PIL import Image
import createAssets
from numpy import zeros_like, uint8, array

mosaic = []
not_used = []

slicesPath = 'slices'
resizePath = 'resized'

imgMosaic = None


def main(args):
    dir_path = args[3]
    createAssets.dirPath = dir_path
    file_name = args[1]
    nr_of_subdivisions = int(args[2])
    methode = int(args[4])
    overlayArg = int(args[5])

    if overlayArg == 1:
        overlay = True
    else:
        overlay = False

    if not createAssets.ensure_dir(slicesPath):
        createAssets.subdivide_photo(file_name, nr_of_subdivisions, slicesPath)
        createAssets.create_data_frame('dataSlices.csv', slicesPath)

    sizeX, sizeY = createAssets.get_size_x_and_size_y_of_slices(slicesPath)

    if not createAssets.ensure_dir(resizePath):
        createAssets.resize_pictures(sizeX, sizeY, dir_path, resizePath)
        createAssets.create_data_frame('dataResized.csv', resizePath)

    data_slices = pd.read_csv('dataSlices.csv', sep=",")
    data_resized = pd.read_csv('dataResized.csv', sep=",")

    reds_resized = data_resized["red"].tolist()
    greens_resized = data_resized["green"].tolist()
    blues_resized = data_resized["blue"].tolist()
    names_resized = data_resized["name"].tolist()

    reds_slices = data_slices["red"].tolist()
    greens_slices = data_slices["green"].tolist()
    blues_slices = data_slices["blue"].tolist()

    for _ in range(len(reds_resized)):
        not_used.append(True)

    cols, rows = createAssets.get_cols_and_rows_of_slices(slicesPath)

    for _ in range(cols * rows):
        mosaic.append("")

    if methode is 1:
        calculate_mosaic_euclidean_rep(cols * rows, len(reds_resized), names_resized, reds_resized, greens_resized,
                                       blues_resized, reds_slices, greens_slices, blues_slices)
        methode_string = 'RGB_Repetition'
    elif methode is 2:
        calculate_mosaic_euclidean_no_rep(cols * rows, len(reds_resized), names_resized, reds_resized, greens_resized,
                                          blues_resized, reds_slices, greens_slices, blues_slices)
        methode_string = 'RGB_No_Repetition'
    elif methode is 3:
        calculate_mosaic_lab_rep(cols * rows, len(reds_resized), names_resized, reds_resized, greens_resized,
                                 blues_resized, reds_slices, greens_slices, blues_slices)
        methode_string = 'CIELAB_Repetition'
    else:
        calculate_mosaic_lab_no_rep(cols * rows, len(reds_resized), names_resized, reds_resized, greens_resized,
                                    blues_resized, reds_slices, greens_slices, blues_slices)
        methode_string = 'CIELAB_No_Repetition'

    name = '{}_{}.jpg'.format(methode_string, (cols * rows))
    nameOverlay = '{}_{}_Overlay.png'.format(methode_string, (cols * rows))
    imgMosaic = create_mosaic(name, cols, rows, resizePath)

    if overlay:
        img = Image.open(file_name)
        size_x, size_y = img.size
        img2 = imgMosaic.resize((size_x, size_y), Image.ANTIALIAS)
        create_overlay(nameOverlay, img2, file_name)


def calculate_mosaic_euclidean_no_rep(nr_of_subdivisions, nr_of_tiles, name_r, reds_r, greens_r, blues_r,
                                      reds_s, greens_s, blues_s):
    temp = True

    print('Calculating mosaic')
    for i in range(nr_of_subdivisions):
        temp1 = 1000
        index = 0

        if i > nr_of_tiles and temp is True:
            for x in range(len(name_r)):
                not_used[x] = True
            temp = False

        for j in range(nr_of_tiles):
            if not_used[j]:
                temp2 = createAssets.color_distance_euclidean(reds_r[j], greens_r[j], blues_r[j],
                                                              reds_s[i], greens_s[i], blues_s[i])

                if temp2 < temp1:
                    temp1 = temp2
                    index = j
                else:
                    continue
            else:
                continue

        mosaic[i] = name_r[index]
        not_used[index] = False
        print('Slice {} done'.format(i + 1))

    print('Mosaic calculated')


def calculate_mosaic_lab_no_rep(nr_of_subdivisions, nr_of_tiles, name_r, reds_r, greens_r, blues_r,
                                reds_s, greens_s, blues_s):
    temp = True
    print('Calculating mosaic')
    for i in range(nr_of_subdivisions):
        temp1 = 1000
        index = 0

        if i > nr_of_tiles and temp is True:
            for x in range(len(name_r)):
                not_used[x] = True
            temp = False

        for j in range(nr_of_tiles):
            if not_used[j]:
                temp2 = createAssets.color_distance_lab(reds_r[j], greens_r[j], blues_r[j],
                                                        reds_s[i], greens_s[i], blues_s[i])

                if temp2 < temp1:
                    temp1 = temp2
                    index = j
                else:
                    continue
            else:
                continue

        mosaic[i] = name_r[index]
        not_used[index] = False

        print('Slice {} done'.format(i + 1))

    print('Mosaic calculated')


def calculate_mosaic_euclidean_rep(nr_of_subdivisions, nr_of_tiles, name_r, reds_r, greens_r, blues_r,
                                   reds_s, greens_s, blues_s):
    print('Calculating mosaic')
    for i in range(nr_of_subdivisions):
        temp1 = 1000
        index = 0
        for j in range(nr_of_tiles):
            temp2 = createAssets.color_distance_euclidean(reds_r[j], greens_r[j], blues_r[j],
                                                          reds_s[i], greens_s[i], blues_s[i])

            if temp2 < temp1:
                temp1 = temp2
                index = j
            else:
                continue

        mosaic[i] = name_r[index]
        print('Slice {} done'.format(i + 1))

    print('Mosaic calculated')


def calculate_mosaic_lab_rep(nr_of_subdivisions, nr_of_tiles, name_r, reds_r, greens_r, blues_r,
                             reds_s, greens_s, blues_s):
    print('Calculating mosaic')
    for i in range(nr_of_subdivisions):
        temp1 = 1000
        index = 0
        for j in range(nr_of_tiles):
            temp2 = createAssets.color_distance_lab(reds_r[j], greens_r[j], blues_r[j],
                                                    reds_s[i], greens_s[i], blues_s[i])

            if temp2 < temp1:
                temp1 = temp2
                index = j
            else:
                continue

        mosaic[i] = name_r[index]
        print('Slice {} done'.format(i + 1))

    print('Mosaic calculated')


def create_mosaic(name, cols, rows, resize_path):
    print('Creating mosaic')

    new_mosaic = list(createAssets.chunks(mosaic, rows))

    size_x, size_y = createAssets.get_size_x_and_size_y_of_resized(resize_path)

    new_im = Image.new('RGB', (size_x * (cols - 1), size_y * (rows - 1)))

    for x in range(cols):
        for y in range(rows):
            print('Building X: {} Y: {} done'.format(x, y))
            try:
                img = Image.open('{}/{}'.format(resize_path, new_mosaic[x][y]))
            except IndexError:
                print("Error")
                img = None
            new_im.paste(img, (y * size_x, x * size_y))

    new_im.save(name)

    print('Mosaic made and saved as {}'.format(name))

    return new_im


def create_overlay(name, photo1, photo2):
    pil_image = photo1

    a = cv2.imread(photo2, cv2.IMREAD_UNCHANGED)
    b = cv2.cvtColor(array(pil_image), cv2.COLOR_RGB2BGR)

    a = a.astype(float) / 255
    b = b.astype(float) / 255  # make float on range 0-1

    mask = a >= 0.5  # generate boolean mask of everywhere a > 0.5
    ab = zeros_like(a)  # generate an output container for the blended image

    # now do the blending
    ab[~mask] = (2 * a * b)[~mask]  # 2ab everywhere a<0.5
    ab[mask] = (1 - 2 * (1 - a) * (1 - b))[mask]  # else this

    x = (ab * 255).astype(uint8)
    cv2.imwrite(name, x)

    print('Overlay mosaic made and saved as {}'.format(name))


if __name__ == '__main__':
    main(sys.argv)
