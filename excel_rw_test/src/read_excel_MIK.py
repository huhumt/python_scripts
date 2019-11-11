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
            if "Linearity" in key:
                if "Accuracy" in key and "Precision" in key:
                    return "point test"
                else:
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
            if "Linearity" in key:
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
                break
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

    def read_target(self):

        '''
        get target from excel
        '''

        target_list = []

        if self.test_type == "point test":
            measure_index = self.csv_fd['Target : 1']
            pixel_x_list = self.csv_fd['Pixel_X']
            pixel_y_list = self.csv_fd[' Pixel_Y']
            for i in range(len(measure_index)):
                value = str(measure_index[i])
                if "Real Coordinate" in value:
                    target_list.append([float(pixel_x_list[i]), float(pixel_y_list[i])])
            # point_x = target_sheet['X']
            # point_y = target_sheet['Y']
            # for i in range(len(point_x)):
            #     target_list.append([point_x[i], point_y[i]])
        else:
            for sheet_name in self.fd.sheet_names:
                if sheet_name not in ["Result Data", "Graph", "Raw Data", "analysis_output"]:
                    target_sheet = self.fd.parse(sheet_name)
                    keys = target_sheet.keys()
                    if "Start X" in keys and "Start Y" in keys and "End X" in keys and "End Y" in keys:
                        start_x = target_sheet['Start X']
                        start_y = target_sheet['Start Y']
                        end_x = target_sheet['End X']
                        end_y = target_sheet['End Y']
                        for i in range(len(start_x)):
                            x0 = str(start_x[i])
                            y0 = str(start_y[i])
                            x1 = str(end_x[i])
                            y1 = str(end_y[i])
                            if x0 and y0 and x1 and y1:
                                target_list.append([float(x0), float(y0), float(x1), float(y1)])
                        return target_list

        return target_list

    def read_measure(self):

        '''
        get measure data from excel
        '''

        measure_list_mm = []
        measure_list_pixel = []

        if self.test_type == "point test":
            measure_index = self.csv_fd['Target : 1']
            new_point_flag = 1
            start_index = 0
            measure_index_list = []
            repeat_index_list = []
            for i in range(len(measure_index)):
                value = str(measure_index[i])
                if "Target" in value:
                    if new_point_flag == 0:
                        repeat_index_list.append([start_index, i])
                        measure_index_list.append(repeat_index_list)
                        repeat_index_list = []
                    new_point_flag = 1
                elif "Repeat" in value:
                    if new_point_flag == 1:
                        new_point_flag = 0
                    else:
                        repeat_index_list.append([start_index, i])
                    start_index = i + 1
                elif "Worst" in value:
                    repeat_index_list.append([start_index, i])
                    measure_index_list.append(repeat_index_list)
                    repeat_index_list = []
            mm_x_list = self.csv_fd[' X']
            mm_y_list = self.csv_fd[' Y']
            pixel_x_list = self.csv_fd['Pixel_X']
            pixel_y_list = self.csv_fd[' Pixel_Y']
            # del measure_index_list[-1]
            for index in measure_index_list:
                xy_list_mm = []
                xy_list_pixel = []
                for (start, end) in index:
                    repeat_list_mm = []
                    repeat_list_pixel = []
                    for i in range(start, end):
                        if str(mm_x_list[i]) != "nan" and str(mm_y_list[i]) != "nan":
                            repeat_list_mm.append([float(mm_x_list[i]), float(mm_y_list[i])])
                        if str(pixel_x_list[i]) != "nan" and str(pixel_y_list[i]) != "nan":
                            repeat_list_pixel.append([int(pixel_x_list[i]), int(pixel_y_list[i])])
                    xy_list_mm.append(repeat_list_mm)
                    xy_list_pixel.append(repeat_list_pixel)
                measure_list_mm.append(xy_list_mm)
                measure_list_pixel.append(xy_list_pixel)
        else:
            measure_sheet = self.fd.parse('Raw Data')
            measure_index = measure_sheet['Target : 1']
            measure_index_list = []
            start_index = 1
            for i in range(len(measure_index)):
                if "Target" in str(measure_index[i]):
                    measure_index_list.append([start_index, i - 1])
                    start_index = i + 2

            mm_x_list = measure_sheet['mm']
            mm_y_list = measure_sheet['Unnamed: 5']
            pixel_x_list = measure_sheet['pixel']
            pixel_y_list = measure_sheet['Unnamed: 3']
            for index in measure_index_list:
                start_index = index[0]
                end_index = index[1]
                xy_list_mm = []
                xy_list_pixel = []
                for i in range(start_index, end_index):
                    xy_list_mm.append([mm_x_list[i], mm_y_list[i]])
                    xy_list_pixel.append([pixel_x_list[i], pixel_y_list[i]])
                measure_list_mm.append(xy_list_mm)
                measure_list_pixel.append(xy_list_pixel)

            xy_list_mm = []
            xy_list_pixel = []
            for i in range(measure_index_list[-1][1] + 3, len(measure_index)):
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
