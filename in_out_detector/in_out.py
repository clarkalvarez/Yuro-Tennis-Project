#!/bin/env python3

import cv2
import sys
import numpy as np

sys.path.append("")

from in_out_detector.helper import FieldParts
from in_out_detector.helper import Visualize
from in_out_detector.helper.TrackBar import TrackBar
from in_out_detector.helper import Utils

lower_hsv = (0, 34, 143)
upper_hsv = (21, 176, 255)
line_conf = (80, 165, 14)
ANGLE_TOLERANCE = 5  # percentage (%)

region_split_x = (17, 40, 60, 83)  # percentage (%)
region_split_y = (22, 41, 65, 85)  # percentage (%)


def main():
    IMAGE = "tenniscourt/orangecourt.jpg"
    tb = TrackBar(lower_hsv, upper_hsv, line_conf,
                  ANGLE_TOLERANCE, region_split_x, region_split_y)
    tb.set_track_bar()

    image = cv2.imread(IMAGE)
    black = np.zeros(image.shape, dtype=np.uint8)

    image1 = image.copy()

    while True:
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        lower, higher, line_settings, angle_tolerance, split_x, split_y = tb.get_track_bar()
        angle_tolerance /= 10.0

        threshold = cv2.inRange(hsv, lower, higher)

        black_img, lines = Utils.get_boundaries(threshold, line_settings)
        line90, line0 = Utils.get_perpendicular_lines(lines, tolerance=angle_tolerance)
        points = Utils.get_intersection(line90, line0)
        x_points, y_points = Utils.get_regions(image, split_x, split_y)
        points_x, points_y = Utils.get_corner_points(black_img, points, split_x, split_y)

        boundary_doubles = FieldParts.get_boundary_doubles(points_x, points_y)
        boundary_singles = FieldParts.get_boundary_singles(points_x, points_y)

        boundary_doubles_left = FieldParts.get_boundary_doubles_left(points_x, points_y)
        boundary_doubles_right = FieldParts.get_boundary_doubles_right(points_x, points_y)

        boundary_singles_left = FieldParts.get_boundary_singles_left(points_x, points_y)
        boundary_singles_right = FieldParts.get_boundary_singles_right(points_x, points_y)

        # line_black = Visualize.draw_lines(black_img, line90, line0)
        # region_image = Visualize.draw_regions(image, x_points, y_points)

        final_image = Visualize.draw_boundary(image1, black, boundary_doubles_left,
                                              color=(120, 120, 0), thickness=2,
                                              fade=0.4, boundary=False, area=True)
        final_image = Visualize.draw_boundary(final_image, black, boundary_doubles_right,
                                              color=(0, 120, 120), thickness=2,
                                              fade=0.4, boundary=False, area=True)
        final_image = Visualize.draw_boundary(final_image, black, boundary_singles_left,
                                              color=(0, 50, 160), thickness=2,
                                              fade=0.6, boundary=False, area=True)
        final_image = Visualize.draw_boundary(final_image, black, boundary_singles_right,
                                              color=(160, 50, 0), thickness=2,
                                              fade=0.6, boundary=False, area=False)
        final_image = Visualize.draw_boundary(final_image, black, boundary_doubles,
                                              color=(0, 0, 255), thickness=2,
                                              fade=0.1, boundary=True, area=True)
        final_image = Visualize.draw_boundary(final_image, black, boundary_singles,
                                              color=(255, 0, 0), thickness=2,
                                              fade=0.1, boundary=True, area=True)

        cv2.imshow("Original Image", image)
        cv2.imshow("Threshold Image", threshold)
        cv2.imshow("Lined Image", black_img)
        # cv2.imshow("Line Black Image", line_black)
        # cv2.imshow("Region Image", region_image)
        cv2.imshow("Final Image", final_image)

        k = cv2.waitKey(10) & 0xFF
        if k == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
