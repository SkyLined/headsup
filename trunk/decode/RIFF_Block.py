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
  def __init__(self, stream, offset, max_size, parent, name, valid_blocks):
    import C;
    from RIFF_Chunk import RIFF_Chunk;
    from RIFF_ACON_Checks import RIFF_ACON_Checks;
    from RIFF_WAVE_Checks import RIFF_WAVE_Checks;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._name = self.Member(C.STRING, 'name', 4);

    valid_chunk_names = None;
    if valid_blocks is not None:
      valid_block_names = valid_blocks.keys();
      if self._name.value in valid_block_names:
        valid_chunk_names = valid_blocks[self._name.value];
      else:
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

    self._padding = [];
    self._chunks = [];
    self._named_chunks = {};
    while self.DataAvailable():
      chunk = self.Member(RIFF_Chunk, 'chunk_%d' % (len(self._chunks) + 1), \
          valid_chunk_names);
      self._chunks.append(chunk);
      off_by = self.current_offset - chunk.expected_end_offset;
      if self.DataAvailable() and off_by > 0:
        # The RIFF_Block that is contained in this RIFF_Chunk was larger than
        # expected and our offset and max_size reflect this.This means the
        # current_offset now points inside the next RIFF_Chunk and not to the
        # start of it. We need to move the offset back to where the next
        # RIFF_Chunk is expected to start and update the max_size as well:
        self.current_offset -= off_by;
        self.current_max_size += off_by;

      if chunk._name.value not in self._named_chunks:
        self._named_chunks[chunk._name.value] = [chunk];
      else:
        self._named_chunks[chunk._name.value].append(chunk);

    if self._name.value == 'ACON':
      RIFF_ACON_Checks(self);
    elif self._name.value == 'WAVE':
      RIFF_WAVE_Checks(self);
    self.notes.append( \
        '0x%X|%d chunks' % (len(self._chunks), len(self._chunks)));

    chunks_format_details = {};
    for chunk in self._chunks:
      if chunk.format_details not in chunks_format_details:
        chunks_format_details[chunk.format_details] = 1;
      else:
        chunks_format_details[chunk.format_details] += 1;
    keys = chunks_format_details.keys();
    keys.sort();
    details = [];
    for key in keys:
      if chunks_format_details[key] == 1:
        details.append(key);
      else:
        details.append('%d * %s' % (chunks_format_details[key], key));
    self.format_details = '%s(%s)' % \
        (self._name.value, ', '.join(details));

    self.Unused();

