#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas

class read_excel_MIK:

    """
    For read and parse excel file
    """

    def __init__(self, filename):

        '''
        open excel file
        '''

        self.fd = pandas.ExcelFile(filename)
        self.test_type = self.read_test_type()
        if self.test_type == "point test":
            csv_filename = filename.replace(".xlsx", ".csv")
            self.csv_fd = pandas.read_csv(csv_filename, error_bad_lines=False, warn_bad_lines=False)
        elif self.test_type == "unknown test":
            print("Unknown xlsx data, can't support it")
            exit(0)

    def read_test_type(self):

        '''
        check whether it is line or point test
        '''

        result_sheet = self.fd.parse("Result Data")

        for key in result_sheet.keys():
            if ("Jitter" in str(key)) or ("Accuracy" in str(key) and "Precision" in str(key)):
                return "point test"
            elif "Linearity" in str(key):
                return "line test"

        return "unknown test"

    def read_config(self):

        '''
        read boundary, max_x, max_y information
        '''

        boundary_range = 5
        result_sheet = self.fd.parse("Result Data")
        edge_error_threshold = 1.5
        center_error_threshold = 1.0
        for (key, val) in result_sheet.items():
            for i in range(len(val)):
                if "Active Size" in str(val[i]):
                    max_x = result_sheet['Unnamed: 2'][i]
                    max_y = result_sheet['Unnamed: 3'][i]
                elif "Boundary" in str(val[i]):
                    boundary_range = result_sheet['Unnamed: 2'][i]
                elif "Edge Linearity" in str(val[i]):
                    edge_error_threshold = result_sheet['Unnamed: 2'][i]
                elif "CenterLinearity" in str(val[i]):
                    center_error_threshold = result_sheet['Unnamed: 2'][i]
        return [self.test_type, max_x, max_y, boundary_range, edge_error_threshold, center_error_threshold]

    def read_report_time(self):

        '''
        read report time for line test
        '''

        result_sheet = self.fd.parse("Result Data")

        report_time_list = []
        if self.test_type == "line test":
            for (key, val) in result_sheet.items():
                for i in range(len(val)):
                    if "Report Time" in str(val[i]):
                        report_time_list = val[i+2:]
                        break

        return report_time_list

    def read_pass_fail_info(self):

        '''
        read pass/fail information directly from Result Data sheet
        '''

        result_sheet = self.fd.parse("Result Data")

        pass_fail_list = []

        for (key, val) in result_sheet.items():
            for i in range(len(val)):
                if "Pass/Fail" in str(val[i]):
                    for j in range(100):
                        try:
                            pass_fail_info = str(val[i+2+j])

                            if "Pass" in pass_fail_info or "Failed" in pass_fail_info:
                                pass_fail_list.append(str(val[i+2+j]))
                            else:
                                break
                        except:
                            break

        print(pass_fail_list)
        if "Failed" in pass_fail_list:
            print("+++++++++++++%d+++++++++++++++++Bad news, failed" % (len(pass_fail_list)))
        else:
            print(">>>>>>>>>>>>>%d>>>>>>>>>>>>>>>>>Well done, mankind" % (len(pass_fail_list)))

        return pass_fail_list

    def read_linearity_error(self):

        '''
        read linearity directly from Result Data sheet
        '''

        result_sheet = self.fd.parse("Result Data")

        edge_max_list = []
        center_max_list = []
        if self.test_type == "line test":
            for (key, val) in result_sheet.items():
                for i in range(len(val)):
                    if "Edge Max(mm)" in str(val[i]):
                        for j in range(8):
                            edge_max_list.append(float(val[i+2+j]))
                        break
                for i in range(len(val)):
                    if "Center Max(mm)" in str(val[i]):
                        for j in range(8):
                            center_max_list.append(float(val[i+2+j]))
                        break

        self.read_pass_fail_info()

        return [edge_max_list, center_max_list]

    def read_target(self):

        '''
        get target from excel
        '''

        target_list = []

        if self.test_type == "point test":
            label_list = list(self.csv_fd.columns)
            measure_index = self.csv_fd[label_list[0]]
            pixel_x_list = self.csv_fd[label_list[1]]
            pixel_y_list = self.csv_fd[label_list[2]]
            # measure_index = self.csv_fd['Target : 1']
            # pixel_x_list = self.csv_fd['Pixel_X']
            # pixel_y_list = self.csv_fd[' Pixel_Y']
            for i in range(len(measure_index)):
                value = str(measure_index[i])
                if "Real Coordinate" in value:
                    target_list.append([float(pixel_x_list[i]), float(pixel_y_list[i])])
            # point_x = target_sheet['X']
            # point_y = target_sheet['Y']
            # for i in range(len(point_x)):
            #     target_list.append([point_x[i], point_y[i]])
        elif self.test_type == "line test":
            # only support MI line test
            # [self.test_type, max_x, max_y, boundary_range, edge_error_threshold, center_error_threshold]
            config_list = self.read_config()
            start_x = 3.5
            end_x = config_list[1] - 3.5
            start_y = 3.5
            end_y = config_list[2] - 3.5

            target_list.append([start_x, start_y, end_x, start_y])
            target_list.append([end_x, start_y, end_x, end_y])
            target_list.append([end_x, end_y, start_x, end_y])
            target_list.append([start_x, end_y, start_x, start_y])
            target_list.append([start_x, start_y, end_x, end_y])
            target_list.append([end_x, start_y, start_x, end_y])
            target_list.append([config_list[1] / 2, start_y, config_list[1] / 2, end_y])
            target_list.append([start_x, config_list[2] / 2, end_x, config_list[1] / 2])

        return target_list

    def read_measure(self):

        '''
        get measure data from excel
        '''

        measure_list_mm = []
        measure_list_pixel = []

        if self.test_type == "point test":
            label_list = list(self.csv_fd.columns)
            measure_index = self.csv_fd[label_list[0]]
            pixel_x_list = self.csv_fd[label_list[1]]
            pixel_y_list = self.csv_fd[label_list[2]]
            mm_x_list = self.csv_fd[' X']
            mm_y_list = self.csv_fd[' Y']

            measure_index_list = []
            start_index = 0

            for i in range(len(measure_index)):
                value = str(measure_index[i])
                if "Real" in value and "Coordinate" in value and start_index == 0:
                    start_index = i + 1
                elif "Target" in value and start_index > 0:
                    measure_index_list.append([start_index, i])
                    start_index = 0

            if start_index > 0:
                measure_index_list.append([start_index, len(measure_index) - 2])

            for index in measure_index_list:
                xy_list_mm = []
                xy_list_pixel = []
                for i in range(index[0], index[1]):
                    if str(mm_x_list[i]) != "nan" and str(mm_y_list[i]) != "nan":
                        xy_list_mm.append([float(mm_x_list[i]), float(mm_y_list[i])])
                    if str(pixel_x_list[i]) != "nan" and str(pixel_y_list[i]) != "nan":
                        xy_list_pixel.append([int(pixel_x_list[i]), int(pixel_y_list[i])])
                measure_list_mm.append(xy_list_mm)
                measure_list_pixel.append(xy_list_pixel)
        elif self.test_type == "line test":
            measure_sheet = self.fd.parse('Raw Data')
            measure_index = measure_sheet['Target : 1']
            measure_index_list = []
            start_index = 1
            for i in range(len(measure_index)):
                if "Target" in str(measure_index[i]):
                    measure_index_list.append([start_index, i - 1])
                    start_index = i + 2
            measure_index_list.append([start_index, len(measure_index)])

            mm_x_list = measure_sheet['mm']
            mm_y_list = measure_sheet['Unnamed: 5']
            pixel_x_list = measure_sheet['pixel']
            pixel_y_list = measure_sheet['Unnamed: 3']
            for (left, right) in measure_index_list:
                xy_list_mm = []
                xy_list_pixel = []
                for i in range(left, right):
                    xy_list_mm.append([mm_x_list[i], mm_y_list[i]])
                    xy_list_pixel.append([pixel_x_list[i], pixel_y_list[i]])
                measure_list_mm.append(xy_list_mm)
                measure_list_pixel.append(xy_list_pixel)

        return measure_list_mm, measure_list_pixel

    def destroy(self):

        '''
        destroy excel fd
        '''

        self.fd.close()

