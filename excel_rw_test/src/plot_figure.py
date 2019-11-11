#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from draw_boundary import get_boundary_xy_coordinate
import matplotlib.pyplot as plt
# from random import randint
from math import sqrt

def plot_target_measure(config_list, target_list, measure_list_mm, ax):

    """
    plot target and measure
    """

    test_type = config_list[0]
    boundary_error_threshold = config_list[4]
    center_error_threshold = config_list[5]

    for i in range(len(target_list)):
        if test_type == "line test":
            start_x = target_list[i][0]
            start_y = target_list[i][1]
            end_x = target_list[i][2]
            end_y = target_list[i][3]
            # insert_point = 200
            # step_x = (end_x - start_x) / insert_point
            # step_y = (end_y - start_y) / insert_point
            # target_x = []
            # target_y = []
            # for j in range(insert_point):
            #     target_x.append(start_x + step_x * j)
            #     target_y.append(start_y + step_y * j)
            # target_x.append(end_x)
            # target_y.append(end_y)
            target_x = [start_x, end_x]
            target_y = [start_y, end_y]
            measure_x = [measure_list_mm[i][j][0] for j in range(len(measure_list_mm[i]))]
            measure_y = [measure_list_mm[i][j][1] for j in range(len(measure_list_mm[i]))]
            for j in range(len(measure_y)):
                if measure_y[j] > 150:
                    print(i, j, measure_x[j], measure_y[j])
            target_line, = ax.plot(target_x, target_y, 'g-', linewidth=0.8)
            # measure_line, = ax.plot(measure_x, measure_y, 'b.', linewidth=1.5)
            measure_line, = ax.plot(measure_x, measure_y, 'b.', linewidth=0.5)
        elif test_type == "point test":
            # target_point, = ax.plot(target_list[i][0], target_list[i][1], 'go')
            target_point = plt.Circle((target_list[i][0], target_list[i][1]), 0.35, color='green', fill=False)
            ax.add_artist(target_point)
            for repeat in measure_list_mm[i]:
                measure_x = [repeat[j][0] for j in range(len(repeat))]
                measure_y = [repeat[j][1] for j in range(len(repeat))]
                measure_point, = ax.plot(measure_x, measure_y, 'b.')

def plot_figure(config_list, target_list, measure_list_mm, fig_filename):

    """
    plot figure for target and measure
    """

    test_type = config_list[0]
    max_x = config_list[1]
    max_y = config_list[2]
    boundary_range = config_list[3]

    fig, ax = plt.subplots()
    x_size = 10.
    y_size = x_size * max_y / max_x
    fig.set_size_inches((x_size, y_size))
    # fig.set_dpi(1080.)
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    #plot target and measure
    plot_target_measure(config_list, target_list, measure_list_mm, ax)
    # plot boundary
    ax.vlines(x=0, ymin=0, ymax=max_y, color='grey')
    ax.vlines(x=max_x, ymin=0, ymax=max_y, color='grey')
    ax.hlines(y=0, xmin=0, xmax=max_x, color='grey')
    ax.hlines(y=max_y, xmin=0, xmax=max_x, color='grey')
    # plot boundary_range
    ax.vlines(x=boundary_range, ymin=boundary_range, ymax=max_y - boundary_range, color='black')
    ax.vlines(x=max_x - boundary_range, ymin=boundary_range, ymax=max_y - boundary_range, color='black')
    ax.hlines(y=boundary_range, xmin=boundary_range, xmax=max_x - boundary_range, color='black')
    ax.hlines(y=max_y - boundary_range, xmin=boundary_range, xmax=max_x - boundary_range, color='black')

    plt.savefig(fig_filename)
    # plt.show()

def plot_figure_notch(circular_list, rect_list, config_list, target_list, measure_list_mm, fig_filename):

    """
    plot notch tp
    """

    test_type = config_list[0]
    max_x = config_list[1]
    max_y = config_list[2]
    boundary_range = config_list[3]

    fig, ax = plt.subplots()
    x_size = 10.
    y_size = x_size * max_y / max_x
    fig.set_size_inches((x_size, y_size))
    fig.set_dpi(320.)
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    #plot target and measure
    plot_target_measure(config_list, target_list, measure_list_mm, ax)
    # plot boundary
    circular_para_list = [ \
            ["top_left_circular", [circular_list[0], circular_list[0], circular_list[0]]], \
            ["top_right_circular", [max_x - circular_list[1], circular_list[1], circular_list[1]]], \
            ["bottom_left_circular", [circular_list[2], max_y - circular_list[2], circular_list[2]]], \
            ["bottom_right_circular", [max_x - circular_list[3], max_y - circular_list[3], circular_list[3]]] \
            ]
    left_radius = max(abs(rect_list[5] - rect_list[4]), abs(rect_list[1] - rect_list[0]))
    right_radius = max(abs(rect_list[5] - rect_list[4]), abs(rect_list[3] - rect_list[2]))
    rect_para_list = [ \
            ["rect_left_circular", [rect_list[0] + left_radius, rect_list[4], left_radius]], \
            ["rect_right_circular", [rect_list[3] - right_radius, rect_list[4], right_radius]] \
            ]
    boundary_x, boundary_y = get_boundary_xy_coordinate(circular_para_list, rect_para_list)
    boundary_line, = ax.plot(boundary_x, boundary_y, '-', linewidth=1, color='grey')
    # plot boundary_range
    center_move = boundary_range / sqrt(2.)
    circular_para_list = [ \
            ["top_left_circular", [circular_list[0] + center_move, circular_list[0] + center_move, circular_list[0]]], \
            ["top_right_circular", [max_x - circular_list[1] - center_move, circular_list[1] + center_move, circular_list[1]]], \
            ["bottom_left_circular", [circular_list[2] + center_move, max_y - circular_list[2] - center_move, circular_list[2]]], \
            ["bottom_right_circular", [max_x - circular_list[3] - center_move, max_y - circular_list[3] - center_move, circular_list[3]]] \
            ]
    rect_para_list = [ \
            ["rect_left_circular", [rect_list[0] + left_radius - center_move, rect_list[4] + center_move, left_radius]], \
            ["rect_right_circular", [rect_list[3] - right_radius + center_move, rect_list[4] + center_move, right_radius]] \
            ]
    boundary_range_x, boundary_range_y = get_boundary_xy_coordinate(circular_para_list, rect_para_list)
    boundary_line, = ax.plot(boundary_range_x, boundary_range_y, 'k-', linewidth=0.5)

    # fig_filename = "./output" + str(randint(1000000, 9999999)) + ".png"
    plt.savefig(fig_filename)
    print("figure has been save to '%s'" % ( fig_filename ))
    # plt.show()

if __name__ == "__main__":

    """
    this is for test purpose
    """

    # test_type, max_x, max_y, boundary_range
    config_list = ["line test", 200, 200, 50]
    target_list = [[1, 1, 100, 100], [100, 1, 1, 100], [1,1,1,100]]
    measure_list_mm = [[[1,1], [2,3], [4, 5]], [[100,1],[99, 2],[50,50]], [[1,1],[1,2]]]
    plot_figure(config_list, target_list, measure_list_mm)
