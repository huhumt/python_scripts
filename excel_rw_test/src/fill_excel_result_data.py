#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from get_boundary_list import get_shadow_point
from line_analysis import line_analysis
from xlrd import open_workbook
from xlutils.copy import copy
from math import sqrt
# example usage:
# sh.cell_value(rowx=1, colx=1)
# for i in range(sh.nrows)
# for i in range(sh.ncols)
# sh.row(1)
# sh.col(1)
def generate_point_result_data(boundary_index_list, target_list, measure_list_mm, accuracy_list, linearity_list, precision_list):

    # target_x, target_y, measure_x, measure_y, accuracy_x, accuracy_y, precision_x, precision_y, linearity
    result_data_list = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] for i in range(len(target_list))]
    for i in range(len(measure_list_mm)):
        max_accuray = [[0, 0, 0, 0], [0, 0, 0, 0]]
        max_linearity = 0
        for j in range(len(measure_list_mm[i])):
            for k in range(len(measure_list_mm[i][j])):
                accuracy_x = accuracy_list[i][j][k][0]
                accuracy_y = accuracy_list[i][j][k][1]
                if accuracy_x > max_accuray[0][0]:
                    max_accuray[0][0] = accuracy_x
                    max_accuray[0][1] = i
                    max_accuray[0][2] = j
                    max_accuray[0][3] = k
                if accuracy_y > max_accuray[1][0]:
                    max_accuray[1][0] = accuracy_y
                    max_accuray[1][1] = i
                    max_accuray[1][2] = j
                    max_accuray[1][3] = k
                if linearity_list[i][j][k] > max_linearity:
                    max_linearity = linearity_list[i][j][k]
        result_data_list[i][0] = target_list[i][0]
        result_data_list[i][1] = target_list[i][1]
        if max_accuray[0][0] > max_accuray[1][0]:
            result_data_list[i][2] = measure_list_mm[max_accuray[0][1]][max_accuray[0][2]][max_accuray[0][3]][0]
            result_data_list[i][3] = measure_list_mm[max_accuray[0][1]][max_accuray[0][2]][max_accuray[0][3]][1]
        else:
            result_data_list[i][2] = measure_list_mm[max_accuray[1][1]][max_accuray[1][2]][max_accuray[1][3]][0]
            result_data_list[i][3] = measure_list_mm[max_accuray[1][1]][max_accuray[1][2]][max_accuray[1][3]][1]
        result_data_list[i][4] = max_accuray[0][0]
        result_data_list[i][5] = max_accuray[1][0]
        result_data_list[i][6] = precision_list[i][0]
        result_data_list[i][7] = precision_list[i][1]
        result_data_list[i][8] = max_linearity
    return result_data_list

def fill_point_test_result_data_sheet(filename, xlsx_data):

    #xlsx_data_list: boundary_index_list, target_list, measure_list_mm, accuracy_list, linearity_list, precision_list
    #    boundary_max_accuracy[0], center_max_accuracy[0], boundary_max_linearity[0], center_max_linearity[0]
    result_data_list = generate_point_result_data(xlsx_data[0], xlsx_data[1], xlsx_data[2], xlsx_data[3], xlsx_data[4], xlsx_data[5])
    # print(xlsx_data[6], xlsx_data[7], xlsx_data[8], xlsx_data[9], len(xlsx_data))

    read_fd = open_workbook(filename)
    read_data_sheet = read_fd.sheet_by_name("Result Data")
    write_fd = copy(read_fd)
    write_data_sheet = write_fd.get_sheet(0)
    for i in range(read_data_sheet.nrows):
        for j in range(read_data_sheet.ncols):
            cell_val = str(read_data_sheet.cell_value(rowx=i, colx=j))
            if "Active Size[mm]" in cell_val:
                write_data_sheet.write(i, j+1, "64.8")
                write_data_sheet.write(i, j+2, "136.69")
                break
            elif "Touch Resolution[pixel]" in cell_val:
                write_data_sheet.write(i, j+1, "1080")
                write_data_sheet.write(i, j+2, "2280")
                break
            elif "Edge Linearity Max[mm]" in cell_val:
                write_data_sheet.write(i, j+1, str(round(xlsx_data[6], 3)))
                break
            elif "Center Linearity Max[mm]" in cell_val:
                write_data_sheet.write(i, j+1, str(round(xlsx_data[7], 3)))
                break
            elif "Edge Precision Max[mm]" in cell_val:
                write_data_sheet.write(i, j+1, str(round(xlsx_data[8][0][0], 3)))
                write_data_sheet.write(i, j+2, str(round(xlsx_data[8][1][0], 3)))
                break
            elif "Center Precision Max[mm]" in cell_val:
                write_data_sheet.write(i, j+1, str(round(xlsx_data[9][0][0], 3)))
                write_data_sheet.write(i, j+2, str(round(xlsx_data[9][1][0], 3)))
                break
            elif "Touch Point" in cell_val:
                for m in range(len(result_data_list)):
                    for n in range(len(result_data_list[m])):
                        write_data_sheet.write(i+2+m, j+1+n, str(round(result_data_list[m][n], 3)))
                    pass_flag = "Pass"
                    if m in xlsx_data[0]:
                        error_threshold = 1.5
                    else:
                        error_threshold = 1.0
                    for ll in range(4, len(result_data_list[m])):
                        if result_data_list[m][ll] > error_threshold:
                            pass_flag = "Failed"
                            print("\n*****************************************")
                            print("*****************************************")
                            print("***********WARNING*************************")
                            print("***********FAILED DETECTED*********************")
                            print("*****************************************")
                            print("*****************************************\n")
                            break
                    write_data_sheet.write(i+2+m, j+12, pass_flag)
                break
    save_filename = filename.replace(".xlsx", "_result_output.xlsx")
    write_fd.save(save_filename)

