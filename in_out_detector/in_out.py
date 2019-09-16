#!/bin/env python3

# Native and web-based libraries
import cv2
import sys;

sys.path.append("")  # To be able to import from previous directory
import numpy as np
# My own python files.
from Configuration import JSONCourtConfig
from in_out_detector.helper import FieldParts
from in_out_detector.helper import Visualize
from in_out_detector.helper.TrackBar import TrackBar
from in_out_detector.helper import Utils

conf = "configuration/config.json"


def main():
    # This is the sample image
    IMAGE = "tenniscourt/orangecourt.jpg"

    # Get configuration data for tennis court initial configuration
    court = JSONCourtConfig(conf, "orange-court-1")

    lower_hsv = court["lower-hsv"]
    upper_hsv = court["upper-hsv"]
    line_conf = court["line-conf"]
    ANGLE_TOLERANCE = court["angle-tolerance"]
    region_split_x = court["region-split-x"]
    region_split_y = court["region-split-y"]

    # Enter the configurations into the TrackBar
    tb = TrackBar(lower_hsv, upper_hsv, line_conf,
                  ANGLE_TOLERANCE, region_split_x, region_split_y)
    tb.set_track_bar()  # set TrackBar

    # Read Image
    image = cv2.imread(IMAGE)
    # Create black image with shape equal to the read image
    black = np.zeros(image.shape, dtype=np.uint8)
    # Retain original image by copying
    image1 = image.copy()

    while True:
        # Convert the RGB image into HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # Read and Get the data from the Track Bar configuration
        lower, higher, line_settings, angle_tolerance, split_x, split_y = tb.get_track_bar()
        angle_tolerance /= 10.0

        threshold = cv2.inRange(hsv, lower, higher)

        black_img, lines = Utils.get_boundaries(threshold, line_settings)
        line90, line0 = Utils.get_perpendicular_lines(lines, tolerance=angle_tolerance)
        points = Utils.get_intersection(line90, line0)
        points_x, points_y = Utils.get_corner_points(black_img, points, split_x, split_y)
        # x_points, y_points = Utils.get_regions(image, split_x, split_y)

        boundary_doubles = FieldParts.get_boundary_doubles(points_x, points_y)
        boundary_singles = FieldParts.get_boundary_singles(points_x, points_y)
        boundary_doubles_left = FieldParts.get_boundary_doubles_left(points_x, points_y)
        boundary_doubles_right = FieldParts.get_boundary_doubles_right(points_x, points_y)
        boundary_singles_left = FieldParts.get_boundary_singles_left(points_x, points_y)
        boundary_singles_right = FieldParts.get_boundary_singles_right(points_x, points_y)

        # line_black = Visualize.draw_lines(black_img, line90, line0)
        # region_image = Visualize.draw_regions(image, x_points, y_points)

        # Visualize the Boundaries:
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
        # # cv2.imshow("Region Image", region_image)
        cv2.imshow("Final Image", final_image)

        k = cv2.waitKey(10) & 0xFF
        if k == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
