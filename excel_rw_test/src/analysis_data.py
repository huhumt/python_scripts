#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fill_excel_result_data import fill_line_test_result_data_sheet, fill_point_test_result_data_sheet
from point_analysis import point_analysis
from line_analysis import line_analysis

def analysis_point_max_accuracy(boundary_index_list, accuracy_list):

    """
    anaylysis max accuracy for center and boundary area
    """

    boundary_max_accuracy = [[0, [0, 0, 0]], [0, [0, 0, 0]]]
    center_max_accuracy = [[0, [0, 0, 0]], [0, [0, 0, 0]]]
    for i in range(len(accuracy_list)):
        for j in range(len(accuracy_list[i])):
            max_xy = [[0, 0], [0, 0]]
            for k in range(len(accuracy_list[i][j])):
                x = accuracy_list[i][j][k][0]
                y = accuracy_list[i][j][k][1]
                if x > max_xy[0][0]:
                    max_xy[0][0] = x
                    max_xy[0][1] = k
                if y > max_xy[1][0]:
                    max_xy[1][0] = y
                    max_xy[1][1] = k
            if i in boundary_index_list:
                if max_xy[0][0] > boundary_max_accuracy[0][0]:
                    boundary_max_accuracy[0][0] = max_xy[0][0]
                    boundary_max_accuracy[0][1] = [i, j, max_xy[0][1]]
                if max_xy[1][0] > boundary_max_accuracy[1][0]:
                    boundary_max_accuracy[1][0] = max_xy[1][0]
                    boundary_max_accuracy[1][1] = [i, j, max_xy[1][1]]
            else:
                if max_xy[0][0] > center_max_accuracy[0][0]:
                    center_max_accuracy[0][0] = max_xy[0][0]
                    center_max_accuracy[0][1] = [i, j, max_xy[0][1]]
                if max_xy[1][0] > center_max_accuracy[1][0]:
                    center_max_accuracy[1][0] = max_xy[1][0]
                    center_max_accuracy[1][1] = [i, j, max_xy[1][1]]
    return boundary_max_accuracy, center_max_accuracy

def analysis_point_max_linearity(boundary_index_list, linearity_list):

    """
    analysis max linearity for center and boundary area
    """

    boundary_max_linearity = [0, [0, 0, 0]]
    center_max_linearity = [0, [0, 0, 0]]
    for i in range(len(linearity_list)):
        for j in range(len(linearity_list[i])):
            max_val = max(linearity_list[i][j])
            max_val_index = linearity_list[i][j].index(max_val)
            if i in boundary_index_list:
                if max_val > boundary_max_linearity[0]:
                    boundary_max_linearity[0] = max_val
                    boundary_max_linearity[1] = [i, j, max_val_index]
            else:
                if max_val > center_max_linearity[0]:
                    center_max_linearity[0] = max_val
                    center_max_linearity[1] = [i, j, max_val_index]
    return boundary_max_linearity, center_max_linearity

def analysis_point_max_precision(boundary_index_list, precision_list):

    """
    analysis max precision for center and boundary list
    """

    boundary_max_precision = [[0, 0], [0, 0]]
    center_max_precision = [[0, 0], [0, 0]]
    for i in range(len(precision_list)):
        x = precision_list[i][0]
        y = precision_list[i][1]
        if i in boundary_index_list:
            if x > boundary_max_precision[0][0]:
                boundary_max_precision[0][0] = x
                boundary_max_precision[0][1] = i
            if y > boundary_max_precision[1][0]:
                boundary_max_precision[1][0] = y
                boundary_max_precision[1][1] = i
        else:
            if x > center_max_precision[0][0]:
                center_max_precision[0][0] = x
                center_max_precision[0][1] = i
            if y > center_max_precision[1][0]:
                center_max_precision[1][0] = y
                center_max_precision[1][1] = i
    return boundary_max_precision, center_max_precision

