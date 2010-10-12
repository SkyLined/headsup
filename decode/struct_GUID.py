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

KNOWN_GUIDS = {
  '{00000000-0000-0000-C000-000000000046}': 'IUnknown',
  '{00020400-0000-0000-C000-000000000046}': 'IDispatch',
}
KNOWN_TYPE_VARIANTS = {
  0: 'Network Computing System',
  2: 'Standard',
  6: 'MS COM',
  7: 'Reserved',
};


# https://secure.wikimedia.org/wikipedia/en/wiki/Globally_unique_identifier
def struct_GUID(stream, offset, max_size, parent, name):
  import C;
  result = C.STRUCT(stream, offset, max_size, parent, name, 'GUID', \
      ('Data1',     C.DWORD),
      ('Data2',     C.WORD),
      ('Data3',     C.WORD),
      ('Data4',     {C.ARRAY: (8, C.BYTE)}),
  );
  result.dump_simplified = True;
  result.string_value = '{%08X-%04X-%04X-%02X%02X-%02X%02X%02X%02X%02X%02X}' % \
      (result._Data1.value, result._Data2.value, result._Data3.value,
      result._Data4._values[0], result._Data4._values[1],
      result._Data4._values[2], result._Data4._values[3],
      result._Data4._values[4], result._Data4._values[5],
      result._Data4._values[6], result._Data4._values[7]);
  result.notes.append(result.string_value);
  if result.string_value in KNOWN_GUIDS:
    result.notes.append('(%s)' % KNOWN_GUIDS[result.string_value]);
  
  type_variant = result._Data4._values[1] >> 5; # Upper 3 bits
  if type_variant in KNOWN_TYPE_VARIANTS:
    result.notes.append('type=%s' % KNOWN_TYPE_VARIANTS[type_variant]);
  else:
    result.warnings.append(
        'Unknown type variant in Data4 byte 2 upper 3 bits: %d' % type_variant);
  version = result._Data3.value >> 12; # Upper 4 bits.
  if version == 0:
    pass; # Nothing specified; ignored.
  elif version in [1,4]:
    result.notes.append('version=%d' % version);
  else:
    result.warnings.append(
        'Unknown version in Data3 upper 4 bits: %d (expected 0, 1 or 4)' % \
        version);
  return result;