if __name__ == "__main__":

    """
    This is for test purpose
    """

    fd = read_excel_MIK("../H_Line/Result.xlsx")
    test_type, max_x, max_y, boundary_range = fd.read_config()
    target_list = fd.read_target()
    measure_list_mm, measure_list_pixel = fd.read_measure()
    print("This is %s, max_x = %f, max_y = %f, boundary_range = %f" % ( test_type, max_x, max_y, boundary_range ))
    for i in range(len(target_list)):
        print("\nNO.%d target line ---------------------- (%f, %f) -> (%f, %f)" % ( i + 1, target_list[i][0], target_list[i][1], target_list[i][2], target_list[i][3] ))
        for j in range(len(measure_list[i])):
            print("\tNO.%d measured point ---------------------------- (%f, %f)" % ( j + 1, measure_list_mm[i][j][0], measure_list_mm[i][j][1] ))
        print("\n")

    fd = read_excel_MIK("../POINTS/20180918175024.xlsx")
    test_type, max_x, max_y, boundary_range = fd.read_config()
    target_list = fd.read_target()
    measure_list_mm, measure_list_pixel = fd.read_measure()
    print("This is %s, max_x = %f, max_y = %f, boundary_range = %f" % ( test_type, max_x, max_y, boundary_range ))
    for i in range(len(target_list)):
        print("\nNO.%d target point ---------------------- (%f, %f)" % ( i + 1, target_list[i][0], target_list[i][1] ))
        for j in range(len(measure_list[i])):
            print("\tRepeat %d" % ( j + 1 ))
            for k in range(len(measure_list[i][j])):
                print("\t\tNO.%d measured point ---------------------------- (%f, %f)" % ( k + 1, measure_list_mm[i][j][k][0], measure_list_mm[i][j][k][1] ))
            print("\n")
