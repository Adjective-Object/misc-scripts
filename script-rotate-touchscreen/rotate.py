#!/usr/bin/env python3
import subprocess as sp
import re
import sys
import itertools as it
from functools import reduce

DEVICE_ID=14
TRANSFORM_PROP_ID=140

rotate_anticlockwise=[0, 1, 0, -1, 0, 1, 0, 0, 1]


class Screen():
    def __init__(self, width, height, xoff, yoff):
        self.width = width
        self.height = height
        self.x = xoff
        self.y = yoff

    def __repr__(self):
        return "<Screen %sx%s @ %sx%s>" % (
            self.width,
            self.height,
            self.x,
            self.y,
        )


rect_regex = re.compile(r'(\d+)x(\d+)\+(\d+)\+(\d+)')
def parse_rect(rect_string):
    match = rect_regex.match(rect_string)
    groups = [int(x) for x in match.groups()]
    return Screen(
        groups[0],
        groups[1],
        groups[2],
        groups[3]
    )


def fetch_screens():
    proc = sp.run(['xrandr'], stdout=sp.PIPE)

    if proc.returncode != 0:
        print("error fetching screen from xrandr")
        return {}

    lines = str(proc.stdout).split("\\n")
    screens = {}
    for line in lines:
        if " connected " in line:
            fields = line.split(" ")
            screens[fields[0]] = parse_rect(fields[2])

    return screens


def join_screens(screens):
    width, height = 0, 0
    for screen in screens:
        width = max(width, screen.x + screen.width)
        height = max(height, screen.y + screen.height)

    return Screen(width, height, 0, 0)


def get_scale_transform(screen, union):
    scale_x = float(screen.width) / union.width
    scale_y = float(screen.height) / union.width

    translate_x = screen.x / union.width
    translate_y = screen.y / union.height

    return [
        scale_x, 0, 0, # translate_x / scale_x,
        0, 1, 0, # translate_y / scale_y,
        0, 0, 1
    ]


def multiply_transforms(a, b):
    # 0  1  2
    # 3  4  5
    # 6  7  8

    a_ranges = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]
    ]
    b_ranges = [
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8]
    ]

    ranges = [
        zip(a_ranges[ar], b_ranges[br])
        for (ar, br) in it.product(range(3), range(3))
    ]

    return [
        sum((a[first] * b[second] for (first, second) in r))
        for r in ranges
    ]


def rotate_display(device, orientation):
    sp.call(['xrandr', '-o', orientation])

def transform_touchscreen(device, transform):
    sp.call(['xinput', 'set-prop', device, '140'] + [str(x) for x in transform])

def main(argv):
    screen = 'eDP1'
    touchscreen = 'Atmel Atmel maXTouch Digitizer'
    touchpad = 'SynPS/2 Synaptics TouchPad'
    orientation = sys.argv[1]

    screens = fetch_screens()
    union = join_screens(screens.values())

    if screen not in screens.keys():
        print("%s not in found screens (%s)" % (
            screen,
            ", ".join(screens.keys())
        ))
        return 1

    scale_transform = get_scale_transform(screens[screen], union);

    num_rotations = 0
    if orientation == "right":
        num_rotations = 1
    if orientation == "inverted":
        num_rotations = 2
    if orientation == "left":
        num_rotations = 3

    transform = reduce(
        lambda x, y: multiply_transforms(x, y),
        [rotate_anticlockwise] * num_rotations,
        scale_transform,
    )

    rotate_display(screen, orientation)
    transform_touchscreen(touchpad, transform)
    transform_touchscreen(touchscreen, transform)

if __name__ == "__main__":
    main(sys.argv)

