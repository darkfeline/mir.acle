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

import asyncio
import sys


def start(handler, loop=None):
    if loop is None:
        loop = asyncio.get_event_loop()
    loop.run_until_complete(_mainloop(loop, handler))


async def _async_reader(loop, file):
    reader = asyncio.StreamReader()
    reader_protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: reader_protocol, file)
    return reader


async def _mainloop(loop, handler):
    stdin = await _async_reader(loop, sys.stdin)
    while True:
        line = await stdin.readline()
        if not line:
            break
        handler(line)
