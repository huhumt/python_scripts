#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from point_analysis import point_analysis
from line_analysis import line_analysis

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
    boundary_range = 3.5

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

def print_point_accuracy_info(accuracy_x_list, accuracy_y_list, boundary_index_list):

    """
    print accuracy info
    """

    max_edge_x = 0.0
    max_edge_y = 0.0
    max_center_x = 0.0
    max_center_y = 0.0

    for i in range(len(accuracy_x_list)):
        if i in boundary_index_list:
            if accuracy_x_list[i] > max_edge_x:
                max_edge_x = accuracy_x_list[i]
            if accuracy_y_list[i] > max_edge_y:
                max_edge_y = accuracy_y_list[i]
        else:
            if accuracy_x_list[i] > max_center_x:
                max_center_x = accuracy_x_list[i]
            if accuracy_y_list[i] > max_center_y:
                max_center_y = accuracy_y_list[i]
    # print("\tEdge max accuracy error   (%f, %f), point index (%d, %d)"
    #         % (max_edge_x, max_edge_y,
    #             accuracy_x_list.index(max_edge_x), accuracy_y_list.index(max_edge_y)))
    # print("\tCenter max accuracy error (%f, %f), point index (%d, %d)"
    #         % (max_center_x, max_center_y,
    #             accuracy_x_list.index(max_center_x), accuracy_y_list.index(max_center_y)))
    print("Accuracy: Center X: %.3fmm, Center Y: %.3fmm" % (max_center_x, max_center_y))
    print("          Edge   X: %.3fmm, Edge   Y: %.3fmm\n" % (max_edge_x, max_edge_y))

    if max_edge_x < 1.5 and max_edge_y < 1.5 and max_center_x < 1.0 and max_center_y < 1.0:
        return 1
    else:
        return 0

def print_point_jitter_info(jitter_x_list, jitter_y_list, boundary_index_list):

    """
    print jitter info
    """

    max_edge_x = 0.0
    max_edge_y = 0.0
    max_center_x = 0.0
    max_center_y = 0.0

    for i in range(len(jitter_x_list)):
        if i in boundary_index_list:
            if jitter_x_list[i] > max_edge_x:
                max_edge_x = jitter_x_list[i]
            if jitter_y_list[i] > max_edge_y:
                max_edge_y = jitter_y_list[i]
        else:
            if jitter_x_list[i] > max_center_x:
                max_center_x = jitter_x_list[i]
            if jitter_y_list[i] > max_center_y:
                max_center_y = jitter_y_list[i]
    # print("\tEdge max jitter error   (%f, %f), point index (%d, %d)"
    #         % (max_edge_x, max_edge_y,
    #             jitter_x_list.index(max_edge_x), jitter_y_list.index(max_edge_y)))
    # print("\tCenter max jitter error (%f, %f), point index (%d, %d)"
    #         % (max_center_x, max_center_y,
    #             jitter_x_list.index(max_center_x), jitter_y_list.index(max_center_y)))
    print("Jitter: Center X: %.3fmm, Center Y: %.3fmm" % (max_center_x, max_center_y))
    print("        Edge   X: %.3fmm, Edge   Y: %.3fmm\n" % (max_edge_x, max_edge_y))

    if max_edge_x < 0.3 and max_edge_y < 0.3 and max_center_x < 0.3 and max_center_y < 0.3:
        return 1
    else:
        return 0

