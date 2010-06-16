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

# http://en.wikipedia.org/wiki/BMP_file_format
class BMP(Structure):
  type_name = 'BMP';
  def __init__(self, stream, offset, max_size, parent, name):
    from struct_BMPHEADER import struct_BMPHEADER;
    from BITMAP import BITMAP;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._header = self.Member(struct_BMPHEADER, 'header');

    if self._header._FileSize.value != max_size:
      self._header._FileSize.warnings.append( \
          'actual size = 0x%X|%d' % (max_size, max_size));

    self._bitmap = self.Member(BITMAP, 'bitmap', self._header._Offset.value);

