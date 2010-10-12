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

def x(object):
  pass;
function_type = type(x);
class x(object):
  pass;
class_type = type(x);

class STRUCT(Structure):
  def __init__(self, stream, offset, max_size, parent, name, struct_name, \
      *member_definitions):
    self.type_name = 'struct ' + struct_name;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    for member_name, member_type in member_definitions:
      if type(member_type) == dict:
        member_creator, creator_args = member_type.items()[0];
        if type(creator_args) != list and type(creator_args) != tuple:
          creator_args = [creator_args];
      elif type(member_type) == function_type or type(member_type) == class_type:
        member_creator = member_type;
        creator_args = [];
      else:
        raise AssertionError('Unknown member type %s' % repr(member_type));
      member = self.Member(member_creator, member_name, *creator_args);
      setattr(self, '_' + member_name, member);

    self.notes.append('0x%X|%d members' % (len(self.value), len(self.value)));


class BITFIELD_COMPONENT(Structure):
  type_name = 'BITFIELD_COMPONENT';
  def __init__(self, stream, offset, max_size, parent, name, \
      bit_offset, bit_size, value):
    Structure.__init__(self, stream, offset, max_size, parent, name);
    self.dump_simplified = True;

    self.value = value;
    self.bit_offset = bit_offset;
    self.bit_size = bit_size;

  def SimplifiedValue(self, header = None):
    bits = '';
    for i in range(self.bit_size):
      bits = {True:'1', False:'0'}[self.value & (1 << i) > 0] + bits;

    if self.bit_size == 1:
      result = 'bit %d: %d' % (self.bit_offset + 1, self.value);
    else:
      bit_values = 'b|0x%X|%d' % (self.value, self.value);
      for i in range(self.bit_size):
        if self.value & (1 << i):
          bit_values = '1' + bit_values;
        else:
          bit_values = '0' + bit_values;
      bits = 'bits %d-%d (%d bits)' % \
          (self.bit_offset + 1, self.bit_offset + self.bit_size, self.bit_size);
      result = '%s: %s' % (bits, bit_values);
    return result;

class BITFIELD(Structure):
  type_name = 'BITFIELD';
  def __init__(self, stream, offset, max_size, parent, name, \
      *component_definitions):
    Structure.__init__(self, stream, offset, max_size, parent, name);

    size_in_bits = 0;
    for component_name, component_bits in component_definitions:
      size_in_bits += component_bits;
    assert size_in_bits % 8 == 0, \
        'BITFIELD "%s" total size is %d bits, which is not BYTE alligned' % \
        (name, size_in_bits);
    self.size = size_in_bits / 8;
    self.bits = []; # LSB to MSB
    self.bytes = []; # LSB to MSB
    for i in range(self.size - 1, -1, -1):
      if self.current_offset + i < len(stream):
        byte = ord(stream[self.current_offset + i]);
      else:
        byte = 0;
      self.bytes.append(byte);
      for j in range(8):
        bit = {True: 1, False: 0}[byte & (1 << j) > 0];
        self.bits.append(bit);
    bit_offset = 0;
    for component_name, component_bits in component_definitions:
      value = 0;
      for i in range(component_bits):
        value += self.bits[bit_offset + i] << i;
      component = BITFIELD_COMPONENT(self.stream, offset, max_size, \
          self, component_name, bit_offset, component_bits, value);
      self.value.append(component);
      bit_offset += component_bits;
      setattr(self, '_' + component_name, component);
    self.notes.append('0x%X|%d components (ordered LSB to MSB)' % \
        (len(component_definitions), len(component_definitions)));

    self.current_offset += self.size;
    self.current_max_size -= self.size;

  def SimplifiedValues(self, header = None):
    results = [];
    for component in self.value:
      if component.value != 0:
        results.append('%s (%s)' % (component.name, component.SimplifiedValue()));
    if len(results) == 0:
      return ['No bits set'];
    else:
      return results;

class ARRAY(Structure):
  type_name = 'ARRAY';
  def __init__(self, stream, offset, max_size, parent, name, items_count, \
      item_creator, *item_creator_args, **nitem_creator_args):
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._values = [];
    self._items = [];

    i = 0;
    while i < items_count: # and self.DataAvailable(1) 
      item_name = '%s[0x%X|%d]' % (name, i, i);
      item = self.Member(item_creator, item_name, *item_creator_args, \
          **nitem_creator_args);
      self._items.append(item);
      self._values.append(item.value);
      i += 1;
    self.notes.append('0x%X|%d items' % (items_count, items_count));