def print_line_linearity_info(target_list, measure_list_mm, boundary_index_list, linearity_list):

    """
    analysis line boundary/center linearity
    """

    slash_k_b_list = line_analysis(target_list, measure_list_mm).get_target_line_formula()
    boundary_max_x = [0, [0, 0]]
    boundary_max_y = [0, [0, 0]]
    center_max_x = [0, [0, 0]]
    center_max_y = [0, [0, 0]]

    if linearity_list:
        rate_x_list = [0, 1, 0, 1, 0.707106781, 0.707106781, 1, 0]
        rate_y_list = [1, 0, 1, 0, 0.707106781, 0.707106781, 0, 1]

        boundary_error_x = []
        boundary_error_y = []

        center_error_x = []
        center_error_y = []

        for i in range(8):
            boundary_error_x.append(linearity_list[0][i] * rate_x_list[i])
            boundary_error_y.append(linearity_list[0][i] * rate_y_list[i])
            center_error_x.append(linearity_list[1][i] * rate_x_list[i])
            center_error_y.append(linearity_list[1][i] * rate_y_list[i])

        boundary_max_x[0] = max(boundary_error_x)
        boundary_max_y[0] = max(boundary_error_y)

        center_max_x[0] = max(center_error_x)
        center_max_y[0] = max(center_error_y)
    else:
        linearity_list = line_analysis(target_list, measure_list_mm).cal_linearity()
        for i in range(len(linearity_list)):
            for j in range(len(linearity_list[i])):
                measure_x = measure_list_mm[i][j][0]
                measure_y = measure_list_mm[i][j][1]
                x, y = get_shadow_point(slash_k_b_list[i], measure_x, measure_y, target_list[i][0])

                delta_x = abs(x - measure_x) - 1e-4
                delta_y = abs(y - measure_y) - 1e-4

                if j in boundary_index_list[i]:
                    if delta_x > boundary_max_x[0]:
                        boundary_max_x[0] = delta_x
                        boundary_max_x[1] = [i, j]
                    if delta_y > boundary_max_y[0]:
                        boundary_max_y[0] = delta_y
                        boundary_max_y[1] = [i, j]
                else:
                    if delta_x > center_max_x[0]:
                        center_max_x[0] = delta_x
                        center_max_x[1] = [i, j]
                    if delta_y > center_max_y[0]:
                        center_max_y[0] = delta_y
                        center_max_y[1] = [i, j]
    print("\tEdge max linearity error   (%f, %f), debug info: X:%d-%d, (%f, %f)---Y:%d-%d, (%f, %f)"
            % (boundary_max_x[0], boundary_max_y[0], boundary_max_x[1][0], boundary_max_x[1][1],
                measure_list_mm[boundary_max_x[1][0]][boundary_max_x[1][1]][0],
                measure_list_mm[boundary_max_x[1][0]][boundary_max_x[1][1]][1],
                boundary_max_y[1][0], boundary_max_y[1][1],
                measure_list_mm[boundary_max_y[1][0]][boundary_max_y[1][1]][0],
                measure_list_mm[boundary_max_y[1][0]][boundary_max_y[1][1]][1]))
    print("\tCenter max linearity error (%f, %f), debug info: X:%d-%d, (%f, %f)---Y:%d-%d, (%f, %f)"
            % (center_max_x[0], center_max_y[0], center_max_x[1][0], center_max_x[1][1],
                measure_list_mm[center_max_x[1][0]][center_max_x[1][1]][0],
                measure_list_mm[center_max_x[1][0]][center_max_x[1][1]][1],
                center_max_y[1][0], center_max_y[1][1],
                measure_list_mm[center_max_y[1][0]][center_max_y[1][1]][0],
                measure_list_mm[center_max_y[1][0]][center_max_y[1][1]][1]))
    print("Center X: %.3fmm, Center Y: %.3fmm" % (center_max_x[0], center_max_y[0]))
    print("Edge   X: %.3fmm, Edge   Y: %.3fmm" % (boundary_max_x[0], boundary_max_y[0]))

    if boundary_max_x[0] >= 1.5 or boundary_max_y[0] >= 1.5 or center_max_x[0] >= 1.0 or center_max_y[0] >= 1.0:
        print("\t\t----------------------------------LINE TEST FAIL")
    else:
        print("\t\t----------------------------------LINE TEST PASS")

def analysis_data(config_list, target_list, measure_list_mm, linearity_list):

    """
    analysis data based on data type, target and measure list
    """

    len1 = len(target_list)
    len2 = len(measure_list_mm)
    test_type = config_list[0]

    if len1 == 0 or len2 ==0 or len1 != len2:
        print("len of traget-measure: ", len1, len2)
        print("target_list[0]: ", target_list[0])
        print("target_list[-1]: ", target_list[-1])
        print("measure_list[0]: ", measure_list_mm[0])
        print("measure_list[-1]: ", measure_list_mm[-1])
        print("Error when loading target/mearsure data")
        return -2

    boundary_index_list = get_boundary_list(config_list, target_list, measure_list_mm)
    print("\nActive size: %.3fmm, %.3fmm" % (config_list[1], config_list[2]))

    if test_type == "point test":
        print("\nPoint test data analysis:")
        point_fd = point_analysis(target_list, measure_list_mm)
        accuracy_x_list, accuracy_y_list = point_fd.cal_accuracy()
        ret1 = print_point_accuracy_info(accuracy_x_list, accuracy_y_list, boundary_index_list)

        jitter_x_list, jitter_y_list = point_fd.cal_jitter()
        ret2 = print_point_jitter_info(jitter_x_list, jitter_y_list, boundary_index_list)

        if ret1 > 0 and ret2 > 0:
            print("\t\t----------------------------------POINT TEST PASS")
        else:
            print("\t\t----------------------------------POINT TEST FAIL")
        return 0
    elif test_type == "line test":
        print("\nLine test data analysis:")
        print_line_linearity_info(target_list, measure_list_mm, boundary_index_list, linearity_list)
        print("\n\n")
        return 0
    else:
        print("Unsupport excel data")
        return -1
