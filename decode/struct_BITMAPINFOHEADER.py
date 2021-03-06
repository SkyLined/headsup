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


# http://msdn.microsoft.com/en-us/library/aa930622.aspx
def struct_BITMAPINFOHEADER(stream, offset, max_size, parent, name, \
    height_div_2 = False):
  import C;
  result = C.STRUCT(stream, offset, max_size, parent, name, \
      'BITMAPINFOHEADER', \
      ('Size',                    C.DWORD),
      ('Width',                   C.LONG),
      ('Height',                  C.LONG),
      ('Planes',                  C.WORD),
      ('BitCount',                C.WORD),
      ('Compression',             C.DWORD),
      ('SizeImage',               C.DWORD),
      ('XPelsPerMeter',           C.INT),
      ('YPelsPerMeter',           C.INT),
      ('ClrUsed',                 C.DWORD),
      ('ClrImportant',            C.DWORD),
  );

  w = result._Width.value;
  h = result._Height.value;
  details = [
    '%dx%d' % (w, h),
    '%d bit' % (result._BitCount.value),
  ];
  if w <= 0:
    result._Width.warnings.append('expected value larger than 0');
  if h <= 0:
    result._Height.notes.append('image is top-down');
    h = -h;
  if height_div_2:
    h /= 2;
    result._Height.notes.append( \
        'image divided into 2 * 0x%X|%d' % (h, h));
  if w > 0 and h > 0:
    if w > 10000:
      result.warnings.append('value is large');
    if h > 10000:
      result.warnings.append('value is large');
    if w * h > 0xFFFFFFFF:
      result.warnings.append('W*H overflows => 0x%X`%08X|%d' % \
          (w * h >> 32, w * h & 0xFFFFFFFF, w * h & 0xFFFFFFFF));
    elif w * h > 0x7FFFFFFF:
      result.warnings.append('W*H overflows (signed) => 0x%X`%08X|%d' % \
          (w * h >> 31, w * h & 0x7FFFFFFF, w * h & 0x7FFFFFFF));
    elif w * h > 0x01000000:
      result.warnings.append('W*H is large => 0x%X|%d' % (w * h, w * h));
    else:
      result._Width.notes.append('W*H => 0x%X|%d' % (w * h, w * h));

  if result._Planes.value > 100:
    result._Planes.warnings.append('value is large, expected value to be 1');
  elif result._Planes.value != 1:
    result._Planes.warnings.append('expected value to be 1');
  if result._BitCount.value not in [1,4,8,16,24,32]:
    result._BitCount.warnings.append( \
        'Unusual value; expected 1, 4, 8, 16, 24 or 32');
  compression_methods = {  # description, BitCount limitations
    0: ('uncompressed',     None),
    1: ('8 bit RLE',        [8]),
    2: ('4 bit RLE',        [4]),
    3: ('bitfield',         [16, 32]),
    4: ('JPEG',             None),
    5: ('PNG',              None),
  };
  if result._Compression.value not in compression_methods:
    result._Compression.warnings.append('unknown compression method');
    details.append('unknown compression');
  else:
    description, valid_bit_counts = \
        compression_methods[result._Compression.value];
    details.append(description);
    result._Compression.notes.append(description);
    if valid_bit_counts is not None \
        and result._BitCount.value not in valid_bit_counts:
      result._Compression.warnings.append( \
          'invalid for %d bits per pixel' % result._BitCount.value);

  if result._SizeImage.value > 0x010000000:
    result._SizeImage.warnings.append( \
        'image is large: %dMb' % (result._SizeImage.value / 0x100000));
  if result._XPelsPerMeter.value < 0:
    result._XPelsPerMeter.warnings.append('expected positive value or 0');
  if result._YPelsPerMeter.value < 0:
    result._YPelsPerMeter.warnings.append('expected positive value or 0');

  max_number_of_colors = 2 ** result._BitCount.value;
  if result._ClrUsed.value > max_number_of_colors:
    result._ClrUsed.warnings.append('expected value < 0x%X|%d' % \
        (max_number_of_colors, max_number_of_colors));
  if result._ClrImportant.value > result._ClrUsed.value:
    result._ClrImportant.warnings.append('expected value < 0x%X|%d' % \
        (result._ClrUsed.value, result._ClrUsed.value));

  result.format_details = ', '.join(details);
  return result;