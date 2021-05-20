#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import sqrt

class point_analysis:

    """
    analysis point
    """

    def __init__(self, target_list, measure_list):

        '''
        initialize with target and measure data list
        '''

        self.target_list = target_list
        self.measure_list = measure_list

    def cal_accuracy(self):

        '''
        calculate point accuracy using formula:
        accuracy_x = mean(target_x - measure_x)
        accuracy_y = mean(target_y - measure_y)
        '''

        accuracy_x_list = []
        accuracy_y_list = []

        for i in range(len(self.target_list)):
            target_x = self.target_list[i][0]
            target_y = self.target_list[i][1]
            sum_x = 0.0
            sum_y = 0.0
            for (measure_x, measure_y) in self.measure_list[i]:
                # sum_x += abs(measure_x - target_x)
                # sum_y += abs(measure_y - target_y)
                sum_x += measure_x
                sum_y += measure_y
            # accuracy_x_list.append(sum_x / len(self.measure_list[i]))
            # accuracy_y_list.append(sum_y / len(self.measure_list[i]))
            accuracy_x_list.append(abs(sum_x / len(self.measure_list[i]) - target_x))
            accuracy_y_list.append(abs(sum_y / len(self.measure_list[i]) - target_y))

        return accuracy_x_list, accuracy_y_list

    def cal_jitter(self):

        '''
        calculate point linearity using formula:
        jitter_x = std(measure_x - mean_x)
        jitter_y = std(measure_y - mean_y)
        '''

        jitter_x_list = []
        jitter_y_list = []

        for i in range(len(self.target_list)):
            sum_x = 0.0
            sum_y = 0.0
            for (measure_x, measure_y) in self.measure_list[i]:
                sum_x += measure_x
                sum_y += measure_y
            mean_x = sum_x / len(self.measure_list[i])
            mean_y = sum_y / len(self.measure_list[i])

            sum_x = 0.0
            sum_y = 0.0
            for (measure_x, measure_y) in self.measure_list[i]:
                sum_x += ((measure_x - mean_x) ** 2)
                sum_y += ((measure_y - mean_y) ** 2)
            jitter_x_list.append(sqrt(sum_x / len(self.measure_list[i])))
            jitter_y_list.append(sqrt(sum_y / len(self.measure_list[i])))

        return jitter_x_list, jitter_y_list

if __name__ == "__main__":

    """
    this is only for test purpose
    """

    target_list = [[10, 10], [20, 20], [30, 30], [40, 40], [50, 50]]
    measure_list = [ \
            [[[10.01, 10.03], [10.01, 10.03], [10.01, 10.03], [10.01, 10.03], [10.01, 10.03]]], \
            [[[20.01, 20.03], [20.01, 20.03], [20.01, 20.03], [20.01, 20.03], [20.01, 20.03]]], \
            [[[30.01, 30.03], [30.01, 30.03], [30.01, 30.03], [30.01, 30.03], [30.01, 30.03]]], \
            [[[40.01, 40.03], [40.01, 40.03], [40.01, 40.03], [40.01, 40.03], [40.01, 40.03]]], \
            [[[50.01, 50.03], [50.01, 50.03], [50.01, 50.03], [50.01, 50.03], [50.01, 50.03]]]]
    point_fd = point_analysis(target_list, measure_list)
    accuracy_list = point_fd.cal_accuracy()
    precision_list = point_fd.cal_precision()
    linearity_list = point_fd.cal_linearity()
    for i in range(len(target_list)):
        print("\nNO.%d point, target coordinate (%f, %f)" % ( i + 1, target_list[i][0], target_list[i][1] ))
        for j in range(len(measure_list[i])):
            print("\tRepeat %d" % ( j + 1 ))
            for k in range(len(measure_list[i][j])):
                print("\t\tMeasured point %d ------------------------ (%f, %f)" % ( k + 1, measure_list[i][j][k][0], measure_list[i][j][k][1] ))
                print("\t\t\tAccuracy: (%f, %f)" % ( accuracy_list[i][j][k][0], accuracy_list[i][j][k][1] ))
                print("\t\t\tLinearity: %f" % ( linearity_list[i][j][k] ))
        print("Precision: (%f, %f)" % ( precision_list[i][0], precision_list[i][1] ))
