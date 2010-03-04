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

# http://www.w3.org/TR/PNG/#11tIME
class PNG_tIME(Structure):
  type_name = 'PNG_tIME';
  def __init__(self, stream, offset, max_size, parent, name):
    import math, time;
    import C;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._year = self.Member(C.WORD, 'year', little_endian = False);
    if self._year.value > time.gmtime()[0] or self._year.value < 1900:
      self._year.notes.append('unlikely value');

    self._month = self.Member(C.BYTE, 'month');
    if self._month.value > 12 or self._month.value < 1:
      self._month.warnings.append('illegal value');

    self._day = self.Member(C.BYTE, 'day');
    if self._day.value > 31 or self._day.value < 1:
      self._day.warnings.append('illegal value');

    self._hour = self.Member(C.BYTE, 'hour');
    if self._hour.value > 23 or self._hour.value < 0:
      self._hour.warnings.append('illegal value');

    self._minute = self.Member(C.BYTE, 'minute');
    if self._minute.value > 59 or self._minute.value < 0:
      self._minute.warnings.append('illegal value');

    self._second = self.Member(C.BYTE, 'second');
    if self._second.value > 60 or self._second.value < 0: # Leap second = 60 :)
      self._second.warnings.append('illegal value');

    self.Unused();
