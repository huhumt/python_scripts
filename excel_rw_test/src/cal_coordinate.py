#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import pi, sin, cos

class circle_coordinate:

    """
    This is a program to calculate coordinate
    on a circle given center point and radius
    """

    def __init__(self, par):

        '''
        par format:
            par[0]: x coordinate of circle center point
            par[1]: y coordinate of circle center point
            par[2]: circle radius
            par[3]: start angle of arc, based on polar coordinate system
            par[4]: end angle of the arc, range from 0~360 degree
            par[5]: how many points need to be inserted on the arc
        '''

        self.center_x = par[0]
        self.center_y = par[1]
        self.radius = par[2]
        self.start_angle = par[3]
        self.stop_angle = par[4]
        self.point_num = par[5]
        self.x_coordinate = []
        self.y_coordinate = []

    def cal_coordinate(self):

        '''
        calculate coordinate for each point on the arc
        '''

        # clear array to record newest points
        self.x_coordinate = []
        self.y_coordinate = []
        # step lenght
        delta_angle = (self.stop_angle - self.start_angle) / (self.point_num - 1)

        for i in range(self.point_num):
            # angle to radian
            cur_angle = (self.start_angle + i * delta_angle) * pi / 180
            self.x_coordinate.append(self.center_x + self.radius * cos(cur_angle))
            self.y_coordinate.append(self.center_y - self.radius * sin(cur_angle))

    def get_point(self, num):

        '''
        output points on the arc
        num: which point do you need, begin from 1 to point_num
             if num is bigger than total point or equal to 0,
             output all the points in an array
        '''

        self.cal_coordinate()
        if num > 0 and num <= self.point_num:
            return self.x_coordinate[num], self.y_coordinate[num]
        else:
            return self.x_coordinate, self.y_coordinate
