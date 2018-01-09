import argparse

from project.face_swap.py import run_swap
from project.canny_edge.py import run_canny_edge
from project.gaussian_blur.py import run_gaussian_blur
from project.cat_face import run_cat_face
from project.negative import run_negative
from project.color import run_color

FILTERS = {'canny_edge': run_canny_edge(),
           'blur': run_gaussian_blur(),
           'face_swap': run_swap(),
           'cat_face': run_cat_face(),
           'negative': run_negative(),
           'color': run_color(),
           }

parser = argparse.ArgumentParser(description='Simple image filters')
# parser.add_argument('filter', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')
parser.add_argument('filter', type=str, help='Specify filter you want to use')

args = parser.parse_args()

func = FILTERS[args.filter]
func()
