#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class read_log:
    '''
    This class is used to read a txt file
    '''
    def __init__(self, name):
        self.name = name

    def read(self):

        fd = open(self.name, 'r')
        try:
            total_log_list = []
            cur_log_list = []
            output_pass_fail_flag = 0
            output_pass_fail_list = []
            active_size_list = []

            for line in fd:
                if output_pass_fail_flag > 0:
                    output_pass_fail_flag = 0
                    pass_fail_len = len(line.split(","))
                    if pass_fail_len not in output_pass_fail_list:
                        output_pass_fail_list.append(pass_fail_len)
                        print(pass_fail_len, output_pass_fail_list)

                if 'filename:' in line:
                    cur_log_list.append(line)
                    output_pass_fail_flag = 1
                elif 'Active size:' in line:
                    active_x = (line.split("mm, ")[0]).split()[-1]
                    active_y = (line.split()[-1]).split("mm")[0]
                    active_size_label = cur_log_list[0].split("\\")[1]
                    for active_size_element in active_size_list:
                        if active_size_label == active_size_element[0] and [active_x, active_y] != active_size_element[1]:
                            print(cur_log_list[0], active_size_element, active_size_label, active_x, active_y)
                    active_size_list.append([active_size_label, [active_x, active_y]])
                elif 'Center X:' and 'Center Y:' in line:
                    cur_log_list.append(float((line.split("Center X:")[-1]).split("mm")[0]))
                    cur_log_list.append(float((line.split("Center Y:")[-1]).split("mm")[0]))
                elif 'Edge   X:' and 'Edge   Y:' in line:
                    cur_log_list.append(float((line.split("Edge   X:")[-1]).split("mm")[0]))
                    cur_log_list.append(float((line.split("Edge   Y:")[-1]).split("mm")[0]))
                elif '----------------------' in line and 'TEST' in line:
                    if cur_log_list:
                        for history_log in total_log_list:
                            if cur_log_list[1:] == history_log[1:]:
                                print(cur_log_list[0], history_log[0], "\t\t------------- is duplicated ", cur_log_list[1:], "\n\n")
                        total_log_list.append(cur_log_list)
                        cur_log_list = []
        finally:
            fd.close()

        return total_log_list

def print_error_info(cur_output, cur_mode, cur_log):
    """
    print apl, jitter, linearity info
    """

    item_order_list = ['apl', 'jitter', 'linearity']

    if "repeatability" in cur_output and cur_log[3] == item_order_list[0]:
        if "X" in cur_output:
            print("\t\t%10s: Edge %.3fmm, Center %.3fmm" % (cur_mode, cur_log[-1][-2], cur_log[-1][-4]))
        elif "Y" in cur_output:
            print("\t\t%10s: Edge %.3fmm, Center %.3fmm" % (cur_mode, cur_log[-1][-1], cur_log[-1][-3]))
    elif "accuracy" in cur_output and cur_log[3] == item_order_list[0]:
        if "X" in cur_output:
            print("\t\t%10s: Edge %.3fmm, Center %.3fmm" % (cur_mode, cur_log[-1][2], cur_log[-1][0]))
        elif "Y" in cur_output:
            print("\t\t%10s: Edge %.3fmm, Center %.3fmm" % (cur_mode, cur_log[-1][3], cur_log[-1][1]))
    elif "jitter" in cur_output and cur_log[3] == item_order_list[1]:
        if "X" in cur_output:
            print("\t\t%10s: Edge %.3fmm, Center %.3fmm" % (cur_mode, cur_log[-1][-2], cur_log[-1][-4]))
        elif "Y" in cur_output:
            print("\t\t%10s: Edge %.3fmm, Center %.3fmm" % (cur_mode, cur_log[-1][-1], cur_log[-1][-3]))
    elif "linearity" in cur_output and cur_log[3] == item_order_list[2]:
        if "X" in cur_output:
            print("\t\t%10s: Edge %.3fmm, Center %.3fmm" % (cur_mode, cur_log[-1][2], cur_log[-1][0]))
        elif "Y" in cur_output:
            print("\t\t%10s: Edge %.3fmm, Center %.3fmm" % (cur_mode, cur_log[-1][3], cur_log[-1][1]))

if __name__ == "__main__":

    """
    function entery
    """

    log_list = read_log("./test.log").read()

    mode_order_list = ['charging', 'floating', 'white', 'black', 'hbm', 'w_b_blink']
    name_order_list = []
    print_log_list = []

    for log_element in log_list:
        test_item = log_element[0].split("\\")[-2] # apl, jitter, linearity
        test_mode = log_element[0].split("\\")[-3] # white, black, hbm, w_b_blink, to_ground, floating
        test_name = log_element[0].split("\\")[-4] # G1_#25, G4_#17

        print_log_list.append([0, test_name, test_mode, test_item, log_element[1:]])

        if test_name not in name_order_list:
            name_order_list.append(test_name)

    output_log_list = ['X-repeatability', 'Y-repeatability',
            'X-axis accuracy', 'Y-axis accuracy',
            'X-axis jitter', 'Y-axis jitter',
            'X-axis linearity', 'Y-axis linearity']

    print("\n\n\n------------ generate print info ------------\n")
    for cur_name in name_order_list:
        print(cur_name)
        for cur_output in output_log_list:
            print("\t", cur_output)
            for cur_mode in mode_order_list:
                for cur_log in print_log_list:
                    if cur_name == cur_log[1] and cur_mode == cur_log[2]:
                        print_error_info(cur_output, cur_mode, cur_log)
            print("\n\n")
        print("\n\n\n")
    print("\n\n\n------ end of generate print info -----------\n")