class UnsignedInteger(Structure):
  def __init__(self, stream, offset, max_size, parent, name, size, \
      little_endian = True):
    Structure.__init__(self, stream, offset, max_size, parent, name);
    self.dump_simplified = True;

    self.size = size;
    self.current_offset = offset + size;
    self.current_max_size = max_size - size;

    available_stream_size = len(stream) - offset;
    if available_stream_size > size:
      available_stream_size = size;

    self.value = 0;
    if little_endian:
      for i in range(available_stream_size):
        self.value |= ord(stream[offset + i]) << (8 * i);
    else:
      for i in range(available_stream_size):
        self.value |= ord(stream[offset + i]) << (8 * (self.size - i - 1));

  def SimplifiedValue(self, header = None):
    if self.value < 0:
      fmtstr = '-0x%0' + str(self.size * 2) + 'X|%d';
      value = fmtstr % (-self.value, self.value);
    else:
      fmtstr = '0x%0' + str(self.size * 2) + 'X|%d';
      value = fmtstr % (self.value, self.value);
    return '%s: %s' % (self.type_name, value);

class SignedInteger(UnsignedInteger):
  def __init__(self, stream, offset, max_size, parent, name, size, \
      little_endian = True):
    UnsignedInteger.__init__(self, stream, offset, max_size, parent, name, \
        size, little_endian);
    self.uvalue = self.value;
    if self.size and self.value:
      negative_value = (1 << (8 * size - 1)); # 0x80, 0x80000, etc...
      if self.value >= negative_value:
        self.value -= negative_value * 2;     # 0x100, 0x100000, etc...

class QWORD(UnsignedInteger):
  type_name = 'QWORD';
  def __init__(self, stream, offset, max_size, parent, name, little_endian=True):
    UnsignedInteger.__init__(self, stream, offset, max_size, parent, name, 8, \
        little_endian);
class DWORD(UnsignedInteger):
  type_name = 'DWORD';
  def __init__(self, stream, offset, max_size, parent, name, little_endian=True):
    UnsignedInteger.__init__(self, stream, offset, max_size, parent, name, 4, \
        little_endian);
class WORD(UnsignedInteger):
  type_name = 'WORD';
  def __init__(self, stream, offset, max_size, parent, name, little_endian=True):
    UnsignedInteger.__init__(self, stream, offset, max_size, parent, name, 2, \
        little_endian);
class BYTE(UnsignedInteger):
  type_name = 'BYTE';
  def __init__(self, stream, offset, max_size, parent, name):
    UnsignedInteger.__init__(self, stream, offset, max_size, parent, name, 1);

class UINT64(UnsignedInteger):
  type_name = 'UINT64';
  def __init__(self, stream, offset, max_size, parent, name, little_endian=True):
    UnsignedInteger.__init__(self, stream, offset, max_size, parent, name, 8, \
        little_endian);
class UINT(UnsignedInteger):
  type_name = 'UINT';
  def __init__(self, stream, offset, max_size, parent, name, little_endian=True):
    UnsignedInteger.__init__(self, stream, offset, max_size, parent, name, 4, \
        little_endian);
class ULONG(UnsignedInteger):
  type_name = 'ULONG';
  def __init__(self, stream, offset, max_size, parent, name, little_endian=True):
    UnsignedInteger.__init__(self, stream, offset, max_size, parent, name, 4, \
        little_endian);
class USHORT(UnsignedInteger):
  type_name = 'USHORT';
  def __init__(self, stream, offset, max_size, parent, name, little_endian=True):
    UnsignedInteger.__init__(self, stream, offset, max_size, parent, name, 2, \
        little_endian);
class UCHAR(UnsignedInteger):
  type_name = 'UCHAR';
  def __init__(self, stream, offset, max_size, parent, name):
    UnsignedInteger.__init__(self, stream, offset, max_size, parent, name, 1);

class INT64(SignedInteger):
  type_name = 'INT64';
  def __init__(self, stream, offset, max_size, parent, name, little_endian=True):
    SignedInteger.__init__(self, stream, offset, max_size, parent, name, 8, \
        little_endian);
class INT(SignedInteger):
  type_name = 'INT';
  def __init__(self, stream, offset, max_size, parent, name, little_endian=True):
    SignedInteger.__init__(self, stream, offset, max_size, parent, name, 4, \
        little_endian);
class LONG(SignedInteger):
  type_name = 'LONG';
  def __init__(self, stream, offset, max_size, parent, name, little_endian=True):
    SignedInteger.__init__(self, stream, offset, max_size, parent, name, 4, \
        little_endian);
class SHORT(SignedInteger):
  type_name = 'SHORT';
  def __init__(self, stream, offset, max_size, parent, name, little_endian=True):
    SignedInteger.__init__(self, stream, offset, max_size, parent, name, 2, \
        little_endian);
class CHAR(SignedInteger):
  type_name = 'CHAR';
  def __init__(self, stream, offset, max_size, parent, name):
    SignedInteger.__init__(self, stream, offset, max_size, parent, name, 1);

