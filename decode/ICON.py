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

from Structure import Structure

class ICON(Structure):
  type_name = 'ICON'
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    from struct_ICONDIR import struct_ICONDIR;
    from struct_ICONDIRENTRY import struct_ICONDIRENTRY;
    from struct_ICONIMAGE import struct_ICONIMAGE;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    icon_start_offset = offset;

    self._icondir = self.Member(struct_ICONDIR, 'icondir');
    self._icondirentries = self.Member(C.ARRAY, 'icondirentries', \
        self._icondir._Count.value, struct_ICONDIRENTRY, \
        self._icondir._Type.value);

    self._images = [];
    self._unused = [];
    total_unused_size = 0;
    for icondirentry in self._icondirentries._items:
      image_offset = icon_start_offset + \
          icondirentry._ImageOffset.value;
      overlap_size = 0;
      if image_offset > self.current_offset and self.DataAvailable():
        # There is unused space between the image and the current offset:
        if image_offset > len(self.stream):
          # Image starts beyond end of stream, remaining stream is unused:
          unused_size = len(self.stream) - self.current_offset;
        else:
          # Image starts inside the stream, part of stream is unused:
          unused_size = image_offset - self.current_offset;
        unused = self.Member(C.STRING, 'unused', unused_size);
        total_unused_size += unused.size;
        self._unused.append(unused);
      elif image_offset < self.current_offset:
        # The image is expected to start before the current offset and overlaps
        # with previous data:
        overlap_size = self.current_offset - image_offset;
        # Remember current pointers and sizes:
        previous_size = self.size;
        previous_offset = self.current_offset;
        previous_max_size = self.current_max_size;
        # Back up the pointers and sizes according to the overlap:
        self.size -= overlap_size;
        self.current_offset -= overlap_size;
        self.current_max_size += overlap_size;
      if image_offset >= len(self.stream):
        icondirentry._ImageOffset.warnings.append( \
            'Offset is beyond end of stream');
      else:
        image = self.Member(struct_ICONIMAGE, \
            '%s_image_data' % icondirentry.name);
        self._images.append(image);
        if overlap_size > 0:
          if previous_size > self.size:
            # this image overlaps and is small enough that it fits entirely in
            # the previous data; restore previous size, offset and max_size:
            image.warnings.append('image data overlaps previous data entirely');
            self.size = previous_size;
            self.current_offset = previous_offset;
            self.current_max_size = previous_max_size;
          else:
            image.warnings.append( \
                'image data overlaps 0x%X|%d bytes of previous data' % \
                (overlap_size, overlap_size));
    if total_unused_size > 0:
      self.warnings.append('block contains a total of 0x%X|%d unused bytes' % \
          (total_unused_size, total_unused_size));
