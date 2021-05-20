#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def is_digit_in_string(input_string):

    """
    check whether digit in string
    """

    return any(ch.isdigit() for ch in input_string)

class read_excel_TW:

    """
    For read and parse TW csv file
    """

    def __init__(self, csv_filename):

        '''
        open excel file
        '''

        self.filename = csv_filename
        self.pixel_x = 474
        self.pixel_y = 474
        self.test_type = self.read_test_type()

        if self.test_type == "unknown test":
            print("Unknown xlsx data, can't support it")
            exit(0)

    def read_test_type(self):

        '''
        check whether it is line or point test
        '''

        fd = open(self.filename, 'r', encoding="big5")

        try:
            for line in fd:
                if "測試項目" in line:
                    if "線性測試" in line:
                        return "line test"
                    elif "點擊測試" in line:
                        return "point test"
        finally:
            fd.close()

        return "unknown test"

    def read_config(self):

        '''
        read boundary, max_x, max_y information
        '''

        boundary_range = 5
        edge_error_threshold = 1.5
        center_error_threshold = 1.0
        max_x = 0
        max_y = 0

        fd = open(self.filename, 'r', encoding="big5")
        try:
            for line in fd:
                if max_x > 0 and max_y > 0:
                    break

                if "X(Pixel)" in line and "測試區X長(mm)" in line:
                    tmp_list = list(line.split(","))
                    self.pixel_x = float(tmp_list[1])
                    max_x = float(tmp_list[3])
                elif "Y(Pixel)" in line and "測試區Y長(mm)" in line:
                    tmp_list = list(line.split(","))
                    self.pixel_y = float(tmp_list[1])
                    max_y = float(tmp_list[3])
        finally:
            fd.close()

        return [self.test_type, max_x, max_y, boundary_range, edge_error_threshold, center_error_threshold]

    def read_report_time(self):

        '''
        read report time for line test
        '''

        report_time_list = []
        return report_time_list

    def read_linearity_error(self):

        '''
        read linearity directly from Result Data sheet
        '''

        return []

    def read_target(self):

        '''
        get target from excel
        '''

        target_list = []
        config_list = self.read_config()

        is_data_start = 0
        valid_data_begin_flag = 0

        fd = open(self.filename, 'r', encoding="big5")

        if self.test_type == "point test":
            try:
                for line in fd:
                    if is_data_start and valid_data_begin_flag == 1:
                        if is_digit_in_string(line):
                            tmp_list = list(line.split(","))
                            point_x = float(tmp_list[1]) * config_list[1] / self.pixel_x
                            point_y = float(tmp_list[2]) * config_list[2] / self.pixel_y
                            target_list.append([point_x, point_y])
                            valid_data_begin_flag = 0
                    elif valid_data_begin_flag >= 2:
                        valid_data_begin_flag -= 1

                    if "X1" in line and "Y1" in line and "X2" in line and "Y2" in line and "誤差" in line:
                        valid_data_begin_flag = 1
                        is_data_start = 1
                    elif "點到點最大誤差" in line:
                        if is_data_start:
                            valid_data_begin_flag = 1
            finally:
                fd.close()
        elif self.test_type == "line test":
            try:
                for line in fd:
                    if is_data_start and valid_data_begin_flag == 1:
                        if is_digit_in_string(line):
                            tmp_list = list(line.split(","))
                            start_x = float(tmp_list[1]) * config_list[1] / self.pixel_x
                            start_y = float(tmp_list[2]) * config_list[2] / self.pixel_y
                            end_x = float(tmp_list[3]) * config_list[1] / self.pixel_x
                            end_y = float(tmp_list[4]) * config_list[2] / self.pixel_y
                            target_list.append([start_x, start_y, end_x, end_y])
                            valid_data_begin_flag = 0
                    elif valid_data_begin_flag >= 2:
                        valid_data_begin_flag -= 1

                    if "SX" in line and "SY" in line and "EX" in line and "EY" in line and "誤差" in line:
                        valid_data_begin_flag = 1
                        is_data_start = 1
                    elif "平均偏差" in line:
                        if is_data_start:
                            valid_data_begin_flag = 1
            finally:
                fd.close()

        return target_list

    def read_measure(self):

        '''
        get measure data from excel
        '''

        frame_pixel_list = []
        measure_list_mm = []
        measure_list_pixel = []
        config_list = self.read_config()

        is_data_start = 0
        valid_data_begin_flag = 0

        fd = open(self.filename, 'r', encoding="big5")

        if self.test_type == "point test":
            try:
                for line in fd:
                    if "X1" in line and "Y1" in line and "X2" in line and "Y2" in line and "誤差" in line:
                        valid_data_begin_flag = 2
                        is_data_start = 1
                    elif "平均誤差" in line:
                        if is_data_start:
                            valid_data_begin_flag = 0
                            measure_list_pixel.append(frame_pixel_list)
                            frame_pixel_list = []
                    elif "點到點最大誤差" in line:
                        if is_data_start:
                            valid_data_begin_flag = 2

                    if is_data_start and valid_data_begin_flag == 1:
                        if is_digit_in_string(line):
                            tmp_list = list(line.split(","))
                            frame_pixel_list.append([float(tmp_list[3]), float(tmp_list[4])])
                    elif valid_data_begin_flag >= 2:
                        valid_data_begin_flag -= 1
            finally:
                fd.close()
        elif self.test_type == "line test":
            try:
                for line in fd:
                    if "SX" in line and "SY" in line and "EX" in line and "EY" in line and "誤差" in line:
                        valid_data_begin_flag = 2
                        is_data_start = 1
                    elif "平均偏差" in line:
                        if is_data_start:
                            valid_data_begin_flag = 2
                            measure_list_pixel.append(frame_pixel_list)
                            frame_pixel_list = []

                    if is_data_start and valid_data_begin_flag == 1:
                        if is_digit_in_string(line):
                            tmp_list = list(line.split(","))
                            frame_pixel_list.append([float(tmp_list[5]), float(tmp_list[6])])
                    elif valid_data_begin_flag >= 2:
                        valid_data_begin_flag -= 1

            finally:
                fd.close()

        for frame_pixel in measure_list_pixel:
            frame_mm_list = []
            for (pix_x, pix_y) in frame_pixel:
                mm_x = pix_x * config_list[1] / self.pixel_x
                mm_y = pix_y * config_list[2] / self.pixel_y
                frame_mm_list.append([mm_x, mm_y])
            measure_list_mm.append(frame_mm_list)

        return measure_list_mm, measure_list_pixel

    def destroy(self):

        '''
        destroy excel fd
        '''

        return 0

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
