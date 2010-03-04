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

class GIF_IMAGE(Structure):
  type_name = 'GIF_IMAGE';
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    from GIF_BLOCK import GIF_BLOCK;
    from GIF_COLORTABLE import GIF_COLORTABLE;
    from GIF_IMAGE_DESCRIPTOR import GIF_IMAGE_DESCRIPTOR;
    from LZW_compressed_data import LZW_compressed_data;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._descriptor = self.Member(GIF_IMAGE_DESCRIPTOR, 'descriptor');
    
    flags = self._descriptor._Flags;
    self._has_local_color_table = flags._LocalColorTable.value == 1;
    if self._has_local_color_table:
      self._local_color_table_entries = \
          2 ** (flags._SizeLocalColorTable.value + 1);
      self._local_color_table_sorted = flags._Sort.value == 1;
      self._local_color_table = self.Member(GIF_COLORTABLE, \
          'local_color_table', self._local_color_table_entries, \
          self._local_color_table_sorted);
    else:
      self._local_color_table = None;

    self._lzw_minimum_code_size = self.Member(C.BYTE, 'LZW_minimum_code_size');
    if self._lzw_minimum_code_size.value == 0:
      self._lzw_minimum_code_size.warnings.append('expected value > 0');
    
    self._compressed_pixel_data_container = self.Member(GIF_BLOCK, 'pixel_data');
    self._pixel_data_container = \
        self._compressed_pixel_data_container.ContainMember( \
        LZW_compressed_data, 'decompressed_pixel_data', \
        self._lzw_minimum_code_size.value);
    self._pixel_data = self._pixel_data_container.ContainMember( \
        C.STRING, 'pixel_data', \
        self._descriptor._Width.value * self._descriptor._Height.value);
