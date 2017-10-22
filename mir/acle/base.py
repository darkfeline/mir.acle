# Copyright (C) 2017 Allen Li
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""acle base implementation

This module implements the very basic functionality for an async command
line loop.
"""

import asyncio
import sys


def start_command_line(handler, input_file=None, loop=None):
    """Start an asynchronous command line.

    handler is a coroutine which is called with each command line as a
    string.

    input_file is a file object to read commands from.  If missing, use
    stdin.

    loop is the asyncio event loop to use.  If missing, use
    asyncio.get_event_loop().
    """
    if input_file is None:
        input_file = sys.stdin
    if loop is None:
        loop = asyncio.get_event_loop()
    loop.run_until_complete(_mainloop(loop, handler, input_file))


async def _mainloop(loop, handler, input_file):
    reader = await _async_reader(loop, input_file)
    while True:
        line = await reader.readline()
        if not line:
            break
        await handler(line)


async def _async_reader(loop, file):
    reader = asyncio.StreamReader()
    reader_protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: reader_protocol, file)
    return reader
