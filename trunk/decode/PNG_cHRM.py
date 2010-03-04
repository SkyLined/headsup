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

# http://www.w3.org/TR/PNG/#11cHRM
class PNG_cHRM(Structure):
  type_name = 'PNG_cHRM';
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._white_point_x = self.Member(C.DWORD, 'White_point_X', little_endian = False);
    white_point_x = self._white_point_x.value / 100000.0;
    self._white_point_x.notes.append('= %f;' % white_point_x);

    self._white_point_y = self.Member(C.DWORD, 'White_point_Y', little_endian = False);
    white_point_y = self._white_point_y.value / 100000.0;
    self._white_point_y.notes.append('= %f;' % white_point_y);

    self._red_x = self.Member(C.DWORD, 'Red_X', little_endian = False);
    red_x = self._red_x.value / 100000.0;
    self._red_x.notes.append('= %f;' % red_x);

    self._red_y = self.Member(C.DWORD, 'Red_Y', little_endian = False);
    red_y = self._red_y.value / 100000.0;
    self._red_y.notes.append('= %f;' % red_y);

    self._green_x = self.Member(C.DWORD, 'Green_X', little_endian = False);
    green_x = self._green_x.value / 100000.0;
    self._green_x.notes.append('= %f;' % green_x);

    self._green_y = self.Member(C.DWORD, 'Green_Y', little_endian = False);
    green_y = self._green_y.value / 100000.0;
    self._green_y.notes.append('= %f;' % green_y);

    self._blue_x = self.Member(C.DWORD, 'Blue_X', little_endian = False);
    blue_x = self._blue_x.value / 100000.0;
    self._blue_x.notes.append('= %f;' % blue_x);

    self._blue_y = self.Member(C.DWORD, 'Blue_Y', little_endian = False);
    blue_y = self._blue_y.value / 100000.0;
    self._blue_y.notes.append('= %f;' % blue_y);

    self.Unused();

