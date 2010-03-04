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

# http://www.w3.org/Graphics/GIF/spec-gif89a.txt
class GIF_EXTENSION_GRAPHICS_CONTROL(Structure):
  type_name = 'GRAPHICS_CONTROL_EXTENSION';
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    from GIF_BLOCK import GIF_BLOCK;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._data = self.Member(GIF_BLOCK, 'data');

    if self._data.contained_max_size != 0x4:
      self._data.warnings.append('expected contained data to be 0x4 bytes');

    self._graphics_control = self._data.ContainMember(C.STRUCT, \
        'data', 'GRAPHICS_CONTROL', \
        ('Flags',                     {C.BITFIELD: (
            ('TransparentColor',      1),
            ('UserInput',             1),
            ('DisposalMethod',        3),
            ('Reserved',              3),
        )}),
        ('DelayTime',                 C.BYTE),
        ('TransparentColorIndex',     C.BYTE),
    );

    self._data.ContainUnused();
  
    flags = self._graphics_control._Flags;
    if flags._TransparentColor.value == 0:
      flags._TransparentColor.notes.append('transparent color index is not given');
      self._graphics_control._TransparentColorIndex.notes.append('ignored');
    else:
      flags._TransparentColor.notes.append('transparent color index is given');
  
    if flags._UserInput.value == 0:
      flags._UserInput.notes.append('user input is not expected');
    else:
      flags._UserInput.notes.append('user input is expected');
  
    disposal_methods = { 0: 'not specified', 1: 'do not dispose', \
        2: 'restore to background color', 3: 'restore to previous'}
    if flags._DisposalMethod.value in disposal_methods:
      flags._DisposalMethod.notes.append( \
        disposal_methods[flags._DisposalMethod.value]);
    else:
      flags._DisposalMethod.warning.append('expected value to be 0, 1, 2 or 3');
  
    self._graphics_control._DelayTime.notes.append('time = %.2f seconds' % \
        (self._graphics_control._DelayTime.value / 100.0));
