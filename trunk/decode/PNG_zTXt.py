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

# http://www.w3.org/TR/PNG/#11zTXt
class PNG_zTXt(Structure):
  type_name = 'PNG_zTXt';
  def __init__(self, stream, offset, max_size, parent, name):
    import math;
    import C;
    from ZLIB_BLOCK import ZLIB_BLOCK;
    from struct_RGBAQUAD import struct_RGBAQUAD;
    from PNG_CheckText import PNG_CheckText;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    null_seperator_index = self.GetMaxStream().find('\0');
    if null_seperator_index == -1:
      self._keyword = None;
      self._null_seperator = None;
      self.warnings.append('no null found to seperate profile name from text, ' \
          'assuming text only');
    else:
      self._keyword = self.Member(C.STRING, 'keyword', null_seperator_index);
      PNG_CheckText(self._keyword, can_be_empty = False, max_size = 79, \
          no_extra_spaces = True, utf_8 = False, newlines = False, \
          is_keyword = True);
      self._null_seperator = self.Member(C.BYTE, 'null_seperator');

    self._compression_method = self.Member(C.BYTE, 'compression_method');
    if self._compression_method.value == 0:
      self._compression_method.notes.append('zlib deflate');
    else:
      self._compression_method.warnings.append( \
          'unknown methods, zlib deflate assumed');

    self._compressed_text = self.Member(ZLIB_BLOCK, 'compressed_text');
    self._text = self._compressed_text.ContainMember( \
        C.STRING, 'decompressed_text', self._compressed_text.contained_current_max_size);
    PNG_CheckText(self._text, can_be_empty = True, max_size = None, \
        no_extra_spaces = False, utf_8 = False, newlines = True, \
        is_keyword = False);

    self.Unused();

def CheckName(name):
  if len(name.value) == 0:
    name.warnings.append('expected at least one character');
  elif len(name.value) > 79:
    name.warnings.append('expected at most 79 characters');
  for char in name.value:
    c = ord(char);
    if c < 0x20 or (char > 0x7E and char < 0xA1):
      name.warnings.append('string contains non-printable latin-1 characters');
      break;
  if ' ' in [name.value[0], name.value[-1]]:
    name.warnings.append('string must not start or end with a space');
