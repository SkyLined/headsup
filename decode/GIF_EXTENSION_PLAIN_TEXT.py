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
class GIF_EXTENSION_PLAIN_TEXT(Structure):
  type_name = 'PLAIN_TEXT_EXTENSION';
  def __init__(self, stream, offset, max_size, name):
    import C;
    from GIF_BLOCK import GIF_BLOCK;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._data = self.Member(GIF_BLOCK, 'plain_text_extension_data');

    self._plain_text_header = self._data.ContainMember(C.STRUCT, \
        'plain_text_header', 'PLAIN_TEXT_EXTENSION_HEADER', \
        ('LeftPosition',        C.USHORT),
        ('TopPosition',         C.USHORT),
        ('Width',               C.USHORT),
        ('Height',              C.USHORT),
        ('CharWidth',           C.BYTE),
        ('CharHeight',          C.BYTE),
        ('FrgColorIndex',       C.BYTE),
        ('BkgColorIndex',       C.BYTE),
    );

    w = self._plain_text_header._Width.value;
    h = self._plain_text_header._Height.value;
    if w * h > 0xFFFFFFFF:
      self._plain_text_header.warnings.append( \
          'W*H overflows => 0x%X %08X|%d' % \
          (w * h >> 32, w * h & 0xFFFFFFFF, w * h & 0xFFFFFFFF));
    elif w * h > 0x7FFFFFFF:
      self._plain_text_header.warnings.append( \
          'W*H overflows (signed) => 0x%X %08X|%d' % \
          (w * h >> 31, w * h & 0x7FFFFFFF, w * h & 0x7FFFFFFF));
    elif w * h > 0x01000000:
      self._plain_text_header.warnings.append( \
          'W*H is large => 0x%X|%d' % (w * h, w * h));
    else:
      self._plain_text_header.members['Width'].notes.append( \
          'W*H => 0x%X|%d' % (w * h, w * h));
  
    x = self._plain_text_header._LeftPosition.value;
    y = self._plain_text_header._TopPosition.value;
    cw = self._plain_text_header._CharWidth.value;
    ch = self._plain_text_header._CharHeight.value;
    if x + w > 0xFFFF:
      val = x + w;
      self._plain_text_header._LeftPosition.warnings.append( \
          'L+W overflows => 0x%X %02X|%d' % \
          (val >> 16, val & 0xFFFF, val & 0xFFFF));
    elif x + w + cw > 0xFFFF:
      val = x + w + cw;
      self._plain_text_header._CharWidth.warnings.append( \
          'L+W+CW overflows => 0x%X %02X|%d' % \
          (val >> 16, val & 0xFFFF, val & 0xFFFF));
    if y + h > 0xFFFF:
      val = y + h;
      self._plain_text_header._TopPosition.warnings.append( \
          'T+H overflows => 0x%X %02X|%d' % \
          (val >> 16, val & 0xFFFF, val & 0xFFFF));
    elif y + h + ch > 0xFFFF:
      val = y + h + ch;
      self._plain_text_header._TopPosition.warnings.append( \
          'T+H+CH overflows => 0x%X %02X|%d' % \
          (val >> 16, val & 0xFFFF, val & 0xFFFF));

    self._plain_text_data = self._data.ContainMember( \
        C.STRING, 'plain_text_data', self._data.contained_current_max_size);

    self._data.ContainUnused(); # Should always be 0.