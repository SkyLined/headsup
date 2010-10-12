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

KNOWN_SHITEMID_IDS = {
  0x1F: 'Some hardcoded value',
  0x2F: 'Absolute path',
  0x31: 'Path component 1',
  0x32: 'Path component 2',
  0x33: 'Path component 3',
  0x34: 'Path component 4',
  0x35: 'Path component 5',
  0x36: 'Path component 6',
  0x37: 'Path component 7',
  0x38: 'Path component 8',
  0x39: 'Path component 9',
}

# http://msdn.microsoft.com/en-us/library/bb759800(v=VS.85).aspx
class struct_SHITEMID(Structure):
  type_name = 'SHITEMID';
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._size = self.Member(C.WORD, 'size');
    if self._size.value >= 2:
      self._data = self.Member(C.STRING, 'data', self._size.value - 2);
      self.ContainStream('data', 'data', self._data.value, self._data.size);
      self._Id = self.ContainMember(C.BYTE, 'Id');
      if self._Id.value in KNOWN_SHITEMID_IDS:
        self._Id.notes.append(KNOWN_SHITEMID_IDS[self._Id.value]);
      else:
        self._Id.warnings.append('Unknown value');
      if self._Id.value == 0x25:
        self._IdPadding = self.ContainMember(C.BYTE, 'IdPadding');
        if self._IdPadding.value != 0:
          self._IdPadding.warnigns.append('Expected value to be 0');
        self._Path = self.ContainMember(C.UNICODE_STRING, 'Path');
      elif self._Id.value == 0x2F:
        self._Path = self.ContainMember(C.STRING, 'Path', self._data.size - 1);
      elif self._Id.value > 0x30 and self._Id.value <= 0x39:
        self._Unknown = self.ContainMember(C.ARRAY, 'Unknown', 11, C.BYTE);
        self._Path = self.ContainMember(C.STRING, 'Path');
        if self._Path.size % 2 == 1:
          self._PathPadding = self.ContainMember(C.BYTE, 'PathPadding');
        self._SizeOfUnicodePathData = self.ContainMember(C.WORD, 'SizeOfUnicodePathData');
        self._Word8 = self.ContainMember(C.WORD, 'Word8');
        self._Word4 = self.ContainMember(C.WORD, 'Word4');
        self._WordBEEF = self.ContainMember(C.WORD, 'WordBEEF');
        self._QWordUnknown = self.ContainMember(C.QWORD, 'QWordUnknown');
        self._DWord2A = self.ContainMember(C.DWORD, 'DWord2A');
        self._WordUnknown1 = self.ContainMember(C.WORD, 'WordUnknown1');
        self._DWord0 = self.ContainMember(C.DWORD, 'DWord0');
        self._DWord1 = self.ContainMember(C.DWORD, 'DWord1');
        self._Nulls = self.ContainMember(C.ARRAY, 'Nulls', 0xC, C.BYTE);
        self._UnicodePath = self.ContainMember(C.UNICODE_STRING, 'UnicodePath');
        self._WordUnknown2 = self.ContainMember(C.WORD, 'WordUnknown2');
        self.ContainUnused();
      else:
        self._Value = self.ContainMember(C.ARRAY, 'value', self._data.size - 1, C.BYTE);
    else:
      self._data = None;
      self._Value = None;
      if self._size.value != 0:
        self._size.warnings.append('Expected value to be 0, 2 or larger');
