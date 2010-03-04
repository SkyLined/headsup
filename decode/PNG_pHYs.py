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

# http://www.w3.org/TR/PNG/#11pHYs
class PNG_pHYs(Structure):
  type_name = 'PNG_pHYs';
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._pixels_per_unit_x = self.Member(C.DWORD, 'pixels_per_unit_x', \
        little_endian = False);
    self._pixels_per_unit_y = self.Member(C.DWORD, 'pixels_per_unit_y', \
        little_endian = False);
    self._unit_specifier = self.Member(C.BYTE, 'unit_specifier');
    if self._unit_specifier.value == 0:
      self._unit_specifier.notes.append('unknown (use for aspect ratio only)');
    elif self._unit_specifier.value == 1:
      self._unit_specifier.notes.append('pixels per metre');
    else:
      self._unit_specifier.warnings.append('expected value to be 0 or 1');

    self.Unused();

