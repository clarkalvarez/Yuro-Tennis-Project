#!/bin/env python3

import json


class JSONCourtConfig:
    """
    Reads Court Configuration JSON file

    class parameters: json file, court

    Court Configurations:
        orange-court-1:
            __getitem__:
                lower-hsv, upper-hsv, line-conf, angle-tolerance,
                region-split-x, region-split-y
    """

    def __init__(self, json_file, court):
        super(JSONCourtConfig, self).__init__()

        with open(json_file, "r") as file:
            conf_data = json.load(file)

        self.court_conf = conf_data["in-out-configuration"]["tennis-courts"][court]

    def __getitem__(self, item):
        data = self.court_conf[item]
        if isinstance(data, list):
            return tuple(data)
        return data
