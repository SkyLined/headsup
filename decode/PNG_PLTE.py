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

# http://www.w3.org/TR/PNG/#11PLTE
class PNG_PLTE(Structure):
  type_name = 'PNG_PLTE';
  def __init__(self, stream, offset, max_size, parent, name):
    import math;
    import C;
    from struct_RGBTRIPPLE import struct_RGBTRIPPLE;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    if max_size % 3 != 0:
      self.warnings.append('pallete size should be divisible by 3');

    self._number_of_rgb_tripples = math.floor(max_size / 3.0);
    self._rgb_tripples = self.Member(C.ARRAY, 'rgb_tripples', \
        self._number_of_rgb_tripples, struct_RGBTRIPPLE);
    self._rgb_tripples.dump_simplified = True;

    self.Unused();
