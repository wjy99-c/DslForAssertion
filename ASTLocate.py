#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 3/5/22 10:27 AM
# @Author  : Jiyuan Wang
# @File    : ASTLocate.py

import sys
import clang.cindex
import hardcoded_channel_pattern


# TODO UNDONE
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

    # Recurse for children of this node
    for child in node.get_children():
        traverse(child, target_operator)

    # Add the node to function_calls
    if node.kind == clang.cindex.CursorKind.CALL_EXPR:
        function_calls.append(node)

    # Add the node to function_declarations
    if node.kind == clang.cindex.CursorKind.FUNCTION_DECL:
        function_declarations.append(node)

    # Print out information about the node
    if node.kind in [clang.cindex.CursorKind.BINARY_OPERATOR]:
        if _get_binop_operator(node, target_operator) is not None:
            print('Found %s' % _get_binop_operator(node, target_operator).spelling)

    print('Found %s  type=%s [line=%s, col=%s]' % (
        node.spelling, node.kind, node.location.line, node.location.column))


if __name__ == '__main__':
    # Find out the c++ parser
    function_calls = []  # List of AST node objects that are function calls
    function_declarations = []  # List of AST node objects that are function declarations

    # Traverse the AST tree

    # Tell clang.cindex where libclang.dylib is
    clang.cindex.Config.set_library_path(
        "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/")
    index = clang.cindex.Index.create()

    # Generate AST from filepath passed in the command line
    tu = index.parse("example_program/overflow.cpp")

    root = tu.cursor  # Get the root of the AST
    traverse(root, "+")

    # Print the contents of function_calls and function_declarations
    print(function_calls)
    print(function_declarations)
