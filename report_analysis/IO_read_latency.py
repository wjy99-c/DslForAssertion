#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/15/22 4:50 PM
# @Author  : Jiyuan Wang
# @File    : IO_read_latency.py
import sys
import re


def id_different(s1, s2) -> bool:
    for cont in s1:
        if re.search('id":', cont) is not None:
            id1 = re.search(r"\d+\.?\d*", cont)
    for cont in s2:
        if re.search('id":', cont) is not None:
            id2 = re.search(r"\d+\.?\d*", cont)
    if int(id1[0]) == int(id2[0]):
        return False
    else:
        return True


def return_keyword_number(s, key_word) -> int:
    val = []
    for conts in s:
        if re.search(key_word, conts) is not None:
            val = re.search(r"\d+\.?\d*", conts)
    return int(val[0])


if __name__ == '__main__':
    thre_latency = 100

    candidate_set = []

    with open("viewer_data.js", 'r') as f:
        for line in f:
            x = re.split('{"name', line)
            for event in x:
                if re.search("Pipe", event) is None:  # check for the key word
                    continue
                y = re.split(",", event)
                number = return_keyword_number(y, 'Latency":"')
                if number > thre_latency:
                    candidate_set.append(return_keyword_number(y, '"line":'))

