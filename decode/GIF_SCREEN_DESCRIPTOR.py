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
def GIF_SCREEN_DESCRIPTOR(stream, offset, max_size, parent, name):
  result = C.STRUCT(stream, offset, max_size, parent, name, \
      'GIF_SCREEN_DESCRIPTOR', \
      ('Width',               C.USHORT),
      ('Height',              C.USHORT),
      ('Flags',               {C.BITFIELD: (
          ('SizeGlobalColorTable',  3),
          ('Sort',                  1),
          ('ColorResolution',       3),
          ('GlobalColorTable',      1),
      )}),
      ('BkgColorIndex',       C.BYTE),
      ('PixelAspectRatio',    C.BYTE),
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

  if result._Flags._GlobalColorTable.value == 0:
    result._Flags._GlobalColorTable.notes.append('no global color table');
    result._Flags._SizeGlobalColorTable.notes.append('ignored');
    result._Flags._Sort.notes.append('ignored');
    result._BkgColorIndex.notes.append('ignored');
    if result._BkgColorIndex.value != 0:
      result._BkgColorIndex.warnings.append('expected value to be 0');

  if result._PixelAspectRatio.value == 0:
    result._PixelAspectRatio.notes.append('aspect ratio = none');
  else:
    result._PixelAspectRatio.notes.append( \
        'aspect ratio = %f' % ((result._PixelAspectRatio.value + 15) / 64.0));

  return result;

