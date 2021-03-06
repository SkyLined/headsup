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


# http://en.wikipedia.org/wiki/BMP_file_format
def struct_BMPHEADER(stream, offset, max_size, parent, name):
  import C;
  result = C.STRUCT(stream, offset, max_size, parent, name, \
      'BMPHEADER', \
      ('MagicNumber',       {C.STRING: 2}),
      ('FileSize',          C.DWORD),
      ('Reserved',          {C.ARRAY: (2, C.WORD)}),
      ('Offset',            C.DWORD),
  );
  if result._MagicNumber.value not in ["BM", "BA", "CI", "CP", "IC", "PT"]:
    result._MagicNumber.warnings.append('invalid magic number');

  return result;