import argparse
import os
import random
import numpy as np
import drawSvg as draw

from img_utils import Element, Translation, RoseTrans, Scale

W, H = 1080, 1920
FLOWER_COL = '#AD12E6'
BACKGROUND_COL ='#A9BBC6'

def bezier_from_array(a):
    result_svg = draw.Path(transform='', stroke_width=4, stroke=FLOWER_COL, fill='none', id='line_svg')
    d = "M {},{} C {},{} {},{} {},{}".format(*a)
    result_svg.args['d'] = d
    return result_svg


def beziers_line(a1, a2, size=10):
    a_gradient = np.linspace(a1, a2, num=size)
    results = []
    for a in a_gradient:
        results.append(bezier_from_array(a))

    return results


def generate_input_imgs(out_dir, size=10, steps=100, stop_points=1):
    os.makedirs(out_dir, exist_ok=True)

    size_modifier = 2.2

    grad_1 = np.linspace(np.random.rand(8) * 100 * size_modifier, np.random.rand(8) * 100 * size_modifier, num=steps)

    for i in range(stop_points - 1):
        grad_1 = np.append(grad_1, np.linspace(grad_1[-1], np.random.rand(8) * 100 * size_modifier, num=steps), axis=0)

    grad_1 = np.append(grad_1, np.linspace(grad_1[-1], grad_1[0], num=steps), axis=0)
    grad_2 = np.roll(grad_1, 1, axis=0)
    positions = np.linspace(-600, 600, num=size) - 150

    for i in range(steps * (stop_points + 1)):

        filename = "{:04d}".format(i)
        print(filename)
        sur = draw.Drawing(W, H, origin='center', displayInline=False)
        sur.append(draw.Rectangle(-W / 2, -H / 2, W, H, fill=BACKGROUND_COL))
        line = beziers_line(grad_1[i], grad_2[i], size=size)
        for y, svg_elem in enumerate(line):
            elem = RoseTrans(3 * (y + 2), 100, 100)(Element(svg_elem))
            elem = Scale(1.5)(elem)
            elem = Translation(-150, positions[y])(elem)
            elem.draw(sur)
            sur.savePng(os.path.join(out_dir, filename + '.png'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dest_dir',  help='directory for bezier imgs', type=str, default='data/input_imgs/3')
    args = parser.parse_args()

    generate_input_imgs(args.dest_dir, size=4, steps=2, stop_points=4)
