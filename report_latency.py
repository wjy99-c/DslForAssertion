#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/3/22 5:13 PM
# @Author  : Jiyuan Wang
# @File    : report_latency.py
import sys
import re


def id_different(s1, s2) -> bool:

    for cont in s1:
        if re.search('id":', cont) is not None:
            id1 =re.search(r"\d+\.?\d*", cont)
    for cont in s2:
        if re.search('id":', cont) is not None:
            id2 = re.search(r"\d+\.?\d*", cont)
    if int(id1[0]) == int(id2[0]):
        return False
    else:
        return True


if __name__ == '__main__':
    max_latency = 0
    max_2latency = 0
    max_3latency = 0
    max_set = []
    max_2set = []
    max_3set = []
    with open("viewer_data.js", 'r') as f:
        for line in f:
            x = re.split('{"name', line)
            for event in x:
                y = re.split(",", event)
                for content in y:
                    if re.search('Latency":"', content) is not None:
                        number = re.search(r"\d+\.?\d*", content)
                        if int(number[0]) > max_latency:
                            max_latency = int(number[0])
                            max_set = y
                        elif (int(number[0]) > max_2latency) and (id_different(max_set, y)):
                            max_2latency = int(number[0])
                            max_2set = y
                        elif (int(number[0]) > max_3latency) and (id_different(max_2set, y)) and (id_different(max_set, y)):
                            max_3latency = int(number[0])
                            max_3set = y
    print(max_set)
    print(max_2set)
    print(max_3set)
