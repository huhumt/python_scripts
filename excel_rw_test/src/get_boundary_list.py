#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from line_analysis import line_analysis
from math import sqrt

def get_shadow_point(slash_k_b_list, measure_x, measure_y, target_x):

    """
    get shadow point on a line from given point
    """

    if slash_k_b_list:
        slash_k = slash_k_b_list[0]
        slash_b = slash_k_b_list[1]
        x = (slash_k * (measure_y - slash_b) + measure_x) / (slash_k * slash_k + 1)
        y = slash_k * x + slash_b
    else:
        x = target_x
        y = measure_y
    return x, y

def get_boundary_list(config_list, target_list, measure_list_mm):

    """
    get boundary index
    """

    test_type = config_list[0]
    max_x = config_list[1]
    max_y = config_list[2]
    boundary_range = config_list[3]

    left = boundary_range + 1e-4
    right = max_x - boundary_range - 1e-4
    up = boundary_range + 1e-4
    down = max_y - boundary_range - 1e-4
    boundary_index_list = []
    if test_type == "point test":
        for i in range(len(target_list)):
            x = target_list[i][0]
            y = target_list[i][1]
            if x < left or x > right or y < up or y > down:
                boundary_index_list.append(i)
    elif test_type == "line test":
        slash_k_b_list = line_analysis(target_list, measure_list_mm).get_target_line_formula()
        for i in range(len(measure_list_mm)):
            cur_line_boundary_list = []
            for j in range(len(measure_list_mm[i])):
                measure_x = measure_list_mm[i][j][0]
                measure_y = measure_list_mm[i][j][1]
                x, y = get_shadow_point(slash_k_b_list[i], measure_x, measure_y, target_list[i][0])
                if x < left or x > right or y < up or y > down:
                    cur_line_boundary_list.append(j)
            boundary_index_list.append(cur_line_boundary_list)
    return boundary_index_list

def is_point_in_corner_circular_boundary(distance, circular_radius, boundary_range):

    """
    judge whether a point is in boundary area for four corner circular
    """

    if circular_radius - distance > boundary_range:
        return True
    else:
        return False

def is_point_in_rect_circular_boundary(distance, circular_radius, boundary_range):

    """
    judge whether a point is in boundary area for top center rect
    """

    if distance < circular_radius + boundary_range:
        return True
    else:
        return False

def is_boundary(max_x, max_y, boundary_range, circular_list, rect_list, xy_coordinate):

    """
    check whether a point in notch boundary area
    """

    x = xy_coordinate[0]
    y = xy_coordinate[1]
    if x < circular_list[0] and y < circular_list[0]: # top left corner
        delta_x = x - circular_list[0]
        delta_y = y - circular_list[0]
        distance = sqrt(delta_x * delta_x + delta_y * delta_y)
        if is_point_in_corner_circular_boundary(distance, circular_list[0], boundary_range) is True:
            return True
    elif x > max_x - circular_list[1] and y < circular_list[1]: # top right corner
        delta_x = x - (max_x - circular_list[1])
        delta_y = y - circular_list[1]
        distance = sqrt(delta_x * delta_x + delta_y * delta_y)
        if is_point_in_corner_circular_boundary(distance, circular_list[1], boundary_range) is True:
            return True
    elif x < circular_list[2] and y > max_y - circular_list[2]: # bottom left corner
        delta_x = x - circular_list[2]
        delta_y = y - (max_y - circular_list[2])
        distance = sqrt(delta_x * delta_x + delta_y * delta_y)
        if is_point_in_corner_circular_boundary(distance, circular_list[2], boundary_range) is True:
            return True
    elif x > max_x - circular_list[3] and y > max_y - circular_list[3]: # bottom right corner
        delta_x = x - (max_x - circular_list[3])
        delta_y = y - (max_y - circular_list[3])
        distance = sqrt(delta_x * delta_x + delta_y * delta_y)
        if is_point_in_corner_circular_boundary(distance, circular_list[3], boundary_range) is True:
            return True
    elif x > rect_list[0] and x < rect_list[1] and y > rect_list[4] and y < rect_list[5] + boundary_range:
        radius = max(rect_list[4], rect_list[1] - rect_list[0])
        delta_x = x - (rect_list[0] + radius)
        delta_y = y - 0
        distance = sqrt(delta_x * delta_x + delta_y * delta_y)
        if is_point_in_rect_circular_boundary(distance, radius, boundary_range) is True:
            return True
    elif x > rect_list[2] and x < rect_list[3] and y > rect_list[4] and y < rect_list[5] + boundary_range:
        radius = max(rect_list[4], rect_list[3] - rect_list[2])
        delta_x = x - (rect_list[3] - radius)
        delta_y = y
        distance = sqrt(delta_x * delta_x + delta_y * delta_y)
        if is_point_in_rect_circular_boundary(distance, radius, boundary_range) is True:
            return True
    elif x > rect_list[1] and x < rect_list[2] and y > rect_list[4] and y < rect_list[5] + boundary_range:
        return True
    else:
        return False

def get_notch_boundary_list(config_list, circular_list, rect_list, target_list, measure_list_mm):

    """
    specify notch Tp boundary
    """

    test_type = config_list[0]
    max_x = config_list[1]
    max_y = config_list[2]
    boundary_range = config_list[3]

    boundary_index_list = get_boundary_list(config_list, target_list, measure_list_mm)
    if test_type == "point test":
        for i in range(len(target_list)):
            xy_coordinate = [target_list[i][0], target_list[i][1]]
            if is_boundary(max_x, max_y, boundary_range, circular_list, rect_list, xy_coordinate) is True:
                boundary_index_list.append(i)
    elif test_type == "line test":
        slash_k_b_list = line_analysis(target_list, measure_list_mm).get_target_line_formula()
        for i in range(len(measure_list_mm)):
            for j in range(len(measure_list_mm[i])):
                measure_x = measure_list_mm[i][j][0]
                measure_y = measure_list_mm[i][j][1]
                x, y = get_shadow_point(slash_k_b_list[i], measure_x, measure_y, target_list[i][0])
                xy_coordinate = [x, y]
                if is_boundary(max_x, max_y, boundary_range, circular_list, rect_list, xy_coordinate) is True:
                    boundary_index_list[i].append(j)
    return boundary_index_list
