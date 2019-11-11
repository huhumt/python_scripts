#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def concatenate_left_right_test(config_left, target_left, measure_left_mm, measure_left_pixel, config_right, target_right, measure_right_mm, measure_right_pixel):

    """
    for some limitation, MIK need to test left half and right half, here to concatenate right data to left
    """

    left_test_type = config_left[0]
    left_max_x = config_left[1]
    left_max_y = config_left[2]
    left_boundary_range = config_left[3]

    right_test_type = config_right[0]
    right_max_x = config_right[1]
    right_max_y = config_right[2]
    right_boundary_range = config_right[3]

    if left_test_type != right_test_type or left_boundary_range != right_boundary_range:
        print("Can not concatenate different type of data")
        exit(0)

    config_list = config_left
    config_list[1] += config_right[1]
    config_list[4] = min(config_list[4], config_right[4])
    config_list[5] = min(config_list[5], config_right[5])

    if left_test_type == "line test":
        left_measure_first_x = measure_left_pixel[0][0][0]
        right_measure_first_x = measure_right_pixel[0][0][0]
        if right_measure_first_x > left_measure_first_x:
            real_target_left = target_left
            real_target_right = target_right
            measure_list_mm = measure_left_mm + measure_right_mm
            measure_list_pixel = measure_left_pixel + measure_right_pixel
        else:
            real_target_left = target_right
            real_target_right = target_left
            measure_list_mm = measure_right_mm + measure_left_mm
            measure_list_pixel = measure_right_pixel + measure_left_pixel

        target_list = real_target_left
        for (start_x, start_y, end_x, end_y) in real_target_right:
            target_list.append([start_x + left_max_x, start_y, end_x + left_max_x, end_y])

    elif left_test_type == "point test":
        left_measure_first_x = measure_left_pixel[0][0][0][0]
        right_measure_first_x = measure_right_pixel[0][0][0][0]
        if right_measure_first_x > left_measure_first_x:
            real_target_left = target_left
            real_target_right = target_right
            measure_list_mm = measure_left_mm + measure_right_mm
            measure_list_pixel = measure_left_pixel + measure_right_pixel
        else:
            real_target_left = target_right
            real_target_right = target_left
            measure_list_mm = measure_right_mm + measure_left_mm
            measure_list_pixel = measure_right_pixel + measure_left_pixel

        target_list = real_target_left
        for (target_x, target_y) in real_target_right:
            target_list.append([target_x + left_max_x, target_y])

    return config_list, target_list, measure_list_mm, measure_list_pixel
