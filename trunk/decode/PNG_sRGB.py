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

class PNG_sRGB(Structure):
  type_name = 'PNG_sRGB';
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._intent = self.Member(C.BYTE, 'intent');
    
    if self._intent.value == 0:
      self._intent.notes.append('perceptual');
    elif self._intent.value == 1:
      self._intent.notes.append('relative colorimetric');
    elif self._intent.value == 2:
      self._intent.notes.append('saturation');
    elif self._intent.value == 3:
      self._intent.notes.append('absolute colorimetric');
    else:
      self._intent.warnings.append('expected value to be 0, 1, 2 or 3');

    self.Unused();
