from numpy.lib.arraysetops import unique
from file import function
from PIL import Image
import numpy
from colormap import rgb2hex

def generate_colors(img):
    # convert bytes to RGB values
    rgb_img = img.convert('RGB')
    # make data contiguous for ordering purposes
    arr = numpy.ascontiguousarray(rgb_img)
    # flatten to manipulate 
    arr = arr.ravel()
    # get the unique colors of the array
    palette, unique_index = numpy.unique(arr, return_inverse=True)
    # make array 1D as opposed to ND
    palette = palette.view(arr.dtype).reshape(-1, arr.shape[-1])
    num_unique = numpy.bincount(unique_index)
    sorted = numpy.argsort(num_unique)
    palette = palette[sorted[::-1]]
    # return top 5 colors in the image
    return palette[:5]


def rgb_to_hex(palette):
    hex_codes = []
    for i in palette:
       hex_codes[i] = rgb2hex(palette[i])
    
    return hex_codes
