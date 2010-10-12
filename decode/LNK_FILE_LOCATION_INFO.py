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

# http://www.stdlib.com/art6-1-Shortcut-File-Format-lnk.html
KNOWN_LOCATIONS = {
  0: 'Local volume',
  1: 'Network share',
};

class LNK_FILE_LOCATION_INFO(Structure):
  type_name = 'LNK_FILE_LOCATION_INFO';
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    Structure.__init__(self, stream, offset, max_size, parent, name);
    
    self._size = self.Member(C.DWORD, 'size');
    if self._size.value != 0:
      self._data = self.Member(C.STRING, 'data', self._size.value);
      self.ContainStream('data', 'data', self._data.value, self._data.size);
      self._EndOffset = self.ContainMember(C.DWORD, 'EndOffset');
      if self._EndOffset.value != 0x1C:
        self._EndOffset.warnings.append('Expected value to be 0x1C');
      self._Location = self.ContainMember(C.DWORD, 'Location');
      if self._Location.value in KNOWN_LOCATIONS:
        self._Location.notes.append(KNOWN_LOCATIONS[self._Location.value]);
      else:
        self._Location.warnings.append('Expected value to be 0 or 1');
      self._OffsetLocalVolumeTable = self.ContainMember(C.DWORD, 'OffsetLocalVolumeTable');
      self._OffsetBasePath = self.Member(C.DWORD, 'OffsetBasePath');
      self._OffsetNetworkVolumeTable = self.ContainMember(C.DWORD, 'OffsetNetworkVolumeTable');
      self._OffsetFinalPart = self.Member(C.DWORD, 'OffsetFinalPart');
      # TO BE CONTINUED...