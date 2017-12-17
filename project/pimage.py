import argparse

from face_swap import run_swap
from canny_edge import run_canny_edge
from gaussian_blur import run_gaussian_blur
from cat_face import run_cat_face
from negative import run_negative
from color import run_color
from blue_object import run_blue_object

FILTERS = {'canny_edge': run_canny_edge,
           'blur': run_gaussian_blur,
           'face_swap': run_swap,
           'cat_face': run_cat_face,
           'negative': run_negative,
           'blue_object': run_blue_object,
           'color': run_color
           }

parser = argparse.ArgumentParser(description='Simple image filters')
# parser.add_argument('filter', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')
parser.add_argument('filter', choices=FILTERS.keys(), help='Specify filter you want to use')
#parser.add_argument('color', choices=['spring', 'summer', 'winter', 'autumn', 'rainbow'])

args = parser.parse_args()

func = FILTERS[args.filter]
if args.filter == 'color':
    color = raw_input('Select coloring: spring, summer, autumn, winter, rainbow \n')
    func(color)
else:
    func()
