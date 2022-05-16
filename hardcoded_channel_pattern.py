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
                                                                                        "      std::cout<<\"start reading....\";\n" \
                                                                                        "      flag[i] = " + self.channel_name + "::read();\n" \
                                                                                                                                 "      std::cout<<flag[i]<<\" find a violation!\";\n" \
                                                                                                                                 "      std::cout<<\"read success.\";\n" \
                                                                                                                                 "      if (flag[i]==-1){break;}\n" \
                                                                                                                                 "      interested = 1;\n" \
                                                                                                                                 "}\n" \
                                                                                                                                 "  std::cout<<\"finish reading...\";\n"
        self.outside_channel_size_code = "buffer channel_buf(channel_num.data(), num_channel);\n"  # num_channel undone
        self.inside_kernel_channel_size_code = "accessor channel_sum(channel_buf, h, write_only, 0);\n"

    def kernel_channel_code(self) -> str:
        return self.kernel_code

    def outside_channel_def(self) -> str:
        return self.outside_code_def

    def outside_channel_read(self) -> str:
        return self.outside_code_read

    def outside_channel_size(self) -> str:
        return self.outside_channel_size_code

    def accessor_channel(self) -> str:
        return self.inside_kernel_channel_size_code


# TODO UNTESTED
class OverflowPattern(ChannelsCodePattern):

    def __init__(self, variable: [], ensure=None, requirement=None):
        global requirements
        if requirement is None:
            requirement = []
        else:
            requirements = ""
            for require in requirement:
                requirements = requirements + require + " and "
                print(requirements)
            if requirements != "":
                requirements = "not(" + requirements[:-6] + ") or "
            print(requirements)
            for ensures in ensure:
                requirements = requirements + ensures

        channel_name = "MyDeviceToHostSideChannel_Overflow"
        super(OverflowPattern, self).__init__(channel_name)
        self.kernel_code = "if (((" + variable[1] + ">0)and(" + variable[2] + ">0)and(" + variable[0] + "<0)) or " \
                                                                                                        "((" + variable[
                               1] + "<0)and(" + variable[2] + "<0)and(" + variable[0] + ">0))) " \
                                                                                        "{\n" \
                                                                                        "   bool flag=true;\n " \
                                                                                        "   " + self.channel_name + "::write(i,flag);\n " \
                                                                                                                    "    channel_sum[0] = channel_sum[0] + 1;\n" \
                                                                                                                    "} \n"
        # self.kernel_code = "if (not(" + requirements + ")){\n " \ "   bool flag=true;\n " \ "   " +
        # self.channel_name + "::write(i,flag);\n " \ "    channel_sum[0] = channel_sum[0] + 1;\n" \ "} \n"


class ValueRangePattern(ChannelsCodePattern):

    def __init__(self, variable: [], ensure=None, requirement=None):
        global requirements
        if requirement is None:
            requirement = []
        else:
            requirements = ""
            for require in requirement:
                requirements = requirements + require + " and "
                print(requirements)
            if requirements != "":
                requirements = "not(" + requirements[:-6] + ") or "
            print(requirements)
            for ensures in ensure:
                requirements = requirements + ensures

        channel_name = "MyDeviceToHostSideChannel_ValueRange"
        super(ValueRangePattern, self).__init__(channel_name)
        self.kernel_code = "if (not(" + requirements + ")){\n " \
                                                       "   bool flag=true;\n " \
                                                       "   " + self.channel_name + "::write(i,flag);\n " \
                                                                                   "    channel_sum[0] = channel_sum[0] + 1;\n" \
                                                                                   "} \n"


class ArrayOutOfSizePattern(ChannelsCodePattern):

    def __init__(self, variable: str, ensure=None, requirement=None):
        global requirements
        print(requirement)
        if requirement is None:
            requirement = []
        else:
            requirements = ""
            for requirement in requirement:
                requirements = requirements + requirement + " and "
            if requirements != "":
                requirements = "not(" + requirements[:-6] + ") or "
            for ensures in ensure:
                requirements = requirements + ensures

        channel_name = "MyDeviceToHostSideChannel_Array"
        super(ArrayOutOfSizePattern, self).__init__(channel_name, item=2)
        self.kernel_code = "if (not(" + requirements + ")) {\n " \
                                                       "   bool flag=true;\n " \
                                                       "   " + self.channel_name + "::write(i," \
                                                                                   "flag);\n " \
                                                                                   "    channel_sum[1] = channel_sum[1] + 1;\n" \
                                                                                   "} \n"


class ChannelSizePattern(ChannelsCodePattern):

    def __init__(self, target_channel: str):
        channel_name = "MyDeviceToHostSideChannel_Channel"
        super(ChannelSizePattern, self).__init__(channel_name, item=3)
        self.kernel_code = "bool flag_channel=true;\n" + target_channel + "::write(5,flag_channel);\n if (" \
                                                                          "!flag_channel) {bool flag=true;\n " \
                                                                          "   " + self.channel_name + "::write(i,flag);\n " \
                                                                                                      "    channel_sum[2] = channel_sum[2] + 1;\n" \
                                                                                                      "} \n"


class HangPattern(ChannelsCodePattern):

    def __init__(self, stack_list: []):
        channel_name = "MyDeviceToHostSideChannel_Hang"  # only check the channel hang
        super(HangPattern, self).__init__(channel_name, item=4)
        stack_list_str = ""
        for stack_call in stack_list:
            stack_list_str = stack_list_str + self.channel_name + "::write("+str(stack_call)+",flag);\n "

        self.kernel_code = "  timeout_counter = 0; \n" \
                           "  while (timeout_counter <= kTimeoutCounterMax) { \n" \
                           "    bool valid_read;\n" \
                           "    auto val = IOPipeIn::read(valid_read);\n" \
                           "    if (valid_read) {\n" \
                           "        timeout_counter = 0;\n" \
                           "        if (val == match_num) {\n" \
                           "            DeviceToHostSideChannel::write(val);\n" \
                           "    }\n" \
                           "    IOPipeOut::write(val);\n" \
                           "    } else {\n" \
                           "        timeout_counter++;\n" \
                           "    }\n" \
                           "  }\n" \
                           "  if (timeout_counter>=kTimeoutCounterMax){\n" \
                           "    bool flag=true;\n " \
                           "    " + self.channel_name + "::write(i,flag);\n " \
                           "    " + stack_list_str +\
                           "    " + self.channel_name + "::write(timeout_counter,flag);\n " \
                                                        "    channel_sum[3] = channel_sum[3] + 1;\n" \
                                                        "  } \n"