def analysis_point_accurcay(target_list, measure_list_mm, boundary_index_list, accuracy_list):

    """
    analysis max boundary/center error
    """

    boundary_max_accuracy, center_max_accuracy = analysis_point_max_accuracy(boundary_index_list, accuracy_list)
    print("\tAccuracy:")
    print_accuracy_list = [["boundary", boundary_max_accuracy], ["center  ", center_max_accuracy]]
    for print_accuracy in print_accuracy_list:
        name = "Max " + print_accuracy[0] + " Accuracy_x: "
        for xy in range(2): # first print x, then y
            max_A = print_accuracy[1][xy][0]
            max_i = print_accuracy[1][xy][1][0]
            max_j = print_accuracy[1][xy][1][1]
            max_k = print_accuracy[1][xy][1][2]
            print("\t\t%s%f ---------------- target_x: %f, measure_x: %f, point %d repeat %d NO.%d" \
                    % ( name, max_A, target_list[max_i][0], measure_list_mm[max_i][max_j][max_k][0], max_i + 1, max_j + 1, max_k + 1 ))
            name = "Max " + print_accuracy[0] + " Accuracy_y: "
    return boundary_max_accuracy, center_max_accuracy

def analysis_point_linearity(target_list, measure_list_mm, boundary_index_list, linearity_list):

    """
    analysis max boundary/center error
    """

    boundary_max_linearity, center_max_linearity = analysis_point_max_linearity(boundary_index_list, linearity_list)
    print("\tLinearity:")
    print_linearity_list = [["boundary", boundary_max_linearity], ["center  ", center_max_linearity]]
    for print_linearity in print_linearity_list:
        name = print_linearity[0]
        max_L = print_linearity[1][0]
        max_i = print_linearity[1][1][0]
        max_j = print_linearity[1][1][1]
        max_k = print_linearity[1][1][2]
        print("\t\tMax %s Linearity: %f ---------------- target: (%f, %f), measure: (%f, %f), point %d repeat %d NO.%d" \
                % ( name, max_L, target_list[max_i][0], target_list[max_i][1], \
                measure_list_mm[max_i][max_j][max_k][0], measure_list_mm[max_i][max_j][max_k][1], max_i + 1, max_j + 1, max_k + 1 ))
    return boundary_max_linearity, center_max_linearity

def analysis_point_precision(target_list, measure_list_mm, boundary_index_list, precision_list):

    """
    analysis max boundary/center error
    """

    boundary_max_precision, center_max_precision = analysis_point_max_precision(boundary_index_list, precision_list)
    print("\tPrecision:")
    print_precision_list = [["boundary", boundary_max_precision], ["center  ", center_max_precision]]
    for print_precision in print_precision_list:
        name = "Max " + print_precision[0] + " Precision_x: "
        for xy in range(2):
            max_P = print_precision[1][xy][0]
            max_i = print_precision[1][xy][1]
            print("\t\t%s%f ---------------- target: (%f, %f), point %d" \
                    % ( name, max_P, target_list[max_i][0], target_list[max_i][1], max_i + 1 ))
            name = "Max " + print_precision[0] + " Precision_y: "
    return boundary_max_precision, center_max_precision

def analysis_line_linearity(target_list, measure_list_mm, boundary_index_list, linearity_list):

    """
    analysis line boundary/center linearity
    """

    boundary_max_linearity = [0, [0, 0]]
    center_max_linearity = [0, [0, 0]]
    for i in range(len(linearity_list)):
        for j in range(len(linearity_list[i])):
            if j in boundary_index_list[i]:
                if linearity_list[i][j] > boundary_max_linearity[0]:
                    boundary_max_linearity[0] = linearity_list[i][j]
                    boundary_max_linearity[1] = [i, j]
            else:
                if linearity_list[i][j] > center_max_linearity[0]:
                    center_max_linearity[0] = linearity_list[i][j]
                    center_max_linearity[1] = [i, j]
    print("\tLinearity:")
    print_linearity_list = [["boundary", boundary_max_linearity], ["center  ", center_max_linearity]]
    for print_linearity in print_linearity_list:
        name = print_linearity[0]
        max_L = print_linearity[1][0]
        max_i = print_linearity[1][1][0]
        max_j = print_linearity[1][1][1]
        print("\t\tMax %s linearity %f -------------- target: (%f %f)->(%f, %f), measure: (%f, %f), line %d" \
                % ( name, max_L, target_list[max_i][0], target_list[max_i][1], target_list[max_i][2], target_list[max_i][3], \
                measure_list_mm[max_i][max_j][0], measure_list_mm[max_i][max_j][1], max_i + 1 ))
    return boundary_max_linearity, center_max_linearity

