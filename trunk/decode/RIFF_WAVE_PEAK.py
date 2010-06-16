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

import math;
from Structure import Structure;

class RIFF_WAVE_PEAK(Structure):
  type_name = 'RIFF_WAVE_PEAK'
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._Version = self.Member(C.DWORD, 'Version');
    self._TimeStamp = self.Member(C.DWORD, 'TimeStamp');
    if 'fmt ' in parent.parent._named_chunks:
      fmt_chunk = parent.parent._named_chunks['fmt '][0];
      num_channels = fmt_chunk._data._NumChannels.value;
    else:
      num_channels = math.floor(self.current_max_size / 8.0);
      self.warnings.append('No "fmt" found before this chunk; number of ' \
          'peaks is based on the size of this chunk');
    self._Peaks = self.Member(C.ARRAY, 'Peaks', \
        num_channels, C.STRUCT, 'POSITION_PEAK', 
        ('Value',    C.FLOAT32),
        ('Position', C.DWORD),
    );
    self.format_details = 'PEAK';

    self.Unused();
