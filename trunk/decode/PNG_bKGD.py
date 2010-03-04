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

# http://www.w3.org/TR/PNG/#11bKGD
class PNG_bKGD(Structure):
  type_name = 'PNG_bKGD';
  def __init__(self, stream, offset, max_size, parent, name, \
      color_type, bit_depth, palette_entries):
    import C;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    if color_type in [0, 4]:
      self._grey = self.Member(C.WORD, 'grey', little_endian = False);
      CheckBits(self._grey, bit_depth);
    elif color_type in [2, 6]:
      self._red = self.Member(C.WORD, 'red', little_endian = False);
      CheckBits(self._red, bit_depth);
      self._green = self.Member(C.WORD, 'green', little_endian = False);
      CheckBits(self._green, bit_depth);
      self._blue = self.Member(C.WORD, 'blue', little_endian = False);
      CheckBits(self._blue, bit_depth);
    elif color_type == 3:
      self._palette_index = self.Member(C.BYTE, 'palette index');
      if palette_entries is not None \
          and self._palette_index.value >= palette_entries:
        self._alpha_values.warnings.append(
            'expected value to be at most 0x%X|%d' % \
                (palette_entries, palette_entries));
    elif color_type == None:
      self.warnings.append(
          'chunk has no function when the color type is unknown');
    else:
      self.warnings.append(
          'chunk has no function for color type %d' % color_type);

    self.Unused();

def CheckBits(bits, bit_depth):
  if bit_depth is not None:
    max_value = 2 ** bit_depth - 1;
    if bits.value > max_value:
      bits.warnings.append('expected value to be at most 0x%X|%d' % \
          (max_value, max_value));