def save_point_analysis_to_excel(target_list, measure_list_mm, measure_list_pixel, boundary_index_list, accuracy_list, linearity_list, precision_list, excel_fd):

    """
    save analysis output to 'analysis_output' sheet
    """

    point_analysis_dict = {}
    header_key_list = ["Test type", "Target point(mm)", "Measure point(mm)", "Measure pixel(pixel)", "Accuracy X", "Accuracy Y", "Linearity", "Precision X", "Precision Y"]
    header_val_list = [[] for i in range(len(header_key_list))]

    test_type_index = header_key_list.index("Test type")
    target_index = header_key_list.index("Target point(mm)")
    measure_point_index = header_key_list.index("Measure point(mm)")
    measure_pixel_index = header_key_list.index("Measure pixel(pixel)")
    accuracy_x_index = header_key_list.index("Accuracy X")
    accuracy_y_index = header_key_list.index("Accuracy Y")
    linearity_index = header_key_list.index("Linearity")
    precision_x_index = header_key_list.index("Precision X")
    precision_y_index = header_key_list.index("Precision Y")

    for i in range(len(header_key_list)):
        if i == test_type_index:
            header_val_list[i].append("Point test")
        else:
            header_val_list[i].append("")

    for i in range(len(measure_list_mm)):
        for j in range(len(header_key_list)):
            header_val_list[j].append("")
            if j == test_type_index:
                if i in boundary_index_list:
                    point_type = "boundary point"
                else:
                    point_type = "center point"
                header_val_list[j].append("Point " + str(i + 1) + " (" + point_type + ")")
            elif j == precision_x_index:
                precision_x = round(precision_list[i][0], 3)
                header_val_list[precision_x_index].append(str(precision_x))
            elif j == precision_y_index:
                precision_y = round(precision_list[i][1], 3)
                header_val_list[precision_y_index].append(str(precision_y))
            else:
                header_val_list[j].append("")
        target_x = round(target_list[i][0], 3)
        target_y = round(target_list[i][1], 3)
        for j in range(len(measure_list_mm[i])):
            for k in range(len(header_key_list)):
                if k == test_type_index:
                    header_val_list[k].append("        Repeat " + str(j + 1))
                else:
                    header_val_list[k].append("")
            for k in range(len(measure_list_mm[i][j])):
                header_val_list[test_type_index].append("")
                header_val_list[target_index].append("(" + str(target_x) + ", " + str(target_y) + ")")
                measure_x = round(measure_list_mm[i][j][k][0], 3)
                measure_y = round(measure_list_mm[i][j][k][1], 3)
                header_val_list[measure_point_index].append("(" + str(measure_x) + ", " + str(measure_y) + ")")
                measure_x_pixel = round(measure_list_pixel[i][j][k][0], 3)
                measure_y_pixel = round(measure_list_pixel[i][j][k][1], 3)
                header_val_list[measure_pixel_index].append("(" + str(measure_x_pixel) + ", " + str(measure_y_pixel) + ")")
                accuracy_x = round(accuracy_list[i][j][k][0], 3)
                header_val_list[accuracy_x_index].append(str(accuracy_x))
                accuracy_y = round(accuracy_list[i][j][k][1], 3)
                header_val_list[accuracy_y_index].append(str(accuracy_y))
                linearity = round(linearity_list[i][j][k], 3)
                header_val_list[linearity_index].append(str(linearity))
                header_val_list[precision_x_index].append("")
                header_val_list[precision_y_index].append("")

    for i in range(len(header_key_list)):
        point_analysis_dict[header_key_list[i]] = header_val_list[i]
    excel_fd.write_excel(point_analysis_dict)

