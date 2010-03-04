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

# http://en.wikipedia.org/wiki/BMP_file_format
class BMP(Structure):
  type_name = 'BMP';
  def __init__(self, stream, offset, max_size, parent, name):
    import math;
    import C;
    from struct_BMPHEADER import struct_BMPHEADER;
    from struct_BITMAPINFO import struct_BITMAPINFO;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._header = self.Member(struct_BMPHEADER, 'header');

    if self._header._FileSize.value != max_size:
      self._header._FileSize.warnings.append( \
          'actual size = 0x%X|%d' % (max_size, max_size));

    self._bitmapinfo = self.Member(struct_BITMAPINFO, 'bitmapinfo');

    w = self._bitmapinfo._header._Width.value;
#    if w % 2 == 1:
#      w += 1;
#      self._bitmapinfo._header._Width.notes.append( \
#          'uneven: rounded up to 0x%X|%d' % (w, w));
    h = self._bitmapinfo._header._Height.value;
    bits_per_pixel = self._bitmapinfo._header._BitCount.value;
    # Calculate size in bytes of image data:
    bits_per_row = bits_per_pixel * w;
    # each row is padded to DWORDS:
    dwords_per_row = int(math.ceil(bits_per_row / 32.0));
    image_data_size = dwords_per_row * 4 * h;

    if image_data_size >= 0:
      image_data_offset = self._header._Offset.value;
      overlap_size = 0;
      if self.current_offset < image_data_offset:
        unused_size = image_data_offset - self.current_offset;
        self._unused_before_pixel_data = \
            self.Member(C.STRING, 'unused_before_pixel_data', unused_size);
        self._unused_before_pixel_data.warnings.append('unexpected unused data');
      else:
        self._unused_before_pixel_data = None;
        if image_data_offset < self.current_offset:
          overlap_size = self.current_offset - image_data_offset;
          previous_size = self.size;
          previous_offset = self.current_offset;
          previous_max_size = self.current_max_size;
          self.size -= overlap_size;
          self.current_offset -= overlap_size;
          self.current_max_size += overlap_size;
      image_size = self._bitmapinfo._header._SizeImage.value;
      if image_size == 0: # Unlikely: assume that everything is data.
        image_size = self.current_max_size;
      self._compressed_pixel_data = self.Member(C.STRING, 'pixel_data', \
          image_size);
      self._pixel_data = None;

      compression = self._bitmapinfo._header._Compression.value;
      if compression == 0: # None
        self._pixel_data = self._compressed_pixel_data;
      elif compression == 1: # RLE 8 bit
        self.DecodeRLE(8, self._compressed_pixel_data, w, h);
      elif compression == 2: # RLE 4 bit
        self.DecodeRLE(4, self._compressed_pixel_data, w, h);
      elif compression == 3: # Bit field
        pass;
      elif compression == 4: # JPEG
        pass;
      elif compression == 5: # PNG
        pass;
      
      if self._pixel_data is not None:
        self._pixel_data.notes.append('pixels = 0x%X|%d * %d bits' % \
            (w * h, w * h, bits_per_pixel));
      if overlap_size > 0:
        if previous_size > self.size:
          # this image overlaps and is small enough that it fits entirely in
          # the previous data; restore previous size, offset and max_size:
          self._compressed_pixel_data.warnings.append( \
              'image data overlaps previous data entirely');
          self.size = previous_size;
          self.current_offset = previous_offset;
          self.current_max_size = previous_max_size;
        else:
          self._compressed_pixel_data.warnings.append( \
              'image data overlaps 0x%X|%d bytes of previous data' % \
              (overlap_size, overlap_size));
    else:
      self.warnings.append('cannot show image pixel data because it is ' \
          'reported to have a negative size');
      self._pixel_data = None;

  def DecodeRLE(self, bits, data, w, h):
    assert bits in [4, 8], 'Only guaranteed to work for 4 and 8 bits';
    import C;
    x = 0; y = 0; index = 0;
#    max_x = 0; max_y = 0;
    data.ContainStream('');
    while index < len(data.value):
      length = ord(data.value[index]);
      index += 1;
      if index >= len(data.value):
        data.warnings.append('data stream ends unexpectedly at byte 0x%X|%d' % \
          (index, index));
        break;
      second_byte = ord(data.value[index]);
      index += 1;
      if length > 0:
        if bits == 4 and length % 2 == 1:
          data.warnings.append('data stream contains uneven run length, ' \
              'which is not supported - cannot decode data');
          break;
        data.ContainStream(chr(second_byte) * (length * bits / 8));
        x += length;
      elif second_byte in [0, 1]:
        scanline = data.ContainMember( \
            C.STRING, 'scanline_%d' % y, x * bits / 8);
        if x < w:
          scanline.warnings.append('scanline 0x%X|%d is 0x%X|%d pixels ' \
              'shorter than image is wide' % (y, y, w - x, w - x));
        elif x > w:
          scanline.warnings.append('scanline 0x%X|%d is 0x%X|%d pixels ' \
              'longer than image is wide' % (y, y, x - w, x - w));
        x = 0;
        y += 1;
        if second_byte == 1:
          break;
      elif second_byte == 2:
        data.warnings.append('data stream contains delta command, which ' \
            'is not supported - cannot decode data');
        break;
#        x += ord(data.value[index]);
#        index += 1;
#        if index >= len(data.value):
#          data.warnings.append('data stream ends unexpectedly at byte ' \
#              '0x%X|%d' % (index, index));
#          break;
#        y += ord(data.value[index]);
      else:
        if second_byte % 2 == 1:
          size = second_byte + 1;
        else:
          size = second_byte;
        data.ContainStream(data.value[index:index + size], size * bits / 8);
        index += size;
        x += size;
#      if x > max_x:
#        max_x = x;
#      if y > max_y:
#        max_y = y;
    else:
      data.warnings.append('data stream ends unexpectedly at byte 0x%X|%d' % \
          (index, index));
    if x > 0:
      scanline = data.ContainMember(C.STRING, 'scanline_%d' % y, x);
      scanline.warnings.append('no end of line marker found');

    data.notes.append('decoded to 0x%X|%d bytes' % \
        (data.contained_max_size, data.contained_max_size));
    off_by = index - len(data.value);
    if off_by < 0:
      data.warnings.append( \
          '0x%X|%d bytes of compressed data not used' % (off_by, off_by));

    if y < h:
      data.warnings.append( \
          'decoded image data is 0x%X|%d lines too short');
    elif y > h:
      data.warnings.append( \
          'decoded image data is 0x%X|%d lines too long');
