#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import sqrt

def generate_base_map(read_data_list):

    """
    generate data base map
    """

    tx_len = len(read_data_list[0])
    rx_len = len(read_data_list[0][0])
    sum_list = [([0.0] * rx_len) for i in range(tx_len)]
    for i in range(len(read_data_list)):
        for j in range(len(read_data_list[i])):
            for k in range(len(read_data_list[i][j])):
                sum_list[j][k] += (float(read_data_list[i][j][k]))
    for i in range(len(sum_list)):
        for j in range(len(sum_list[i])):
            sum_list[i][j] /= len(read_data_list)

    return sum_list

def generate_max_delta_map(read_data_list, base_map):

    """
    generate max delta map: delta = data - base
    """

    tx_len = len(read_data_list[0])
    rx_len = len(read_data_list[0][0])
    max_list = [([0.0] * rx_len) for i in range(tx_len)]
    for i in range(len(read_data_list)):
        for j in range(len(read_data_list[i])):
            for k in range(len(read_data_list[i][j])):
                delta = abs(float(read_data_list[i][j][k]) - base_map[j][k])
                if delta > max_list[j][k]:
                    max_list[j][k] = delta

    return max_list

def find_max_value(max_list, exclude_tx_list = [], exclude_rx_list = []):

    """
    find max val
    """

    max_val = -10000
    tx_index = 0
    rx_index = 0
    for i in range(len(max_list)):
        if i not in exclude_tx_list:
            for j in range(len(max_list[i])):
                if j not in exclude_rx_list:
                    if max_list[i][j] > max_val:
                        max_val = max_list[i][j]
                        tx_index = i
                        rx_index = j
    return max_val, tx_index, rx_index

def get_sqrt_square_average(read_data_list):
    """
    sqrt(x1^2 + x2^2 + ... + xn^2)
    """
    tx_len = len(read_data_list[0])
    rx_len = len(read_data_list[0][0])
    sqrt_square_average = [([0.0] * rx_len) for i in range(tx_len)]
    for i in range(len(read_data_list)):
        for j in range(len(read_data_list[i])):
            for k in range(len(read_data_list[i][j])):
                sqrt_square_average[j][k] += ((float(read_data_list[i][j][k])) * read_data_list[i][j][k])
    for i in range(len(sqrt_square_average)):
        for j in range(len(sqrt_square_average[i])):
            sqrt_square_average[i][j] = sqrt(sqrt_square_average[i][j] / len(read_data_list))

    return sqrt_square_average

if __name__ == "__main__":

    """
    this is for test purpose
    """

    read_data_list = [ \
            [[1, 2, 3], [4, 5, 6]], \
            [[1, 2, 3], [4, 5, 6]], \
            [[1, 2, 3], [4, 5, 6]]
            ]
    max_val, base_map, delta_max_map = analysis_data(read_data_list)
    print(max_val)
    print(base_map)
    print(delta_max_map)
