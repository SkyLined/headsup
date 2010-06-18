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

# http://www.w3.org/TR/PNG/#11IHDR
class PNG_IHDR(Structure):
  type_name = 'PNG_IHDR';
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    Structure.__init__(self, stream, offset, max_size, parent, name);
    self._data = self.Member(C.STRUCT, 'data', 'PNG_IHDR', \
      ('Width',           {C.DWORD: False}),
      ('Height',          {C.DWORD: False}),
      ('BitDepth',         C.BYTE),
      ('ColorType',        C.BYTE),
      ('Compression',      C.BYTE),
      ('Filter',           C.BYTE),
      ('Interlace',        C.BYTE),
    );

    w = self._data._Width.value;
    h = self._data._Height.value;
    if w * h > 0xFFFFFFFF:
      self._data.warnings.append('W*H overflows => 0x%X %08X|%d' % \
          (w * h >> 32, w * h & 0xFFFFFFFF, w * h & 0xFFFFFFFF));
    elif w * h > 0x7FFFFFFF:
      self._data.warnings.append('W*H overflows (signed) => 0x%X %08X|%d' % \
          (w * h >> 31, w * h & 0x7FFFFFFF, w * h & 0x7FFFFFFF));
    elif w * h > 0x01000000:
      self._data.warnings.append('W*H is large => 0x%X|%d' % (w * h, w * h));
    else:
      self._data._Width.notes.append('W*H => 0x%X|%d' % (w * h, w * h));
    if w == 0:
      self._data._Width.warnings.append('expect value larger than 0');
    if w >= 0x80000000:
      self._data._Width.warnings.append( \
          'expect value smaller than 0x80000000');
    if h == 0:
      self._data._Height.warnings.append('expect value larger than 0');
    if h >= 0x80000000:
      self._data._Height.warnings.append( \
          'expect value smaller than 0x80000000');
  
    color_type = self._data._ColorType.value;
    if color_type & 1:
      self._data._ColorType.notes.append('palette used');
    if color_type & 2:
      self._data._ColorType.notes.append('color used');
    if color_type & 4:
      self._data._ColorType.notes.append('alpha channel used');
  
    bit_depth = self._data._BitDepth.value;
    self._pixels_are_grayscale = False;
    self._pixels_are_RGB = False;
    self._pixels_are_palette = False;
    self._pixels_have_alpha = False;
    self._sample_depth = bit_depth;
    if bit_depth == 1:
      self._data._BitDepth.notes.append('black/white');
    else:
      self._data._BitDepth.notes.append('%d colors' % (2 ** bitdepth));
    if color_type == 0:
      self._data._ColorType.notes.append('greyscale');
      if bit_depth not in [1, 2, 4, 8, 16]:
        self._data._BitDepth.warnings.append( \
            'expect value to be 1, 2, 4, 8 or 16');
      self._pixels_are_grayscale = True;
    elif color_type == 2:
      self._data._ColorType.notes.append('truecolor');
      if bit_depth not in [8, 16]:
        self._data._BitDepth.warnings.append( \
            'expect value to be 8 or 16');
      self._pixels_are_RGB = True;
    elif color_type == 3:
      self._data._ColorType.notes.append('indexed-color');
      if bit_depth not in [1, 2, 4, 8]:
        self._data._BitDepth.warnings.append( \
            'expect value to be 1, 2, 4 or 8');
      self._pixels_are_palette = True;
      self._sample_depth = 8;
    elif color_type == 4:
      self._data._ColorType.notes.append('greyscale + alpha');
      if bit_depth not in [8, 16]:
        self._data._BitDepth.warnings.append( \
            'expect value to be 8 or 16');
      self._pixels_are_grayscale = True;
      self._pixels_have_alpha = True;
    elif color_type == 6:
      self._data._ColorType.notes.append('truecolor + alpha');
      if bit_depth not in [8, 16]:
        self._data._BitDepth.warnings.append( \
            'expect value to be 8 or 16');
      self._pixels_are_RGB = True;
      self._pixels_have_alpha = True;
    else:
      self._data._ColorType.warnings.append( \
          'expect value to be 0, 2, 3, 4 or 6');
  
    if self._data._Compression.value != 0:
      self._data._Compression.warnings.append('expect value to be 0');
    else:
      self._data._Compression.notes.append( \
          'deflate/inflate with 32K sliding window');
  
    if self._data._Filter.value != 0:
      self._data._Filter.warnings.append('expect value to be 0');
    else:
      self._data._Filter.notes.append( \
          'adaptive filtering with five basic filter types');
  
    if self._data._Interlace.value == 0:
      self._data._Interlace.notes.append('no interlace');
    elif self._data._Interlace.value == 1:
      self._data._Interlace.notes.append('Adam7 interlace');
    else:
      self._data._Interlace.warnings.append('expect value to be 0 or 1');

    self.Unused();

