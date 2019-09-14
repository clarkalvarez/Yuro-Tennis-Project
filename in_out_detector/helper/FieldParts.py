#!/bin/env python3

import cv2
import numpy as np


def get_boundary_doubles(x, y):
    return [(x[0], y[0]), (x[2], y[2]), (x[18], y[18]), (x[16], y[16])]


def get_boundary_singles(x, y):
    return [(x[3], y[3]), (x[7], y[7]), (x[15], y[15]), (x[11], y[11])]


def get_boundary_doubles_left(x, y):
    return [(x[0], y[0]), (x[1], y[1]), (x[17], y[17]), (x[16], y[16])]


def get_boundary_doubles_right(x, y):
    return [(x[1], y[1]), (x[2], y[2]), (x[18], y[18]), (x[17], y[17])]


def get_boundary_singles_left(x, y):
    return [(x[3], y[3]), (x[5], y[5]), (x[13], y[13]), (x[11], y[11])]


def get_boundary_singles_right(x, y):
    return [(x[5], y[5]), (x[7], y[7]), (x[15], y[15]), (x[13], y[13])]