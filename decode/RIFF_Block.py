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

class RIFF_Block(Structure):
  type_name = 'RIFF_BLOCK';
  def __init__(self, stream, offset, max_size, parent, name, valid_block_names):
    import C;
    from RIFF_Chunk import RIFF_Chunk;
    from RIFF_ACON_Checks import RIFF_ACON_Checks;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._name = self.Member(C.STRING, 'name', 4);

    if valid_block_names is not None:
      if self._name.value not in valid_block_names:
        if len(valid_block_names) == 1:
          valid_block_names_string = valid_block_names[0];
        else:
          valid_block_names_string = \
            '", "'.join(valid_block_names[:-1]) + '" or "' + \
            valid_block_names[-1];
        self._name.warnings.append( \
            'expected value to be "%s"' % valid_block_names_string);
    else:
      self._name.notes.append('unknown/unexpected');

    if self._name.value == 'ACON':
      valid_chunk_names = {'anih': None, 'rate': None, \
          'LIST': ['fram', 'INFO'], 'INAM': None, 'IART': None};
    elif self._name.value == 'fram':
      valid_chunk_names = {'icon': None};
    elif self._name.value == 'INFO':
      valid_chunk_names = {'INAM': None, 'IART': None};
    else:
      valid_chunk_names = None;

    self._padding = [];
    self._chunks = [];
    self._named_chunks = {};
    while self.DataAvailable():
      chunk = self.Member(RIFF_Chunk, 'chunk_%d' % (len(self._chunks) + 1), \
          valid_chunk_names);
      self._chunks.append(chunk);
      if chunk._name.value not in self._named_chunks:
        self._named_chunks[chunk._name.value] = [chunk];
      else:
        self._named_chunks[chunk._name.value].append(chunk);

    if self._name.value == 'ACON':
      RIFF_ACON_Checks(self);
    self.notes.append( \
        '0x%X|%d chunks' % (len(self._chunks), len(self._chunks)));

    self.Unused();

