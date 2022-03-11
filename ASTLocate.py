#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 3/5/22 10:27 AM
# @Author  : Jiyuan Wang
# @File    : ASTLocate.py

import sys
import clang.cindex
import hardcoded_channel_pattern
import rewrite


def _get_binop_operator(cursor, target_operator):
    """
    Returns the operator token of a binary operator cursor.

    :param cursor: A cursor of kind BINARY_OPERATOR.
    :return:       The token object containing the actual operator or None.
    """
    children = list(cursor.get_children())
    operator_min_begin = (children[0].location.line,
                          children[0].location.column)
    operator_max_end = (children[1].location.line,
                        children[1].location.column)

    for token in cursor.get_tokens():
        if (operator_min_begin < (token.extent.start.line,
                                  token.extent.start.column) and
                operator_max_end > (token.extent.end.line,
                                    token.extent.end.column) and (token.spelling == target_operator)):
            return token

    return None  # pragma: no cover


def traverse(node, target_operator):  # only for overflow

    target_variable_location = []

    # Recurse for children of this node
    for child in node.get_children():
        traverse(child, target_operator)

    # Add the node to function_declarations
    if node.kind == clang.cindex.CursorKind.FUNCTION_DECL:
        function_declarations.append(node)

    if node.kind == clang.cindex.CursorKind.RETURN_STMT:
        outside_kernel.append(node.location.line)  # place to add "channel read"

    if node.kind == clang.cindex.CursorKind.DECL_REF_EXPR:
        if node.spelling == "sum":  # should be the target variable, place to add kernel channel write. However,
            # seems AST compilation is impossible to get into kernel code
            target_variable_location.append(node.location.line)

    if node.spelling.find("Kernel start") != -1:
        kernel_start.append(node.location.line)

    # Print out information about the node
    if node.kind in [clang.cindex.CursorKind.BINARY_OPERATOR]:
        if _get_binop_operator(node, target_operator) is not None:
            print('Found %s' % _get_binop_operator(node, target_operator).spelling)
            if node.location.line in target_variable_location:
                inside_kernel_assert_location.append(node.location.line)

    print('Found %s  type=%s [line=%s, col=%s]' % (
        node.spelling, node.kind, node.location.line, node.location.column))


if __name__ == '__main__':
    # Find out the c++ parser
    function_calls = []  # List of AST node objects that are function calls
    function_declarations = []  # List of AST node objects that are function declarations
    outside_kernel = []
    inside_kernel_assert_location = []
    kernel_start = []

    # Traverse the AST tree

    # Tell clang.cindex where libclang.dylib is
    clang.cindex.Config.set_library_path(
        "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/")
    index = clang.cindex.Index.create()
    original_code_path = "example_program/overflow1.cpp"
    # Generate AST from filepath passed in the command line
    tu = index.parse(original_code_path)

    root = tu.cursor  # Get the root of the AST
    traverse(root, "+")

    # Print the contents of function_calls and function_declarations
    print(outside_kernel)
    print(inside_kernel_assert_location)
    if len(inside_kernel_assert_location) == 0:
        f = open(original_code_path, "r")
        for i, line in enumerate(f):
            if line.find("+") != -1 and line.find("sum[") != -1:
                print(line)
                inside_kernel_assert_location.append(i)

    line_number_queue = [0, kernel_start[0], kernel_start[0] + 2, inside_kernel_assert_location[0], outside_kernel[0]]
    print(inside_kernel_assert_location[0])
    trial = hardcoded_channel_pattern.OverflowPattern("sum")

    rewrite.rewrite(line_number_queue, "example_program/overflow1.cpp", "example_program/overflow11.cpp", trial)

#kernel_start[0] + 2 should be q.submit
