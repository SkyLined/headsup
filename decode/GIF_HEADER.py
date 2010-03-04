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

import C;

# http://www.w3.org/Graphics/GIF/spec-gif89a.txt
def GIF_HEADER(stream, offset, max_size, parent, name):
  result = C.STRUCT(stream, offset, max_size, parent, name, \
      'GIF_HEADER', \
      ('Signature',     {C.STRING: 3}),
      ('Version',       {C.STRING: 3}),
  );
  if result._Signature.value != 'GIF':
    result._Signature.warnings.append('expected value to be "GIF"');
  if result._Version.value not in ['87a', '89a']:
    result._Version.warnings.append('expected value to be "87a" or "89a"');

  return result;

