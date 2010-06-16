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

# http://www.ietf.org/rfc/rfc1950.txt
class ZLIB_BLOCK(Structure):
  type_name = 'ZLIB_BLOCK';
  def __init__(self, stream, offset, max_size, parent, name):
    import zlib;
    import C;
    Structure.__init__(self, stream, offset, max_size, parent, \
        'compressed_' + name);

    self._header = self.Member(C.BITFIELD, 'header',
        ('FCHECK', 4),
        ('FDICT', 1),
        ('FLEVEL', 3),
        ('CM', 4),
        ('CINFO', 4),
    );
    if self._header._CM.value == 8:
      self._header._CM.notes.append('deflate');
      self._windows_size_base_2 = self._header._CINFO.value + 8;
      self._windows_size = 2 ** (self._header._CINFO.value + 8);
      if self._header._CINFO.value > 7:
        self._header._CINFO.warnings.append('expected value to be at most 7');
    elif self._header._CM.value == 15:
      self._header._CM.warnings.append('value is reserved');
      self._header._CINFO.notes.append('ignored');
    else:
      self._header._CM.warnings.append('expected value to be 8 (deflate)');
      self._header._CINFO.notes.append('ignored');

    # Calculate the 16-bit value of the flags:
    check_value = 0;
    for i in [self._header._CINFO, self._header._CM, self._header._FLEVEL, \
        self._header._FDICT, self._header._FCHECK]:
      check_value = check_value << i.size + i.value;
    # Check that FCHECK makes this 16-bit value a multiple of 31:
    if check_value % 31 != 0:
      expected_value = (check_value + 31 - check_value % 31) % 31;
      self._header._FCHECK.warnings.append( \
          'expected value to be %d' % expected_value);
    if self._header._FLEVEL.value == 1:
      self._header._FLEVEL.notes.append('fastest');
    elif self._header._FLEVEL.value == 2:
      self._header._FLEVEL.notes.append('fast');
    elif self._header._FLEVEL.value == 3:
      self._header._FLEVEL.notes.append('default');
    elif self._header._FLEVEL.value == 4:
      self._header._FLEVEL.notes.append('slowest');
    else:
      self._header._FLEVEL.notes.append('unknown');

    # Dictionary is optional
    if self._header._FDICT.value == 1:
      self._dictionary = self.Member(C.DWORD, 'DICTID');
    else:
      self._dictionary = None;

    self._compressed_data = self.Member(C.STRING, 'compressed_data', \
        self.current_max_size - 4);
    self._decompressed_data = None;
    try:
      # Implementing this for advanced error checking is not my priority, but
      # it may be useful at some point.
      self._decompressed_data = zlib.decompress(self.GetMaxStream());
    except Exception, e:
      self.ContainStream('decompressed_' + name, None, '', 0);
      self._compressed_data.warnings.append('cannot decode: %s' % e);
    else:
      self.ContainStream('decompressed_' + name, None, \
          self._decompressed_data, len(self._decompressed_data));
    
    self._ADLER32 = self.Member(C.DWORD, 'ADLER32', little_endian = False);

    if self._decompressed_data:
      s1 = 1; s2 = 0;
      for char in self._decompressed_data:
        s1 = (s1 + ord(char)) % 65521;
        s2 = (s2 + s1) % 65521;
      adler32 = s2 * 65536 + s1;
      if adler32 != self._ADLER32.value:
        self._ADLER32.warnings.append( \
            'expected value to be 0x%X|%d' % (adler32, adler32));
