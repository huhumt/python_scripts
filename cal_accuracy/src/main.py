#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os_proc import remove_directory, create_directory, get_basename
from read_write_excel import read_write_excel
from analysis_data import analysis_data
from find_pattern import find_pattern
from read_img_from_excel_MIK import read_img_from_excel_MIK

def check_duplicate_element(input_list):

    """
    check whether exist duplicate element in an array
    """

    filename_list = []
    for element in input_list:
        filename_list.append(element.split("\\")[-1])

    for i in range(len(filename_list)):
        if filename_list.count(filename_list[i]) > 1:
            print(input_list[i], "is duplicated")

def find_independent_csv(csv_list, xlsx_list):

    """
    some csv files are independent report
    while some others are part of xlsx files
    """

    xlsx_basename_list = []
    for xlsx_file in xlsx_list:
        xlsx_basename_list.append(get_basename(xlsx_file).replace(".xlsx", ""))

    csv_independent_list = []
    for csv_file in csv_list:
        csv_basename = get_basename(csv_file).replace(".csv", "")
        if csv_basename not in xlsx_basename_list:
            csv_independent_list.append(csv_file)

    return csv_independent_list

def main():

    """
    Main entry for the whole project
    """

    xlsx_list = find_pattern("*.xlsx", "./data/")
    check_duplicate_element(xlsx_list)
    csv_list = find_independent_csv(find_pattern("*.csv", "./data/"), xlsx_list)
    xlsx_list += csv_list

    for xlsx in xlsx_list:
        rw_excel = read_write_excel(xlsx)
        print("filename: %s, %s data type" % (xlsx, rw_excel.read_data_type()))
        try:
            config_list = rw_excel.read_config()
            target_list, measure_list_mm, measure_list_pixel = rw_excel.read_target_and_measure()
            linearity_list = rw_excel.read_linearity_error()
            ret = analysis_data(config_list, target_list, measure_list_mm, linearity_list)
        except:
            pass
        print("\n\n\n")

        # if ret < 0:
        #     remove_directory(xlsx, "./haha")

    remove_directory("./image/generate_img")
    create_directory("./image/generate_img")

    for xlsx in xlsx_list:
        try:
            read_img_from_excel_MIK(xlsx, "./image/generate_img/")
        except:
            pass

if __name__ == "__main__":

    """
    Run project here
    """

    main()
