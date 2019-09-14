import cv2
import numpy as np
from shapely.geometry import LineString


def get_boundaries(img, settings):
    black = np.zeros(img.shape, dtype=np.uint8)
    lines = cv2.HoughLinesP(img, 1, np.pi / 180, settings[0],
                            minLineLength=settings[1],
                            maxLineGap=settings[2])
    # print(lines)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(black, (x1, y1), (x2, y2), 255, 1)

    return black, lines


def get_angle(line):
    x1, y1, x2, y2 = line
    if x2 - x1 == 0:
        return np.pi / 2
    slope = np.abs((y2 - y1) / (x2 - x1))
    return np.arctan(slope)


def get_perpendicular_lines(lines, tolerance, add_pad=5):
    def add_padding(line, added, mode=True):
        if not mode:
            return line[0] - added, line[1], line[2] + added, line[3]
        else:
            return line[0], line[1] + added, line[2], line[3] - added

    angle0 = 0
    angle90 = np.pi / 2
    np_lines = np.array([line[0] for line in lines])
    angles = np.array([get_angle(line[0]) for line in lines])
    angles_90 = np.where((angles <= angle90 + angle90 * tolerance) & (angles >= angle90 - angle90 * tolerance))[0]
    angles_0 = np.where((angles <= angle0 + angle0 * tolerance) & (angles >= angle0 - angle0 * tolerance))[0]
    lines_90 = np_lines[angles_90]
    lines_0 = np_lines[angles_0]

    lines_90 = [add_padding(line, add_pad, mode=True) for line in lines_90]
    lines_0 = [add_padding(line, add_pad, mode=False) for line in lines_0]

    return lines_90, lines_0


def get_intersection(lines1, lines2):
    points = []
    for line1 in lines1:
        line1 = LineString([(line1[0], line1[1]),
                            (line1[2], line1[3])])
        for line2 in lines2:

            line2 = LineString([(line2[0], line2[1]),
                                (line2[2], line2[3])])

            point = line1.intersection(line2)
            point = np.asarray(point)
            if len(point) == 0:
                continue

            points.append((int(point[0]), int(point[1])))

    return points


def get_regions(img, x_split, y_split):
    height, width, _ = img.shape
    x_points = [[(int(x * width / 100), 0), (int(x * width / 100), height)] for x in x_split]
    y_points = [[(0, int(y * height / 100)), (width, int(y * height / 100))] for y in y_split]
    return x_points, y_points


def get_numbers_between(num_list, start, end):
    bet = np.where((num_list > start) & (num_list < end))[0]
    return num_list[bet]


def get_mean_of_points(*num_list):
    return [np.mean(i, axis=0, dtype=np.int) for i in num_list]


def get_corner_points(img, points, x_split, y_split):
    height, width = img.shape
    x = np.array([p[0] for p in points])
    y = np.array([p[1] for p in points])

    x_point1 = x_point4 = x_point12 = x_point17 = get_numbers_between(x, 0, x_split[0]*width/100)
    x_point5 = x_point9 = x_point13 = get_numbers_between(x, x_split[0]*width/100, x_split[1]*width/100)
    x_point2 = x_point6 = x_point10 = x_point14 = x_point18 = get_numbers_between(x, x_split[1]*width/100,
                                                                                  x_split[2]*width/100)
    x_point7 = x_point11 = x_point15 = get_numbers_between(x, x_split[2]*width/100, x_split[3]*width/100)
    x_point3 = x_point8 = x_point16 = x_point19 = get_numbers_between(x, x_split[3]*width/100, width)

    y_point1 = y_point2 = y_point3 = get_numbers_between(y, 0, y_split[0]*height/100)
    y_point4 = y_point5 = y_point6 = y_point7 = y_point8 = get_numbers_between(y, y_split[0]*height/100,
                                                                               y_split[1]*height/100)
    y_point9 = y_point10 = y_point11 = get_numbers_between(y, y_split[1]*height/100, y_split[2]*height/100)
    y_point12 = y_point13 = y_point14 = y_point15 = y_point16 = get_numbers_between(y, y_split[2]*height/100,
                                                                                    y_split[3]*height/100)
    y_point17 = y_point18 = y_point19 = get_numbers_between(y, y_split[3]*height/100, height)

    x_points = get_mean_of_points(x_point1,  x_point2, x_point3, x_point4, x_point5, x_point6, x_point7,
                                  x_point8, x_point9, x_point10, x_point11, x_point12, x_point13, x_point14,
                                  x_point15, x_point16, x_point17, x_point18, x_point19)
    y_points = get_mean_of_points(y_point1, y_point2, y_point3, y_point4, y_point5, y_point6, y_point7,
                                  y_point8, y_point9, y_point10, y_point11, y_point12, y_point13, y_point14,
                                  y_point15, y_point16, y_point17, y_point18, y_point19)
    return x_points, y_points