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

class RIFF_WAVE_adtl_note(Structure):
  type_name = 'RIFF_WAVE_adtl_note'
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._CuePointName = self.Member(C.STRING, 'CuePointName', 4);
    self._Text = self.Member(C.STRING, 'Text', self.current_max_size);
    self.format_details = 'note';

    self.Unused();
