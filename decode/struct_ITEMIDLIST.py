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

# http://msdn.microsoft.com/en-us/library/bb773321(v=VS.85).aspx
class struct_ITEMIDLIST(Structure):
  type_name = 'ITEMIDLIST';
  def __init__(self, stream, offset, max_size, parent, name):
    from struct_SHITEMID import struct_SHITEMID;
    import C;
    Structure.__init__(self, stream, offset, max_size, parent, name);
    
    self._size = self.Member(C.WORD, 'size');
    self._data = self.Member(C.STRING, 'data', self._size.value);
    self.ContainStream('data', 'data', self._data.value, self._data.size);
    self._Items = [];
    i = 0;
    while self.ContainedDataAvailable():
      item = self.ContainMember(struct_SHITEMID, 'item_%d' % i);
      i += 1;
      self._Items.append(item);
      if item._size.value == 0:
        break;
    if item._size.value != 0:
      self.warnings.append('Expected size of last item to be 0');

    self.ContainUnused();
