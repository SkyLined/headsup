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

import C;

# http://www.w3.org/Graphics/GIF/spec-gif89a.txt
def GIF_IMAGE_DESCRIPTOR(stream, offset, max_size, parent, name):
  result = C.STRUCT(stream, offset, max_size, parent, name, \
      'GIF_IMAGE_DESCRIPTOR', \
      ('LeftPosition',              C.USHORT),
      ('TopPosition',               C.USHORT),
      ('Width',                     C.USHORT),
      ('Height',                    C.USHORT),
      ('Flags',                     {C.BITFIELD: (
          ('SizeLocalColorTable',   3),
          ('Reserved',              2),
          ('Sort',                  1),
          ('Interlace',             1),
          ('LocalColorTable',       1),
      )}),
  );

  w = result._Width.value;
  h = result._Height.value;
  if w * h > 0xFFFFFFFF:
    result.warnings.append('W*H overflows => 0x%X %08X|%d' % \
        (w * h >> 32, w * h & 0xFFFFFFFF, w * h & 0xFFFFFFFF));
  elif w * h > 0x7FFFFFFF:
    result.warnings.append('W*H overflows (signed) => 0x%X %08X|%d' % \
        (w * h >> 31, w * h & 0x7FFFFFFF, w * h & 0x7FFFFFFF));
  elif w * h > 0x01000000:
    result.warnings.append('W*H is large => 0x%X|%d' % (w * h, w * h));
  else:
    result._Width.notes.append('W*H => 0x%X|%d' % (w * h, w * h));

  x = result._LeftPosition.value;
  y = result._TopPosition.value;
  if x + w > 0xFFFF:
    result._LeftPosition.warnings.append( \
        'X+W overflows => 0x%X %02X|%d' % \
        (x + w >> 16, x + w & 0xFFFF, x + w & 0xFFFF));
  if y + h > 0xFFFF:
    result._TopPosition.warnings.append( \
        'Y+H overflows => 0x%X %02X|%d' % \
        (y + h >> 16, y + h & 0xFFFF, y + h & 0xFFFF));

  if result._Flags._LocalColorTable.value == 0:
    result._Flags._LocalColorTable.notes.append('no local color table');
    result._Flags._SizeLocalColorTable.notes.append('ignored');
    result._Flags._Sort.notes.append('ignored');

  if result._Flags._Interlace.value == 0:
    result._Flags._Interlace.notes.append('image is not interlaced');
  else:
    result._Flags._Interlace.notes.append('image is interlaced');

  return result;

