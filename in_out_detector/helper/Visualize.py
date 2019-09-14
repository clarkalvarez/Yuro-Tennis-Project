import cv2
import numpy as np


OUTER_BOUNDARY_THICKNESS = 2
SECOND_OUTER_BOUNDARY_THICKNESS = 2


def draw_lines(img, line1, line2):
    black = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    for line in line1:
        cv2.line(black, (line[0], line[1]), (line[2], line[3]),
                 (0, 255, 0), 2)
    for line in line2:
        cv2.line(black, (line[0], line[1]), (line[2], line[3]),
                 (0, 0, 255), 2)
    return black


def draw_points(img, points):
    img1 = img.copy()
    for point in points:
        cv2.circle(img1, (int(point[0]), int(point[1])), 5, (255, 0, 0), -1)
    return img1


def draw_regions(img, x_points, y_points):
    img_ = img.copy()
    for x in x_points:
        cv2.line(img_, (x[0][0], x[0][1]), (x[1][0], x[1][1]), (0, 255, 255), 2)

    for y in y_points:
        cv2.line(img_, (y[0][0], y[0][1]), (y[1][0], y[1][1]), (255, 255, 0), 2)

    return img_


def draw_boundary(img, black, points, color, thickness, fade=0.3, boundary=False, area=False):
    points.append(points[0])
    if boundary:
        for i in range(1, len(points)):
            cv2.line(img, points[i-1], points[i], color, thickness)
    if area:
        p = np.array([[[x[0], x[1]] for x in points]])
        cv2.fillPoly(black, p, color)
        img = cv2.addWeighted(img, 1, black, fade, 0)
    return img
