#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 3/7/22 5:22 PM
# @Author  : Jiyuan Wang
# @File    : hardcoded_channel_pattern.py

class ChannelsCodePattern:
    kernel_code = ""

    def __init__(self, channel_name: str, item=1):
        self.outside_code_def = "struct DeviceToHostSideChannelID;\n"
        self.channel_name = channel_name
        self.outside_code_def = self.outside_code_def + "using " + self.channel_name + "= DeviceToHostSideChannel" \
                                                                                       "<DeviceToHostSideChannelID," \
                                                                                       " int, true, 8>;\n "
        self.outside_code_read = "  for (int i = 0; i < channel_num[" + str(item - 1) + "]; i++) {\n " \
                                 "      interested = 1;\n" \
                                 "      std::cout<<\"start reading....\";\n" \
                                 "      flag[i] = " + self.channel_name + "::read();\n" \
                                 "      std::cout<<flag[i]<<\" find an overflow!\";\n" \
                                 "      std::cout<<\"read success.\";\n" \
                                 "      if (flag[i]==-1){break;}\n" \
                                 "}\n" \
                                 "  std::cout<<\"finish reading...\";\n"
        self.outside_channel_size_code = "buffer channel_buf(channel_num.data(), num_channel);\n"  # num_channel undone
        self.inside_kernel_channel_size_code = "accessor channel_sum(channel_buf, h, write_only, 0)\n"

    def kernel_channel_code(self) -> str:
        return self.kernel_code

    def outside_channel_def(self) -> str:
        return self.outside_code_def

    def outside_channel_read(self) -> str:
        return self.outside_code_read

    def outside_channel_size_code(self) -> str:
        return self.outside_channel_size_code

    def inside_channel_size_code(self) -> str:
        return self.inside_kernel_channel_size_code


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
