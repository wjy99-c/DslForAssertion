#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 3/5/22 9:40 AM
# @Author  : Jiyuan Wang
# @File    : input_config.py

class CompiledAssertionList:
    list = []
    variable_list = []
    position_list = []
    assert_type_list = []

    def __init__(self, input_file: str):
        dsl_f = open(input_file, "r")
        for assertion in dsl_f:
            items = assertion.split()
            self.list.append(items)
            self.variable_list.append(items[1])
            self.variable_list.append(items[2])
            self.assert_type_list.append(items[3])

    def pop(self) -> (str, str, str):
        self.list.pop()
        return self.variable_list.pop(), self.position_list.pop(), self.assert_type_list.pop()


if __name__ == '__main__':
    print("a")
