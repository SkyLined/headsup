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

class LZW_compressed_data(Structure):
  type_name = 'LZW_COMPRESSED_DATA';
  def __init__(self, stream, offset, max_size, parent, name, \
      minimum_code_size, little_endian = True, extra_slots = 0):
    import C;
    Structure.__init__(self, stream, offset, max_size, parent, 
        'compressed_' + name);
    self.dump_simplified = True;

    self.ContainStream('decompressed_' + name, 'compressed_' + name, '', 0);
    if minimum_code_size == 0:
      self.warnings.append('invalid minimum code size for lzw decompression');
    else:
      if minimum_code_size > 12:
        self.warnings.append('minimum code size is %d bits' % minimum_code_size);
      buffer = 0;
      buffer_bit_count = 0;
      current_code_bit_count = minimum_code_size + 1;
      max_code_bit_count = current_code_bit_count;
      clear_code = 1 << minimum_code_size;
      end_code = clear_code + 1;
      new_codes = clear_code + 2;
  
      self._little_endian = little_endian; # Gif:True, Tiff: True/False
      self._extra_slots = extra_slots;     # Gif:0, Tiff:1
  
      suffix = {};
      prefix = {};
  
      slot = new_codes;
      oc = -1;
      fc = -1;
  
      self._used_bytes = 0;
      while self.DataAvailable():
        # Fill our buffer with bits until we have enough for a code:
        while buffer_bit_count < current_code_bit_count \
            and self.DataAvailable():
          self._used_bytes += 1;
          data = self.Member(C.BYTE, 'data_%d' % self._used_bytes);
          if little_endian:
            buffer |= data.value << buffer_bit_count;
          else:
            buffer = buffer << 8 | data.value;
          buffer_bit_count += 8;
        if buffer_bit_count < current_code_bit_count:
          self.warnings.append('data is not properly terminated');
          break;
        # Get a code from our buffer:
        buffer_bit_count -= current_code_bit_count;
        if(little_endian):
          # Use the LSBs
          current_code_bit_mask = (2 ** current_code_bit_count - 1);
          code = buffer & current_code_bit_mask;
          # Keep only the MSBs
          buffer >>= current_code_bit_count;
        else:
          # Use the MSBs
          code = buffer >> buffer_bit_count; # No need to &
          # Keep only the LSBs
          remaining_buffer_mask = (2 ** buffer_bit_count - 1);
          buffer &= remaining_buffer_mask;
        # ...
        if code == end_code:
          break;
        if code == clear_code:
          current_code_bit_count = minimum_code_size + 1;
          slot = new_codes;
          fc = None;
          oc = None;
        else:
          original_code = code;
          if code == slot and fc is not None:
            self.ContainStream('decompressed_' + name, \
                'compressed_' + name, chr(fc), 1);
            code = oc;
          elif code >= slot:
            self.warnings.append( \
                'code 0x%X > slot (0x%X) causes error' % (code, slot));
            break;
          while code >= new_codes:
            self.ContainStream('decompressed_' + name, 'compressed_' + name, \
                chr(suffix[code]), 1);
            code = prefix[code];
          if code > 0xFF:
            self.warnings.append('code 0x%X > 0xFF causes error' % code);
            break;
          self.ContainStream('decompressed_' + name, 'compressed_' + name, \
              chr(code), 1);
          if slot < (1 << current_code_bit_count) and oc is not None:
            suffix[slot] = code;
            prefix[slot] = oc;
            slot += 1;
          fc = code;
          oc = original_code;
          if slot >= (1 << current_code_bit_count) - extra_slots:
            current_code_bit_count += 1;
            if current_code_bit_count > max_code_bit_count:
              max_code_bit_count = current_code_bit_count;
      else:
        self.warnings.append('data is not properly terminated');

      if max_code_bit_count > 12:
        self.warnings.append('codes are up to %d bits' % max_code_bit_count);
      else:
        self.notes.append('codes are up to %d bits' % max_code_bit_count);

    self.Unused();

  def SimplifiedValue(self, header = None):
    return '%s (0x%X|%d bytes)' % \
        (self.type_name, self._used_bytes, self._used_bytes);
