# Copyright 2010 Google Inc.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#      http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# http://www.w3.org/TR/PNG/#D-CRCAppendix
CRC_TABLE = [];
for n in range(0x100):
  c = n;
  for k in range(8):
    if c & 1:
      c = 0xEDB88320 ^ (c >> 1);
    else:
      c >>= 1;
  CRC_TABLE.append(c);

def PNG_CRC32(string):# == zlib.crc32
  crc = 0xFFFFFFFF;
  for char in string:
    crc = CRC_TABLE[(crc & 0xFF) ^ ord(char)] ^ (crc >> 8);
  return crc ^ 0xFFFFFFFF;

