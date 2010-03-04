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

from Structure import Structure;

# http://msdn.microsoft.com/en-us/library/aa921550.aspx
class struct_BITMAPINFO(Structure):
  type_name = 'struct BITMAPINFO';
  def __init__(self, stream, offset, max_size, parent, name, \
      height_div_2 = False):
    import C;
    from struct_BITMAPINFOHEADER import struct_BITMAPINFOHEADER;
    from struct_RGBQUAD import struct_RGBQUAD;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._header = self.Member(struct_BITMAPINFOHEADER, \
        'header', height_div_2);

    bit_count = self._header._BitCount.value;
    compression = self._header._Compression.value;
    number_of_colors = 2 ** bit_count;
    used_colors = self._header._ClrUsed.value;
    # http://msdn.microsoft.com/en-us/library/aa930622.aspx

    if used_colors:
      number_of_rgb_quads = used_colors;
    else:
      number_of_rgb_quads = 2 ** bit_count;

    if bit_count in [16, 24, 32]:
      number_of_rgb_quads = 0;
    if compression == 3: # bitfields:
      number_of_rgb_quads = 3;

    if number_of_rgb_quads > 0:
      self._color_table = self.Member(C.ARRAY, 'color_table', \
          number_of_rgb_quads, struct_RGBQUAD);
      self._color_table.dump_simplified = True;
    else:
      self._color_table = None;
