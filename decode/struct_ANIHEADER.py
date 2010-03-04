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


# http://www.gdgsoft.com/anituner/help/aniformat.htm
def struct_ANIHEADER(stream, offset, max_size, parent, name):
  import C;
  result = C.STRUCT(stream, offset, max_size, parent, name, 'ANIHEADER', \
      ('Size',      C.DWORD),    # length of structure, to be set later.
      ('Frames',    C.DWORD),    # cFrames
      ('Steps',     C.DWORD),    # cSteps
      ('X',         C.DWORD),    # cx (must be 0)
      ('Y',         C.DWORD),    # cy (must be 0)
      ('BitCount',  C.DWORD),    # cBitCount
      ('Planes',    C.DWORD),    # cPlanes
      ('JifRate',   C.DWORD),    # JifRate
      ('Flags',     C.DWORD),    # flags (1 = AF_ICON
  );
  max_size -= result.size;
  if result._Size.value != result.size:
    if result._Size.value > 1000 * 1000:
      result._Size.warnings.append( \
          'value is large, expected value to be %d' % result.size);
    else:
      result._Size.warnings.append('expected value to be %d' % result.size);
  if result._Frames.value == 0:
    result._Frames.warnings.append('expected at least 1 frame');
  elif result._Frames.value > 100:
    result._Frames.warnings.append('value is large');
  if result._Steps.value == 0:
    result._Steps.warnings.append('expected at least 1 step');
  elif result._Steps.value > 100:
    result._Steps.warnings.append('value is large');
  # These are reported to be "reserved, must be 0" but it is set to the W*H size
  # of the icons in some valid ani cursors... so ignoring this check.
#  if result._X.value != 0:
#    result._X.warnings.append('expected value to be 0');
  if result._X.value > 100:
    result._X.warnings.append('value is large');
#  if result._Y.value != 0:
#    result._Y.warnings.append('expected value to be 0');
  if result._Y.value > 100:
    result._Y.warnings.append('value is large');
  if result._BitCount.value > 100:
    result._BitCount.warnings.append('value is large');
  if result._Planes.value > 100:
    result._Planes.warnings.append('value is large');
  if result._JifRate.value > 100:
    result._JifRate.warnings.append('value is large');
  if result._Flags.value != 1:
    result._Flags.warnings.append('expected value to be 1 (AF_ICON)');
  else:
    result._Flags.notes.append('AF_ICON');
  return result;

