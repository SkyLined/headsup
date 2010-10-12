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

# http://www.stdlib.com/art6-Shortcut-File-Format-lnk.html
class LNK(Structure):
  type_name = 'LNK';
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    from struct_SHELL_LINK_HEADER import struct_SHELL_LINK_HEADER;
    from struct_ITEMIDLIST import struct_ITEMIDLIST;
    from struct_LINK_INFO import struct_LINK_INFO;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._ShellLinkHeader = self.Member(struct_SHELL_LINK_HEADER, 'Header');
    
    if self._ShellLinkHeader._LinkFlags._HasLinkTargetIDList.value == 0:
      self._ShellItemIdList = None;
    else:
      self._ShellItemIdList = self.Member( \
          struct_ITEMIDLIST, 'ShellItemIdList');
    self._LinkInfo = self.Member(struct_LINK_INFO, 'LinkInfo');