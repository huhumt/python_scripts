#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from re import findall

class read_txt:
    '''
    This class is used to read a txt file
    '''
    def __init__(self, name):
        self.name = name

    def read(self):

        fd = open(self.name, 'r')
        try:
            is_frame_begin_flag = 0
            is_data_begin_flag = 0
            is_valid_data_flag = 0

            tx_counter = 0
            frame_counter = 0
            frame_total = 0

            tx_num = 4
            rx_num = 5

            filtered_noise_list = []
            filtered_diff_list = []
            filtered_cur_frame_list = []

            unfiltered_noise_list = []
            unfiltered_diff_list = []
            unfiltered_cur_frame_list = []

            tmp_filtered_data = []
            tmp_unfiltered_data = []

            K1_list = []
            K2_list = []

            for line in fd:
                if is_valid_data_flag == 1:
                    tmp_line = line.replace("|", "")
                    if '---Round' in tmp_line:
                        index = tmp_line.find("-")
                        tmp_line = tmp_line[:index]
                    cur_tx_data = list(map(int, tmp_line.split()))
                    filtered_cur_frame_list.append(cur_tx_data[:rx_num])
                    unfiltered_cur_frame_list.append(cur_tx_data[-rx_num:])
                    tx_counter += 1
                    if tx_counter >= tx_num:
                        tx_counter = 0
                        is_valid_data_flag = 0
                        tmp_filtered_data.append(filtered_cur_frame_list)
                        tmp_unfiltered_data.append(unfiltered_cur_frame_list)
                        filtered_cur_frame_list = []
                        unfiltered_cur_frame_list = []

                        frame_counter += 1
                        if frame_counter >= frame_total:
                            if is_data_begin_flag == 1: # noise data
                                filtered_noise_list.append(tmp_filtered_data)
                                unfiltered_noise_list.append(tmp_unfiltered_data)
                            else:
                                filtered_diff_list.append(tmp_filtered_data)
                                unfiltered_diff_list.append(tmp_unfiltered_data)
                                is_frame_begin_flag = 0
                            is_data_begin_flag = 0
                            tmp_filtered_data = []
                            tmp_unfiltered_data = []

                if 'CA' in line and 'CF' in line and 'channel' in line and 'sample' in line and 'K1' in line and 'K2' in line:
                    is_frame_begin_flag = 1
                    K1_list.append(int(findall('\d+', line)[-3]))
                    K2_list.append(int(findall('\d+', line)[-1]))
                elif 'Test without touch' in line and 'noise' in line and is_frame_begin_flag:
                    is_data_begin_flag = 1
                    frame_total = int(findall('\d+', line)[-1])
                    frame_counter = 0
                elif 'Test with touch' in line and '7mm copper' in line and is_frame_begin_flag:
                    is_data_begin_flag = 2
                    frame_total = int(findall('\d+', line)[-1])
                    frame_counter = 0
                elif 'Filtered' in line and 'Un-filtered' in line and "rawdata" in line and is_data_begin_flag:
                    is_valid_data_flag = 1
                    tx_counter = 0

        finally:
            fd.close()

        return filtered_noise_list, filtered_diff_list, unfiltered_noise_list, unfiltered_diff_list, K1_list, K2_list

if __name__ == "__main__":

    """
    this is for test purpose
    """

    f_noise, f_diff, noise, diff, K1, K2 = read_txt("../test_data.txt").read()

    print(len(f_noise), len(f_noise[0]), len(f_noise[0][0]), len(f_noise[0][0][0]))
    print(len(f_diff), len(f_diff[0]), len(f_diff[0][0]), len(f_diff[0][0][0]))

    for i in range(len(f_noise)):
        for j in range(len(f_noise[i])):
            for k in range(len(f_noise[i][j])):
                print(f_noise[i][j][k], "    ", noise[i][j][k])
            print("\n")

    for i in range(len(f_diff)):
        for j in range(len(f_diff[i])):
            for k in range(len(f_diff[i][j])):
                print(f_diff[i][j][k], "    ", diff[i][j][k])
            print("\n")

    print(K1)
    print(K2)
