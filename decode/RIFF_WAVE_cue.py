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

class RIFF_WAVE_cue(Structure):
  type_name = 'RIFF_WAVE_cue'
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._NumCuePoints = self.Member(C.DWORD, 'NumCuePoints');
    self._CuePoints = self.Member(C.ARRAY, 'CuePoints', \
        self._NumCuePoints.value, C.STRUCT, 'CUE_POINT', 
        ('PointName', {C.STRING: 4}),
        ('Position', C.DWORD),
        ('Chunkname', {C.STRING: 4}),
        ('ChunkStart', C.DWORD),
        ('BlockStart', C.DWORD),
        ('SampleOffset', C.DWORD),
    );
    self.format_details = 'cue';
    for cue_point in self._CuePoints._items:
      if cue_point._ChunkStart.value != 0:
        cue_point._ChunkStart.warnings.append('expected value to be 0');

    self.Unused();
