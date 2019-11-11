#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cal_coordinate import circle_coordinate

def get_circular_coordinate(circular_type, circular_list):

    """
    get circular x_coordinate, y_coordinate
    """

    x_coordinate = []
    y_coordinate = []

    # insert 50 points to simulate circular
    point_num = 50
    circular_type_list = [circular_list[i][0] for i in range(len(circular_list))]
    circular_type_index = circular_type_list.index(circular_type)
    center_x = circular_list[circular_type_index][1][0]
    center_y = circular_list[circular_type_index][1][1]
    radius = circular_list[circular_type_index][1][2]
    if radius <= 0:
        return [center_x], [center_y]

    if circular_type == "top_left_circular":
        start_angle = 180
        stop_angle = 90
    elif circular_type == "top_right_circular":
        start_angle = 90
        stop_angle = 0
    elif circular_type == "bottom_left_circular":
        start_angle = -90
        stop_angle = -180
    elif circular_type == "bottom_right_circular":
        start_angle = 0
        stop_angle = -90
    else:
        print("unsupport parameter")
        return x_coordinate, y_coordinate

    # format: center_x, center_y, radius, start_angle, stop_angle, point_num
    circular_para_list = [center_x, center_y, radius, start_angle, stop_angle, point_num]
    x_coordinate, y_coordinate = circle_coordinate(circular_para_list).get_point(0)

    return x_coordinate, y_coordinate

def get_rect_coordinate(rect_list):

    """
    get top center rectangle coordinate
    """

    x_coordinate = []
    y_coordinate = []

    point_num = 50
    # left rect circular
    center_x = rect_list[0][1][0]
    center_y = rect_list[0][1][1]
    radius = rect_list[0][1][2]
    start_angle = -180
    stop_angle = -90
    # format: center_x, center_y, radius, start_angle, stop_angle, point_num
    circular_para_list = [center_x, center_y, radius, start_angle, stop_angle, point_num]
    x_coordinate_tmp, y_coordinate_tmp = circle_coordinate(circular_para_list).get_point(0)
    x_coordinate += x_coordinate_tmp
    y_coordinate += y_coordinate_tmp
    # right rect circular
    center_x = rect_list[1][1][0]
    center_y = rect_list[1][1][1]
    radius = rect_list[1][1][2]
    start_angle = -90
    stop_angle = 0
    circular_para_list = [center_x, center_y, radius, start_angle, stop_angle, point_num]
    x_coordinate_tmp, y_coordinate_tmp = circle_coordinate(circular_para_list).get_point(0)
    x_coordinate += x_coordinate_tmp
    y_coordinate += y_coordinate_tmp
    return x_coordinate, y_coordinate

def get_boundary_xy_coordinate(circular_list, rect_list):

    """
    This is the main entry for the program
    """

    draw_boundary_order = ["top_left_circular", "top_center_rectangle", "top_right_circular", "bottom_right_circular", "bottom_left_circular"]
    x_coordinate = []
    y_coordinate = []

    for circular_type in draw_boundary_order:
        if circular_type == "top_center_rectangle":
            x_coordinate_tmp, y_coordinate_tmp = get_rect_coordinate(rect_list)
        else:
            x_coordinate_tmp, y_coordinate_tmp = get_circular_coordinate(circular_type, circular_list)
        x_coordinate += x_coordinate_tmp
        y_coordinate += y_coordinate_tmp

    # at last point, add 1 point to return to beginning position
    x_coordinate.append(x_coordinate[0])
    y_coordinate.append(y_coordinate[0])

    return x_coordinate, y_coordinate
