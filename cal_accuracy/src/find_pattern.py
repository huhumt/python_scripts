#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, fnmatch

def find_pattern(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

if __name__ == "__main__":

    '''
    This is for test purpose
    '''

    find_pattern('*.txt', './')
