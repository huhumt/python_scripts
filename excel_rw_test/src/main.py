#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from get_boundary_list import get_boundary_list, get_notch_boundary_list
from concatenate_left_right_test import concatenate_left_right_test
from plot_figure import plot_figure, plot_figure_notch
from read_write_excel import read_write_excel
from analysis_data import analysis_data
import json

def get_config_target_measure_list(target_xlsx, max_x_config, max_y_config, boundary_range_config):

    """
    get config, target, measure list
    """

    rw_excel = read_write_excel(target_xlsx)
    # test_type, max_x, max_y, boundary_range, edge_error_threshold, center_error_threshold
    config_list = rw_excel.read_config()
    if config_list[1] == 0:
        config_list[1] = max_x_config
    if config_list[2] == 0:
        config_list[2] = max_y_config
    if config_list[3] == 0:
        config_list[3] = boundary_range_config

    target_list, measure_list_mm, measure_list_pixel = rw_excel.read_target_and_measure()

    return config_list, target_list, measure_list_mm, measure_list_pixel, rw_excel

def main():

    """
    Main entry for the whole project
    """

    fd = open('./config.json', 'r', encoding="utf-8")
    json_formatted_string = fd.read().replace('\\', '\\\\')
    fd.close()
    config_data = json.loads(json_formatted_string)

    max_x_config = config_data["Tp_parameter_config"]["max_x_in_mm"]
    max_y_config = config_data["Tp_parameter_config"]["max_y_in_mm"]
    boundary_range_config = config_data["Tp_parameter_config"]["boundary_range_in_mm"]
    notch_tp_enable = config_data["Notch_parameter_config"]["notch_tp_enable"]
    if notch_tp_enable == 1:
        top_left_circular = config_data["Notch_parameter_config"]["four_corner_circular"]["top_left_circular_in_mm"]
        top_right_circular = config_data["Notch_parameter_config"]["four_corner_circular"]["top_right_circular_in_mm"]
        bottom_left_circular = config_data["Notch_parameter_config"]["four_corner_circular"]["bottom_left_circular_in_mm"]
        bottom_right_circular = config_data["Notch_parameter_config"]["four_corner_circular"]["bottom_right_circular_in_mm"]

        rect_left_start_x = config_data["Notch_parameter_config"]["top_center_rectangle"]["left_start_x_in_mm"]
        rect_left_stop_x = config_data["Notch_parameter_config"]["top_center_rectangle"]["left_stop_x_in_mm"]
        rect_right_start_x = config_data["Notch_parameter_config"]["top_center_rectangle"]["right_start_x_in_mm"]
        rect_right_stop_x = config_data["Notch_parameter_config"]["top_center_rectangle"]["right_stop_x_in_mm"]
        rect_y_height = config_data["Notch_parameter_config"]["top_center_rectangle"]["y_height_in_mm"]

    left_right_concatenate_list = []
    for target_xlsx in config_data["Target_xlsx_full_path"]:
        if "left_right_concatenate" in target_xlsx:
            left_right_concatenate_list.append(target_xlsx)

    for target_xlsx in config_data["Target_xlsx_full_path"]:
        report_time = []
        if "left_right_concatenate" in target_xlsx:
            if target_xlsx in left_right_concatenate_list:
                config_left, target_left, measure_left_mm, measure_left_pixel, rw_excel_left = get_config_target_measure_list(left_right_concatenate_list[0], max_x_config, max_y_config, boundary_range_config)
                config_right, target_right, measure_right_mm, measure_right_pixel, rw_excel_right = get_config_target_measure_list(left_right_concatenate_list[1], max_x_config, max_y_config, boundary_range_config)
                config_list, target_list, measure_list_mm, measure_list_pixel = concatenate_left_right_test(config_left, target_left, measure_left_mm, measure_left_pixel, config_right, target_right, measure_right_mm, measure_right_pixel)
                left_report_time = read_write_excel(left_right_concatenate_list[0]).read_report_time()
                right_report_time = read_write_excel(left_right_concatenate_list[1]).read_report_time()
                for left_report in left_report_time:
                    report_time.append(left_report)
                for right_report in right_report_time:
                    report_time.append(right_report)
                target_xlsx = left_right_concatenate_list[1]
                print("\n\nContract '%s' with '%s' to do data analysis --- %d" % ( left_right_concatenate_list[0], left_right_concatenate_list[1], len(report_time) ))
                del left_right_concatenate_list[0 : 2]
                rw_excel_left.destroy()
                rw_excel = rw_excel_right
                # temporary code to do special test for WSQ on MIK
                config_list[1] += 0.8
            else:
                continue
        else:
            config_list, target_list, measure_list_mm, measure_list_pixel, rw_excel = get_config_target_measure_list(target_xlsx, max_x_config, max_y_config, boundary_range_config)

        # temporary code to do special test for WSQ on MIK
        if config_list[0] == "line test":
            for i in range(len(measure_list_pixel)):
                for j in range(len(measure_list_pixel[i])):
                    measure_list_mm[i][j][0] = measure_list_pixel[i][j][0] * config_list[1] / 1080.
                    measure_list_mm[i][j][1] = measure_list_pixel[i][j][1] * config_list[2] / 2280.
        elif config_list[0] == "point test":
            for i in range(len(measure_list_pixel)):
                for j in range(len(measure_list_pixel[i])):
                    for k in range(len(measure_list_pixel[i][j])):
                        measure_list_mm[i][j][k][0] = measure_list_pixel[i][j][k][0] * config_list[1] / 1080.
                        measure_list_mm[i][j][k][1] = measure_list_pixel[i][j][k][1] * config_list[2] / 2280.

        if notch_tp_enable:
            circular_list = [top_left_circular, top_right_circular, bottom_left_circular, bottom_right_circular]
            rect_list = [rect_left_start_x, rect_left_stop_x, rect_right_start_x, rect_right_stop_x, 0, rect_y_height]
            boundary_index_list = get_notch_boundary_list(config_list, circular_list, rect_list, target_list, measure_list_mm)
        else:
            boundary_index_list = get_boundary_list(config_list, target_list, measure_list_mm)
        analysis_data(target_xlsx, report_time, config_list[0], boundary_index_list, target_list, measure_list_mm, measure_list_pixel, rw_excel)
        print("More details please refer to 'analysis_output' sheet on excel file '%s'" % ( target_xlsx ))
        rw_excel.destroy()

        fig_filename = target_xlsx.replace(".xlsx", ".png")
        if notch_tp_enable:
            plot_figure_notch(circular_list, rect_list, config_list, target_list, measure_list_mm, fig_filename)
        else:
            plot_figure(config_list, target_list, measure_list_mm, fig_filename)

if __name__ == "__main__":

    """
    Run project here
    """

    main()
