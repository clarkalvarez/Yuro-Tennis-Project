#!/bin/env python3

import cv2


class TrackBar:

    def __init__(self, lower_hsv, upper_hsv, line_conf, angle_tolerance, region_split_x,
                 region_split_y):
        self.lower_hsv = lower_hsv
        self.upper_hsv = upper_hsv
        self.line_conf = line_conf
        self.angle_tolerance = angle_tolerance
        self.region_split_x = region_split_x
        self.region_split_y = region_split_y

    def set_track_bar(self):
        cv2.namedWindow("TrackBar")
        cv2.createTrackbar("LOWER H", "TrackBar", self.lower_hsv[0], 255, self.nothing)
        cv2.createTrackbar("LOWER S", "TrackBar", self.lower_hsv[1], 255, self.nothing)
        cv2.createTrackbar("LOWER V", "TrackBar", self.lower_hsv[2], 255, self.nothing)
        cv2.createTrackbar("UPPER H", "TrackBar", self.upper_hsv[0], 255, self.nothing)
        cv2.createTrackbar("UPPER S", "TrackBar", self.upper_hsv[1], 255, self.nothing)
        cv2.createTrackbar("UPPER V", "TrackBar", self.upper_hsv[2], 255, self.nothing)

        cv2.createTrackbar("Threshold", "TrackBar", self.line_conf[0], 500, self.nothing)
        cv2.createTrackbar("MinLineLength", "TrackBar", self.line_conf[1], 500, self.nothing)
        cv2.createTrackbar("MaxLineGap", "TrackBar", self.line_conf[2], 500, self.nothing)

        cv2.createTrackbar("Angle Tolerance", "TrackBar", self.angle_tolerance, 100, self.nothing)

        cv2.createTrackbar("x1", "TrackBar", self.region_split_x[0], 100, self.nothing)
        cv2.createTrackbar("x2", "TrackBar", self.region_split_x[1], 100, self.nothing)
        cv2.createTrackbar("x3", "TrackBar", self.region_split_x[2], 100, self.nothing)
        cv2.createTrackbar("x4", "TrackBar", self.region_split_x[3], 100, self.nothing)

        cv2.createTrackbar("y1", "TrackBar", self.region_split_y[0], 100, self.nothing)
        cv2.createTrackbar("y2", "TrackBar", self.region_split_y[1], 100, self.nothing)
        cv2.createTrackbar("y3", "TrackBar", self.region_split_y[2], 100, self.nothing)
        cv2.createTrackbar("y4", "TrackBar", self.region_split_y[3], 100, self.nothing)

    @staticmethod
    def nothing(x):
        pass

    def get_track_bar(self):
        l_h = cv2.getTrackbarPos('LOWER H', 'TrackBar')
        l_s = cv2.getTrackbarPos('LOWER S', 'TrackBar')
        l_v = cv2.getTrackbarPos('LOWER V', 'TrackBar')
        u_h = cv2.getTrackbarPos('UPPER H', 'TrackBar')
        u_s = cv2.getTrackbarPos('UPPER S', 'TrackBar')
        u_v = cv2.getTrackbarPos('UPPER V', 'TrackBar')

        thr = cv2.getTrackbarPos('Threshold', 'TrackBar')
        mll = cv2.getTrackbarPos('MinLineLength', 'TrackBar')
        mlg = cv2.getTrackbarPos('MaxLineGap', 'TrackBar')

        a_t = cv2.getTrackbarPos('Angle Tolerance', 'TrackBar')

        x1 = cv2.getTrackbarPos('x1', 'TrackBar')
        x2 = cv2.getTrackbarPos('x2', 'TrackBar')
        x3 = cv2.getTrackbarPos('x3', 'TrackBar')
        x4 = cv2.getTrackbarPos('x4', 'TrackBar')
        y1 = cv2.getTrackbarPos('y1', 'TrackBar')
        y2 = cv2.getTrackbarPos('y2', 'TrackBar')
        y3 = cv2.getTrackbarPos('y3', 'TrackBar')
        y4 = cv2.getTrackbarPos('y4', 'TrackBar')

        return (l_h, l_s, l_v), (u_h, u_s, u_v), (thr, mll, mlg), a_t, (x1, x2, x3, x4), (y1, y2, y3, y4)