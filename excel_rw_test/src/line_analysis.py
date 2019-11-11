#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import sqrt

class line_analysis:

    """
    analysis line test data to get linearity
    """

    def __init__(self, target_list, measure_list):

        '''
        init with target and measure
        '''

        self.target_list = target_list
        self.measure_list = measure_list

    def get_target_line_formula(self):

        '''
        generate target line formula based on start point and end point
        output k, b list for y = k * x + b
        '''

        slash_k_b_list = []
        for (start_x, start_y, end_x, end_y) in self.target_list:
            if end_x == start_x:
                slash_k_b_list.append([])
            else:
                slash_k = (end_y - start_y) / (end_x - start_x)
                slash_b = end_y - slash_k * end_x
                slash_k_b_list.append([slash_k, slash_b])

        return slash_k_b_list

    def cal_linearity(self):

        '''
        calculate line linearity using formula:
        all_linearity = max(max of all point linearity)
        single_linearity = max(point to line distance)
        '''

        linearity_list = []
        slash_k_b_list = self.get_target_line_formula()
        for i in range(len(self.target_list)):
            distance_list = []
            for measure_x, measure_y in self.measure_list[i]:
                if slash_k_b_list[i]:
                    slash_k = slash_k_b_list[i][0]
                    slash_b = slash_k_b_list[i][1]
                    distance = abs(slash_k * measure_x - measure_y + slash_b) / sqrt(slash_k * slash_k + 1)
                else:
                    distance = abs(measure_x - self.target_list[i][0])
                distance_list.append(distance)
            linearity_list.append(distance_list)

        return linearity_list

if __name__ == "__main__":

    """
    this is only for test purpose
    """

    target_list = [[10, 10, 1000, 1000]]
    measure_list = [[[10.01, 10.05], [20.22, 20.55], [100.78, 100.99]]]
    linearity_list = line_analysis(target_list, measure_list).cal_linearity()
    max_list = []
    for i in range(len(linearity_list)):
        print("\tLine %d, linearity: %f" % ( i + 1, max(linearity_list[i]) ))
        max_list.append(max(linearity_list[i]))
    print("\nTotal line linearity: %f, index: %d" % ( max(max_list), max_list.index(max(max_list)) ))
