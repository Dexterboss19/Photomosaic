# Python-Photomosaic
A python script (actually 2) that can create a Photomosaic
### Prerequisites
image_slicer, pandas, numpy, colormath, cv2
```
pip install image_slicer pandas numpy colormath opencv-python
```
### How to use
1. put the photo you want to make the mosaic out of in the same folder as the 2 .py files
2. make a folder with the photos you want to use as part of the mosaic (> 3000 Photos for a better result) in the same folder as step 1
3. navigate in cmd to the folder with the 2 .py files in it
4. run the createMosaic.py with the following arguments: file_that_you _want_to_make_to_a_mosaic.jpg number_of_slices folder_of_tiles 1-4* 0-1**

\* 1 for euclidean with repetiton of tiles (fast)

\* 2 for euclidean without repetiton of tiles (fast)

\* 3 for cielab with repetiton of tiles (slow)

\* 4 for cielab without repetiton of tiles (slow)

** 1 will make the normal mosaic and one with the normal picture as an overlay

** 0 will not make the overlay

Example:
```
python createMosaic.py Photo.jpg 3000 folder_of_tiles 2 1
```

### Examples
