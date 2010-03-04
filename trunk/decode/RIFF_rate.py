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

class RIFF_rate(Structure):
  type_name = 'RIFF_rate';
  def __init__(self, stream, offset, max_size, parent, name):
    import math;
    import C;
    Structure.__init__(self, stream, offset, max_size, parent, name);
    self.dump_simplified = True;

    number_of_rates = int(math.floor(max_size / 4.0));
    self._rates = self.Member(C.ARRAY, 'rates', number_of_rates, C.DWORD);

    self.Unused();

  def SimplifiedValue(self, header = None):
    value = repr(self.value);
    if len(value) > 50:
      value = value[:50] + '...' + value[-1];
    return 'string(0x%X|%d bytes): %s' % \
        (self.size, self.size, value);