def get_max_delta(point_list):

    max_delta = 0.0
    for i in range(len(point_list) - 1):
        delta_x = point_list[i][0] - point_list[i + 1][0]
        delta_y = point_list[i][1] - point_list[i + 1][1]
        delta = sqrt(delta_x * delta_x + delta_y * delta_y)
        if delta > max_delta:
            max_delta = delta
    return max_delta


def generate_line_result_data(boundary_index_list, target_list, measure_list_mm, linearity_list):

    # target_x, target_y, measure_x, measure_y, edge_max, center_max, max_distance
    result_data_list = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] for i in range(len(target_list))]
    slash_k_b_list = line_analysis(target_list, measure_list_mm).get_target_line_formula()
    for i in range(len(linearity_list)):
        max_edge = [0.0, 0]
        max_center = [0.0, 0]
        for j in range(len(linearity_list[i])):
            linearity = linearity_list[i][j]
            if j in boundary_index_list[i]:
                if linearity > max_edge[0]:
                    max_edge[0] = linearity
                    max_edge[1] = j
            else:
                if linearity > max_center[0]:
                    max_center[0] = linearity
                    max_center[1] = j
        if max_edge[0] > max_center[0]:
            measure_x = measure_list_mm[i][max_edge[1]][0]
            measure_y = measure_list_mm[i][max_edge[1]][1]
        else:
            measure_x = measure_list_mm[i][max_center[1]][0]
            measure_y = measure_list_mm[i][max_center[1]][1]
        x, y = get_shadow_point(slash_k_b_list[i], measure_x, measure_y, target_list[i][0])
        result_data_list[i][0] = x
        result_data_list[i][1] = y
        result_data_list[i][2] = measure_x
        result_data_list[i][3] = measure_y
        result_data_list[i][4] = max_edge[0]
        result_data_list[i][5] = max_center[0]
        result_data_list[i][6] = get_max_delta(measure_list_mm[i])
        # print(len(measure_list_mm), len(measure_list_mm[i]), len(linearity_list))
    return result_data_list

def fill_line_test_result_data_sheet(filename, report_time, xlsx_data):

    # xlsx_data: boundary_index_list, target_list, measure_list, linearity_list, max_edge, max_center
    result_data_list = generate_line_result_data(xlsx_data[0], xlsx_data[1], xlsx_data[2], xlsx_data[3])

    read_fd = open_workbook(filename)
    read_data_sheet = read_fd.sheet_by_name("Result Data")
    write_fd = copy(read_fd)
    write_data_sheet = write_fd.get_sheet(0)
    for i in range(read_data_sheet.nrows):
        for j in range(read_data_sheet.ncols):
            cell_val = str(read_data_sheet.cell_value(rowx=i, colx=j))
            if "Active Size[mm]" in cell_val:
                write_data_sheet.write(i, j+1, "64.8")
                write_data_sheet.write(i, j+2, "136.69")
                break
            elif "Touch Resolution[pixel]" in cell_val:
                write_data_sheet.write(i, j+1, "1080")
                write_data_sheet.write(i, j+2, "2280")
                break
            elif "Edge Linearity Max[mm]" in cell_val:
                write_data_sheet.write(i, j+1, str(round(xlsx_data[-2], 3)))
                break
            elif "Center Linearity Max[mm]" in cell_val:
                write_data_sheet.write(i, j+1, str(round(xlsx_data[-1], 3)))
                break
            elif "Touch Point" in cell_val:
                # target_x, target_y, measure_x, measure_y, edge_max, center_max, max_distance
                for m in range(len(result_data_list)):
                    write_data_sheet.write(i+2+m, j, str(m+1))
                    for n in range(len(result_data_list[m]) - 1):
                        write_data_sheet.write(i+2+m, j+1+n, str(round(result_data_list[m][n], 3)))
                    if len(report_time) > 0:
                        write_data_sheet.write(i+2+m, j+7, str(report_time[m]))
                    write_data_sheet.write(i+2+m, j+8, str(round(result_data_list[m][-1], 3)))
                    if result_data_list[m][-3] < 1.5 and result_data_list[m][-2] < 1.0:
                        write_data_sheet.write(i+2+m, j+9, "Pass")
                    else:
                        write_data_sheet.write(i+2+m, j+9, "Failed")
                        print("\n*****************************************")
                        print("*****************************************")
                        print("***********WARNING*************************")
                        print("***********FAILED DETECTED*********************")
                        print("*****************************************")
                        print("*****************************************\n")
                break
    save_filename = filename.replace(".xlsx", "_result_output.xlsx")
    write_fd.save(save_filename)