def save_line_analysis_to_excel(target_list, measure_list_mm, measure_list_pixel, boundary_index_list, linearity_list, excel_fd):

    """
    save analysis output to 'analysis_output' sheet
    """

    line_analysis_dict = {}
    header_key_list = ["Test type", "Target line(mm)", "Measure point(mm)", "Measure pixel(pixel)", "Linearity", "Boundary/Center"]
    header_val_list = [[] for i in range(len(header_key_list))]

    test_type_index = header_key_list.index("Test type")
    target_index = header_key_list.index("Target line(mm)")
    measure_point_index = header_key_list.index("Measure point(mm)")
    measure_pixel_index = header_key_list.index("Measure pixel(pixel)")
    linearity_index = header_key_list.index("Linearity")
    boundary_center_index = header_key_list.index("Boundary/Center")

    for i in range(len(header_key_list)):
        if i == test_type_index:
            header_val_list[i].append("Line test")
        else:
            header_val_list[i].append("")

    for i in range(len(measure_list_mm)):
        for j in range(len(header_key_list)):
            header_val_list[j].append("")
            if j == test_type_index:
                header_val_list[j].append("Line " + str(i + 1))
            else:
                header_val_list[j].append("")
        start_x = round(target_list[i][0], 3)
        start_y = round(target_list[i][1], 3)
        end_x = round(target_list[i][2], 3)
        end_y = round(target_list[i][3], 3)
        for j in range(len(measure_list_mm[i])):
            header_val_list[test_type_index].append("")
            header_val_list[target_index].append("(" + str(start_x) + ", " + str(start_y) + ") ---> " + "(" + str(end_x) + ", " + str(end_y) + ")")
            measure_x = round(measure_list_mm[i][j][0], 3)
            measure_y = round(measure_list_mm[i][j][1], 3)
            header_val_list[measure_point_index].append("(" + str(measure_x) + ", " + str(measure_y) + ")")
            measure_x_pixel = round(measure_list_pixel[i][j][0], 3)
            measure_y_pixel = round(measure_list_pixel[i][j][1], 3)
            header_val_list[measure_pixel_index].append("(" + str(measure_x_pixel) + ", " + str(measure_y_pixel) + ")")
            linearity = round(linearity_list[i][j], 3)
            header_val_list[linearity_index].append(str(linearity))
            if j in boundary_index_list[i]:
                header_val_list[boundary_center_index].append("boundary")
            else:
                header_val_list[boundary_center_index].append("center")

    for i in range(len(header_key_list)):
        line_analysis_dict[header_key_list[i]] = header_val_list[i]
    excel_fd.write_excel(line_analysis_dict)

def analysis_data(filename, report_time_list, test_type, boundary_index_list, target_list, measure_list_mm, measure_list_pixel, excel_fd):

    """
    analysis data based on data type, target and measure list
    """

    len1 = len(target_list)
    len2 = len(measure_list_mm)
    if len1 == 0 or len2 ==0 or len1 != len2:
        print(len1, len2)
        print("Error when loading target/mearsure data")
        exit(0)

    if test_type == "point test":
        print("\n\nPoint test data analysis:")
        point_fd = point_analysis(target_list, measure_list_mm)
        accuracy_list = point_fd.cal_accuracy()
        boundary_max_accuracy, center_max_accuracy = analysis_point_accurcay(target_list, measure_list_mm, boundary_index_list, accuracy_list)
        linearity_list = point_fd.cal_linearity()
        boundary_max_linearity, center_max_linearity = analysis_point_linearity(target_list, measure_list_mm, boundary_index_list, linearity_list)
        precision_list = point_fd.cal_precision()
        boundary_max_precision, center_max_precision = analysis_point_precision(target_list, measure_list_mm, boundary_index_list, precision_list)

        save_point_analysis_to_excel(target_list, measure_list_mm, measure_list_pixel, boundary_index_list, accuracy_list, linearity_list, precision_list, excel_fd)

        xlsx_data_list = [boundary_index_list, target_list, measure_list_mm, accuracy_list, linearity_list, precision_list, \
                boundary_max_linearity[0], center_max_linearity[0], boundary_max_precision, center_max_precision]
        fill_point_test_result_data_sheet(filename, xlsx_data_list)

    elif test_type == "line test":
        print("\n\nLine test data analysis:")
        linearity_list = line_analysis(target_list, measure_list_mm).cal_linearity()
        boundary_max_linearity, center_max_linearity = analysis_line_linearity(target_list, measure_list_mm, boundary_index_list, linearity_list)

        save_line_analysis_to_excel(target_list, measure_list_mm, measure_list_pixel, boundary_index_list, linearity_list, excel_fd)

        # xlsx_data: boundary_index_list, target_list, measure_list, linearity_list, max_edge, max_center
        xlsx_data_list = [boundary_index_list, target_list, measure_list_mm, linearity_list, boundary_max_linearity[0], center_max_linearity[0]]
        fill_line_test_result_data_sheet(filename, report_time_list, xlsx_data_list)
    else:
        print("Unsupport excel data")
        exit(0)
