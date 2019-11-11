#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from analysis_data import generate_base_map, generate_max_delta_map, find_max_value, get_sqrt_square_average
from find_pattern import find_pattern
from plot_figure import plot_figure
from read_txt import read_txt
import numpy as np
import math
import sys

def get_max_noise_diff(noise_list, diff_list):

    """
    get max diff and noise
    """

    base_map = generate_base_map(noise_list)
    noise_list_tmp = noise_list
    for i in range(len(noise_list_tmp)):
        for j in range(len(noise_list_tmp[i])):
            for k in range(len(noise_list_tmp[i][j])):
                noise_list_tmp[i][j][k] = noise_list_tmp[i][j][k] - base_map[j][k]
    noise_output_list = get_sqrt_square_average(noise_list_tmp)
    max_noise, tx, rx = find_max_value(noise_output_list)

    sum_of_noise = 0.0
    for tx_data in noise_output_list:
        for rx_data in tx_data:
            sum_of_noise += rx_data
    sum_of_noise /= 36

    touch_base_map = generate_base_map(diff_list)
    touch_list_tmp = touch_base_map
    for i in range(len(base_map)):
        for j in range(len(base_map[i])):
            touch_list_tmp[i][j] = base_map[i][j] - touch_base_map[i][j]
    avg_diff, tx, rx = find_max_value(touch_list_tmp)
    cur_noise = noise_output_list[tx][rx]

    max_diff = -10000
    for i in range(len(diff_list)):
        for j in range(len(diff_list[i])):
            for k in range(len(diff_list[i][j])):
                cur_diff = base_map[j][k] - diff_list[i][j][k]
                if cur_diff > max_diff:
                    max_diff = cur_diff

    print("IDC tool: max diff=%.3f, avg_noise=%.3f, snr=%.3f" % ( max_diff, sum_of_noise, 20 * math.log(max_diff/sum_of_noise, 10)))

    return max_noise, max_diff, cur_noise, avg_diff

def main():

    """
    This is main function for the project
    """

    filename_list = find_pattern("rawdata_K1_K2_20191031*.txt", "./data/")
    for filename in filename_list:
        f_noise_list, f_diff_list, noise_list, diff_list, K1_list, K2_list = read_txt(filename).read()
        for i in range(len(f_noise_list)):
            f_max_noise, f_max_diff, f_ch_noise, f_avg_diff = get_max_noise_diff(f_noise_list[i], f_diff_list[i])
            f_max_diff_to_ch_noise_snr  = math.log(f_max_diff/f_ch_noise, 10) * 20
            f_max_diff_to_max_noise_snr = math.log(f_max_diff/f_max_noise, 10) * 20
            f_avg_diff_to_ch_noise_snr  = math.log(f_avg_diff/f_ch_noise, 10) * 20
            f_avg_diff_to_max_noise_snr = math.log(f_avg_diff/f_max_noise, 10) * 20
            print("filtered---(K1=%3d,K2=%3d): max_noise=%.3f, max_diff=%.3f, ch_noise=%.3f, avg_diff=%.3f, snr=%.3f-%.3f-%.3f-%.3f"
                    % ( K1_list[i], K2_list[i], f_max_noise, f_max_diff, f_ch_noise, f_avg_diff,
                        f_max_diff_to_ch_noise_snr, f_max_diff_to_max_noise_snr, f_avg_diff_to_ch_noise_snr, f_avg_diff_to_max_noise_snr ))
            # print("%d-%d %.3f %.3f %.3f %.3f" % ( K1_list[i], K2_list[i], f_max_diff, f_avg_diff, f_max_noise, f_avg_diff_to_max_noise_snr ))

            max_noise, max_diff, ch_noise, avg_diff = get_max_noise_diff(noise_list[i], diff_list[i])
            max_diff_to_ch_noise_snr = math.log(max_diff/ch_noise, 10) * 20
            max_diff_to_max_noise_snr = math.log(max_diff/max_noise, 10) * 20
            avg_diff_to_ch_noise_snr = math.log(avg_diff/ch_noise, 10) * 20
            avg_diff_to_max_noise_snr = math.log(avg_diff/max_noise, 10) * 20
            print("unfilter---(K1=%3d,K2=%3d): max_noise=%.3f, max_diff=%.3f, ch_noise=%.3f, avg_diff=%.3f, snr=%.3f-%.3f-%.3f-%.3f"
                    % ( K1_list[i], K2_list[i], max_noise, max_diff, ch_noise, avg_diff,
                        max_diff_to_ch_noise_snr, max_diff_to_max_noise_snr, avg_diff_to_ch_noise_snr, avg_diff_to_max_noise_snr ))
            print("\n")
            # print("%d-%d %.3f %.3f %.3f %.3f" % ( K1_list[i], K2_list[i], max_diff, avg_diff, max_noise, avg_diff_to_max_noise_snr ))

        print("\n\n")

    return 0

if __name__ == "__main__":

    '''
    System main entry
    '''

    main()
