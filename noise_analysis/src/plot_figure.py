#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np

def plot_figure(x_list, y1_list, y2_list=[]):

    """
    plot figure for target and measure
    """

    fig, ax = plt.subplots()
    plot1, = ax.plot(x_list, y1_list, 'g-', linewidth=0.8)
    if y2_list:
        plot2, = ax.plot(x_list, y2_list, 'g-', linewidth=0.8)
    plt.show()

def main():

    x_axis = np.linspace(0,20,20)
    y1_axis = [1058,1199,1207,1076,1237,
            1187,1228,1253,1229,1218,
            1221,1231,1248,1211,1239,
            1043,1186,1196,1065,1168]
    y2_axis = [1059,1201,1208,1076,1238,
            1187,1231,1255,1229,1219,
            1221,1232,1249,1212,1239,
            1043,1186,1196,1065,1168]
    plot_figure(x_axis, y1_axis, y2_axis)

if __name__ == "__main__":
    main()
