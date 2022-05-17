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


def return_keyword_str(s, key_word) -> int:
    val = []
    for conts in s:
        if re.search(key_word, conts) is not None:
            val = re.match(r"\":\"*\"", conts)  # should search from start
    return int(val[0])


if __name__ == '__main__':
    max_latency = 0
    max_set = []

    common_operator = []

    with open("../viewer_data.js", 'r') as f:
        for line in f:
            x = re.split('{"name', line)
            for event in x:
                y = re.split(",", event)
                operator_name = return_keyword_str(y, "name")

    print(max_set)
