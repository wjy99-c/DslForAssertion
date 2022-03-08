#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 3/7/22 5:22 PM
# @Author  : Jiyuan Wang
# @File    : hardcoded_channel_pattern.py

class ChannelsCodePattern:
    kernel_code = ""
    outside_code_read = ""

    def __init__(self, channel_name: str):
        self.outside_code_def = "struct DeviceToHostSideChannelID;\n"
        self.channel_name = channel_name
        self.outside_code_def = self.outside_code_def + "using " + self.channel_name + "= DeviceToHostSideChannel" \
                                                                                       "<DeviceToHostSideChannelID," \
                                                                                       " int, true, 8>;\n "
        self.outside_code_read = "  for (int i = 0; i < channel_sum[0]; i++) {\n " \
                                 "      interested = 1;\n" \
                                 "      std::cout<<\"start reading....\";\n" \
                                 "      flag[i] = " + self.channel_name + "::read();\n" \
                                                                          "      std::cout<<flag[i]<<\" find an overflow!\";\n" \
                                                                          "      std::cout<<\"read success.\";\n" \
                                                                          "      if (flag[i]==-1){break;}\n" \
                                                                          "}\n" \
                                                                          "  std::cout<<\"finish reading...\";\n"

    def kernel_channel_ef(self) -> str:
        return self.kernel_code

    def outside_channel_def(self) -> str:
        return self.outside_code_def

    def outside_channel_read(self) -> str:
        return self.outside_code_def


# TODO UNTESTED
class OverflowPattern(ChannelsCodePattern):

    def __init__(self, variable: str):
        channel_name = "MyDeviceToHostSideChannel_Overflow"
        super(OverflowPattern, self).__init__(channel_name)
        self.kernel_code = "if (" + variable + "[i]<0){\n " \
                                               "   bool flag=true;\n " \
                                               "   " + self.channel_name + "::write(i,flag);\n " \
                                                                           "    channel_sum[0] = channel_sum[0] + 1\n" \
                                                                           "} \n"


# TODO UNDONE
class ArrayOutOfSizePattern(ChannelsCodePattern):

    def __init__(self):
        channel_name = "MyDeviceToHostSideChannel_Array"
        super(ArrayOutOfSizePattern, self).__init__(channel_name)


# TODO UNDONE
class HangPattern(ChannelsCodePattern):

    def __init__(self):
        channel_name = "MyDeviceToHostSideChannel_Hang"
        super(HangPattern, self).__init__(channel_name)
