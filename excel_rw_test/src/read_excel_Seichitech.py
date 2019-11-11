#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xlrd
# example usage:
# sh.cell_value(rowx=1, colx=1)
# for i in range(sh.nrows)
# for i in range(sh.ncols)
# sh.row(1)
# sh.col(1)

class read_excel_Seichitech:

    """
    for read Seichitech excel file
    """

    def __init__(self, filename):

        '''
        open excel file
        '''

        self.fd = xlrd.open_workbook(filename)
        self.test_type = self.read_test_type()

    def read_test_type(self):

        '''
        check it's point/line test
        '''

        data_sheet = self.fd.sheet_by_name("详细数据-指头1")
        for i in range(data_sheet.nrows):
            header = data_sheet.cell_value(rowx=i, colx=0)
            if "目标点X" in header:
                return "point test"
            elif "X(物理)" in header:
                return "line test"

        print("Unsupported xlsx file")
        exit(0)

    def read_config(self):

        '''
        for there is no config parameter in Seichitech xlsx, return 0
        '''

        return [self.test_type, 0, 0, 0, 1.5, 1.0]

    def read_report_time(self):

        '''
        there is no report time at all, report empty list
        '''

        return []

    def read_target(self):

        '''
        get target from excel
        '''

        target_list = []
        if self.test_type == "point test":
            data_sheet = self.fd.sheet_by_name("详细数据-指头1")
            for i in range(data_sheet.nrows):
                header = data_sheet.cell_value(rowx=i, colx=0)
                if "目标点X" in header:
                    target_x = data_sheet.cell_value(rowx=i, colx=1)
                    target_y = data_sheet.cell_value(rowx=i+1, colx=1)
                    target_list.append([target_x, target_y])
        elif self.test_type == "line test":
            sheet_names = self.fd.sheet_names()
            sheet_list = ["测试结果", "详细数据-指头1"]
            for name in sheet_names:
                if name not in sheet_list:
                    target_sheet = self.fd.sheet_by_name(name)
                    if target_sheet.nrows > 0 and target_sheet.ncols > 0:
                        start_xy = []
                        end_xy = []
                        for i in range(target_sheet.nrows):
                            value = target_sheet.cell_value(rowx=i, colx=target_sheet.ncols-1)
                            if ":L" in value:
                                start_xy = ((value.split(":L", 1)[1])[1:-1]).split("，")
                            elif ":M" in value:
                                end_xy = ((value.split(":M", 1)[1])[1:-1]).split("，")

                            if start_xy and end_xy:
                                target_list.append([float(start_xy[0]), float(start_xy[1]), float(end_xy[0]), float(end_xy[1])])
                                start_xy = []
                                end_xy = []
                        break
        return target_list

    def read_measure(self):

        '''
        get measure from excel
        '''

        measure_list_mm = []
        measure_list_pixel = []
        data_sheet = self.fd.sheet_by_name("详细数据-指头1")
        for i in range(data_sheet.nrows):
            header = data_sheet.cell_value(rowx=i, colx=0)
            if "X(像素)" in header:
                point_list_mm = []
                point_list_pixel = []
                for j in range(1, data_sheet.ncols):
                    pixel_x = str(data_sheet.cell_value(rowx=i, colx=j))
                    pixel_y = str(data_sheet.cell_value(rowx=i+1, colx=j))
                    mm_x = str(data_sheet.cell_value(rowx=i+2, colx=j))
                    mm_y = str(data_sheet.cell_value(rowx=i+3, colx=j))
                    if mm_x and mm_y and mm_x != '-' and mm_y != '-': # not empty
                        point_list_mm.append([float(mm_x), float(mm_y)])
                    if pixel_x and pixel_y and pixel_x != '-' and pixel_y != '-': # not empty
                        point_list_pixel.append([int(float(pixel_x)), int(float(pixel_y))])
                if self.test_type == "point test":
                    measure_list_mm.append([point_list_mm])
                    measure_list_pixel.append([point_list_pixel])
                elif self.test_type == "line test":
                    measure_list_mm.append(point_list_mm)
                    measure_list_pixel.append(point_list_pixel)

        return measure_list_mm, measure_list_pixel

    def destroy(self):

        '''
        close excel fd
        '''

        self.fd.close()

if __name__ == "__main__":

    """
    this is for test purpose
    """

    fd = read_excel_Seichitech("../data_20170904203335.xlsx")
    test_type, max_x, max_y, boundary_list = fd.read_config()
    if test_type == "line test":
        print("line test")
    elif test_type == "point test":
        print("point test")
    target_list = fd.read_target()
    measure_list_mm, measure_list_pixel = fd.read_measure()
    # for i in range(len(measure_list)):
    #     print(target_list[i])
    #     print(measure_list_mm[i])
    #     print(measure_list_pixel[i])
    fd = read_excel_Seichitech("../data_20170904203901.xlsx")
    test_type, max_x, max_y, boundary_list = fd.read_config()
    if test_type == "line test":
        print("line test")
    elif test_type == "point test":
        print("point test")
    target_list = fd.read_target()
    # print(target_list)
    measure_list_mm, measure_list_pixel = fd.read_measure()
    # print(measure_list_mm[0])
