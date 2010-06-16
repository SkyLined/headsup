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

class RIFF_ACON_anih(Structure):
  type_name = 'RIFF_anih';
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    from struct_ANIHEADER import struct_ANIHEADER;
    Structure.__init__(self, stream, offset, max_size, parent, name);
    
    self._anih = self.Member(struct_ANIHEADER, 'anih_data');

    header_format_details = ', '.join([
      '%d frames' % self._anih._Frames.value,
      '%d steps' % self._anih._Steps.value,
      '%d bit' % self._anih._BitCount.value,
    ]);
    
    self.format_details = 'anih(%s)' % header_format_details;

    self.Unused();
