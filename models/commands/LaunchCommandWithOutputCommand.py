#!/usr/bin/env python3
"""
BSD 3-Clause License

Copyright (c) 2017, SafeBreach Labs
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


Concrete implementation of the LaunchCommandWithOutput command
Author:     Dor Azouri <dor.azouri@safebreach.com>
Date:       2018-02-04 08:03:08
"""

import common.utils as utils
from .SirepCommand import SirepCommand
from common.constants import TRUE_FLAG_STRINGS, INT_SIZE
from common.enums.CommandType import CommandType


class LaunchCommandWithOutputCommand(SirepCommand):
    """Concrete implementation of the LaunchCommandWithOutput command"""

    HEADER_SIZE = 4 * INT_SIZE
    IMPERSONATE_LOGGED_ON_USER_PREFIX = "<AS_LOGGED_ON_USER>"

    def __init__(self,
                 return_output_flag,
                 command_line_string,
                 as_logged_on_user=False,
                 parameters_string="",
                 base_directory_path=""):
        """Described in parent class"""
        super(LaunchCommandWithOutputCommand, self).__init__(
            CommandType.LaunchCommandWithOutput)
        self.return_error_flag = 1  # always return error stream
        self.return_output_flag = int(return_output_flag)
        self.command_line_string = command_line_string
        self.parameters_string = utils.moustache_to_env_var(parameters_string)
        self.base_directory_path = base_directory_path
        self.as_logged_on_user = True if str(as_logged_on_user).lower() in TRUE_FLAG_STRINGS else False
        if self.as_logged_on_user:
            self.command_line_string = \
                LaunchCommandWithOutputCommand.IMPERSONATE_LOGGED_ON_USER_PREFIX + self.command_line_string
        self.payload_length = self._calculate_payload_length()

    def _calculate_payload_length(self):
        """
        Returns the payload length of the command.

        The payload length for this command type is the unicode length of the remote path.
        """
        return sum((
            2*INT_SIZE, # return flags
            7*INT_SIZE, # string array table with offset+length for all three strings
            2*len(self.command_line_string),
            2*len(self.parameters_string),
            2*len(self.base_directory_path),
            ))

    def serialize_sirep(self):
        """Described in parent class"""
        return b''.join((
            utils.pack_uints(self.command_type.value, self.payload_length, self.return_error_flag, self.return_output_flag),
            utils.pack_string_array(self.command_line_string, self.parameters_string, self.base_directory_path),
            ))

    @staticmethod
    def deserialize_sirep(self, command_buffer):
        """Described in parent class"""
        command_type, payload_length, return_error_flag, return_output_flag = utils.unpack_uints(command_buffer[:self.HEADER_SIZE])
        command_line_string, parameters_string, base_directory_path = utils.unpack_string_array(command_buffer[self.HEADER_SIZE:])
        raise NotImplementedError()
