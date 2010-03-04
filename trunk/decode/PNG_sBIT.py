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

# http://www.w3.org/TR/PNG/#11sBIT
class PNG_sBIT(Structure):
  type_name = 'PNG_sBIT';
  def __init__(self, stream, offset, max_size, parent, name, \
      color_type, sample_depth):
    import C;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    if color_type == 0:
      self._significant_greyscale_bits = self.Member(C.BYTE, \
          'significant_greyscale_bits');
      CheckBits(self._significant_greyscale_bits, sample_depth);
    elif color_type in [2, 3]:
      self._significant_red_bits = self.Member(C.BYTE, \
          'significant_red_bits');
      CheckBits(self._significant_red_bits, sample_depth);
      self._significant_green_bits = self.Member(C.BYTE, \
          'significant_green_bits');
      CheckBits(self._significant_green_bits, sample_depth);
      self._significant_blue_bits = self.Member(C.BYTE, \
          'significant_blue_bits');
      CheckBits(self._significant_blue_bits, sample_depth);
    elif color_type == 4:
      self._significant_greyscale_bits = self.Member(C.BYTE, \
          'significant_greyscale_bits');
      CheckBits(self._significant_greyscale_bits, sample_depth);
      self._significant_alpha_bits = self.Member(C.BYTE, \
          'significant_alpha_bits');
      CheckBits(self._significant_alpha_bits, sample_depth);
    elif color_type == 6:
      self._significant_red_bits = self.Member(C.BYTE, \
          'significant_red_bits');
      CheckBits(self._significant_red_bits, sample_depth);
      self._significant_green_bits = self.Member(C.BYTE, \
          'significant_green_bits');
      CheckBits(self._significant_green_bits, sample_depth);
      self._significant_blue_bits = self.Member(C.BYTE, \
          'significant_blue_bits');
      CheckBits(self._significant_blue_bits, sample_depth);
      self._significant_alpha_bits = self.Member(C.BYTE, \
          'significant_alpha_bits');
      CheckBits(self._significant_alpha_bits, sample_depth);
    elif color_type == None:
      self.warnings.append(
          'chunk has no function when the color type is unknown');
    else:
      self.warnings.append(
          'chunk has no function for color type %d' % color_type);

    self.Unused();

def CheckBits(bits, sample_depth):
  if sample_depth is not None:
    if bits.value == 0:
      bits.warnings.append('expected value to be at least 1');
    elif bits.value > sample_depth:
      bits.warnings.append('expected value to be at most 0x%X|%d' % \
          (sample_depth, sample_depth));
      
    