#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 3/5/22 10:27 AM
# @Author  : Jiyuan Wang
# @File    : rewrite.py

from pygccxml import utils
from pygccxml import declarations
from pygccxml import parser
import castxml
import sys
import clang.cindex


def rewrite(line_number_queue, original_code_path: str, generated_code_path: str, generate_kernel_code: str):
    f = open(original_code_path, "r")
    wf = open(generated_code_path, "w")

    for i, line in enumerate(f):
        if i == line_number_queue[0]:
            wf.write(line)
            wf.write(generate_kernel_code)
        else:
            wf.write(generate_kernel_code)

if __name__ == '__main__':
    # Find out the c++ parser
    function_calls = []  # List of AST node objects that are function calls
    function_declarations = []  # List of AST node objects that are fucntion declarations

    # Traverse the AST tree

    def traverse(node):

        # Recurse for children of this node
        for child in node.get_children():
            traverse(child)

        # Add the node to function_calls
        if node.kind == clang.cindex.CursorKind.CALL_EXPR:
            function_calls.append(node)

        # Add the node to function_declarations
        if node.kind == clang.cindex.CursorKind.FUNCTION_DECL:
            function_declarations.append(node)

        # Print out information about the node
        print('Found %s  type=%s [line=%s, col=%s]' % (
            node.displayname, node.kind, node.location.line, node.location.column))


    # Tell clang.cindex where libclang.dylib is
    clang.cindex.Config.set_library_path(
        "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/")
    index = clang.cindex.Index.create()

    # Generate AST from filepath passed in the command line
    tu = index.parse("example_program/test.cpp")

    root = tu.cursor  # Get the root of the AST
    traverse(root)

    # Print the contents of function_calls and function_declarations
    print(function_calls)
    print(function_declarations)
