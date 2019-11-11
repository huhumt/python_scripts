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
        all_accuracy_x = max(max of all point accuracy in x)
        single_point_accuracy = max(abs(target_list[i] - measure_list[i]))
        '''

        accuracy_list = [0] * len(self.target_list)
        for i in range(len(self.target_list)):
            target_x = self.target_list[i][0]
            target_y = self.target_list[i][1]
            point_list = []
            for repeat in self.measure_list[i]:
                repeat_list = []
                for (measure_x, measure_y) in repeat:
                    delta_x = abs(measure_x - target_x)
                    delta_y = abs(measure_y - target_y)
                    repeat_list.append([delta_x, delta_y])
                point_list.append(repeat_list)
            accuracy_list[i] = point_list

        return accuracy_list

    def cal_precision(self):

        '''
        calculate point precision using formula:
        all_precision_x = max(max of all point precision in x)
        sigle_point_precision_x = 2 * sqrt(sum(measure_x ^ 2) / len(measure_list) - aver(measure_list) ^ 2)
        '''

        precision_list = [[0, 0]] * len(self.target_list)
        for i in range(len(self.target_list)):
            sum_x = 0
            sum_y = 0
            square_x_sum = 0
            square_y_sum = 0
            counter = 0
            for repeat in self.measure_list[i]:
                for (measure_x, measure_y) in repeat:
                    sum_x += measure_x
                    sum_y += measure_y
                    square_x_sum += (measure_x * measure_x)
                    square_y_sum += (measure_y * measure_y)
                    counter += 1
            aver_x = sum_x / counter
            aver_y = sum_y / counter
            square_aver_x = square_x_sum / counter
            square_aver_y = square_y_sum / counter
            x_standard_deviation = sqrt(abs(square_aver_x - aver_x * aver_x))
            y_standard_deviation = sqrt(abs(square_aver_y - aver_y * aver_y))

            precision_list[i] = [2. * x_standard_deviation, 2. * y_standard_deviation]

        return precision_list

    def cal_linearity(self):

        '''
        calculate point linearity using formula:
        all_linearity = max(all linearity)
        single_point_linearity = distance(measure, target)
        '''

        linearity_list = [0] * len(self.target_list)
        for i in range(len(self.target_list)):
            target_x = self.target_list[i][0]
            target_y = self.target_list[i][1]
            point_list = []
            for repeat in self.measure_list[i]:
                repeat_list = []
                for (measure_x, measure_y) in repeat:
                    delta_x = measure_x - target_x
                    delta_y = measure_y - target_y
                    distance = sqrt(delta_x * delta_x + delta_y * delta_y)
                    repeat_list.append(distance)
                point_list.append(repeat_list)
            linearity_list[i] = point_list

        return linearity_list


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
