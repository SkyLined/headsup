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


# http://msdn.microsoft.com/en-us/library/ms997538.aspx
def struct_ICONDIR(stream, offset, max_size, parent, name):
  import C;
  result = C.STRUCT(stream, offset, max_size, parent, name, \
      'ICONDIR', \
      ('Reserved',        C.WORD),   # idReserved
      ('Type',            C.WORD),   # idType (1=.ICO, 2=.CUR)
      ('Count',           C.WORD),   # idCount (number of images)
  );
  format_details = [];
  if result._Reserved.value != 0:
    result._Reserved.warnings.append('expected value to be 0');
  if result._Type.value not in [1, 2]:
    result._Type.warnings.append('expected value to be 1 or 2');
    format_details.append('unknown');
  else:
    result._Type.notes.append({1:'ICON', 2:'CURSOR'}[result._Type.value]);
    format_details.append({1:'icon', 2:'cursor'}[result._Type.value]);
  if result._Count.value == 0:
    result._Count.warnings.append('expected at least one image');

  result.format_details = ', '.join(format_details);
  return result;