class STRING(Structure):
  type_name = 'string';
  def __init__(self, stream, offset, max_size, parent, name, size = None):
    Structure.__init__(self, stream, offset, max_size, parent, name);
    self.dump_simplified = True;

    available_stream_size = len(stream) - offset;
    if available_stream_size >= 0:
      available_stream = stream[offset:];
      if size is None:
        # No size means NULL terminated; find NULL:
        self.size = available_stream.find('\0') + 1;
        if self.size == 0:
          # No NULL found means string not terminated:
          self.size = len(available_stream); # treat entire stream as string
          self.warnings.append( \
              'string is not NULL terminated and ends beyond end of stream');
      else:
        self.size = size;
      self.value = available_stream[:self.size];
      self.current_offset += self.size;
      self.current_max_size -= self.size;
    else:
      self.value = '';

  def SimplifiedValue(self, header = None):
    value = repr(self.value);
    if len(value) > 50:
      value = value[:50] + '...' + value[-1];
    return 'string(0x%X|%d bytes): %s' % \
        (self.size, self.size, value);

class UNICODE_STRING(Structure):
  type_name = 'unicode_string';
  def __init__(self, stream, offset, max_size, parent, name, size = None):
    Structure.__init__(self, stream, offset, max_size, parent, name);
    self.dump_simplified = True;

    available_stream_size = len(stream) - offset;
    if available_stream_size >= 0:
      available_stream = stream[offset:];
      if size is None:
        # No size means NULL terminated; find NULL:
        self.size = 0;
        for i in range(0, len(available_stream), 2):
          if available_stream[i:i+2] == '\0\0':
            self.size = i + 2;
            break;
        if self.size == 0:
          # No NULL found means string not terminated:
          self.size = len(available_stream) / 2; # treat entire stream as string
          self.warnings.append( \
              'string is not NULL terminated and ends beyond end of stream');
      else:
        self.size = size;
      if self.size % 2 == 1:
        self.warnings.append('Expected size to be even');
      self.value = u'';
      for i in range(0, self.size / 2):
        char_code_low = 0;
        char_code_high = 0;
        if i * 2 < len(available_stream):
          char_code_low = ord(available_stream[i * 2]);
          if i * 2 + 1 < len(available_stream):
            char_code_high = ord(available_stream[i * 2 + 1]);
        char_code = (char_code_high << 8) + char_code_low;
        self.value += unichr(char_code);
      self.current_offset += self.size;
      self.current_max_size -= self.size;
    else:
      self.value = '';

  def SimplifiedValue(self, header = None):
    value = repr(self.value);
    if len(value) > 50:
      value = value[:50] + '...' + value[-1];
    return 'unicode_string(0x%X|%d bytes): %s' % \
        (self.size * 2, self.size * 2, value);

class FLOAT32(Structure):
  type_name = 'float32';
  def __init__(self, stream, offset, max_size, parent, name, \
      little_endian=True):
    Structure.__init__(self, stream, offset, max_size, parent, name);
    self.dump_simplified = True;

    self.size = 4;
    self.current_offset = offset + self.size;
    self.current_max_size = max_size - self.size;

    available_stream_size = len(stream) - offset;
    if available_stream_size > self.size:
      available_stream_size = self.size;

    value = 0;
    if little_endian:
      for i in range(available_stream_size):
        value |= ord(stream[offset + i]) << (8 * i);
    else:
      for i in range(available_stream_size):
        value |= ord(stream[offset + i]) << (8 * (self.size - i - 1));

    self.sign_bit = value >> 31;
    self.exponent_bits = (value >> 22) & 0xFF;
    self.significant_bits = value & 0x7FFFFF;
    self.sign = {0:'+', 1:'-'}[self.sign_bit];
    sign_multiplier = {0:1, 1:-1}[self.sign_bit];
    if self.exponent_bits == 0xFF:
      self.isInfinity = True;
      if self.fraction_bits != 0:
        self.warnings.append( \
            'expect fraction bits to be 0, found 0x%X' % self.fraction_bits);
      self.value = sign_multiplier * float('inf');
    else:
      self.isInfinity = False;
      self.exponent = self.exponent_bits - 127;
      significant = self.significant_bits;
      if self.exponent_bits != 0:
        significant += 0x800000;
      self.fraction = 0.0;
      for bit_number in range(0, 23):
        bit_index = 22 - bit_number;
        bit_significant_value = 2 ** bit_index;
        bit_fraction_value = 1.0 / 2 ** bit_number;
        if significant & bit_significant_value:
          self.fraction += bit_fraction_value;
      self.value = sign_multiplier * self.fraction * (2 ** self.exponent);

  def SimplifiedValue(self, header = None):
    bits = '%1X %02X %06X' % \
        (self.sign_bit, self.exponent_bits, self.significant_bits);
    if self.isInfinity:
      return self.sign + 'Infinity (%s)' % bits;
    sign_multiplier = {0:1, 1:-1}[self.sign_bit];
    return '%s (%s: %s * 2^%s)' % \
        (self.value, bits, sign_multiplier * self.fraction, self.exponent);
