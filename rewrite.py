#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 3/8/22 6:08 PM
# @Author  : Jiyuan Wang
# @File    : rewrite.py
import hardcoded_channel_pattern


# Goal: invoke AST Locate, rewrite the entire oneAPI source file
def rewrite(line_number_queue, original_code_path: str, generated_code_path: str,
            generate_code_pattern: hardcoded_channel_pattern.ChannelsCodePattern):
    f = open(original_code_path, "r")
    wf = open(generated_code_path, "w")

    for i, line in enumerate(f):
        if i == line_number_queue[0]:
            wf.write(line)
            wf.write(generate_code_pattern.outside_code_def)
        elif i == line_number_queue[1]:
            wf.write(line)
            wf.write(generate_code_pattern.outside_channel_size_code())
        elif i == line_number_queue[2]:
            wf.write(line)
            wf.write(generate_code_pattern.inside_kernel_channel_size_code())
        elif i == line_number_queue[3]:
            wf.write(line)
            wf.write(generate_code_pattern.kernel_channel_code())
        elif i == line_number_queue[4]:
            wf.write(line)
            wf.write(generate_code_pattern.outside_channel_read())
        else:
            wf.write(line)
