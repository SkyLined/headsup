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

class RIFF_Chunk(Structure):
  type_name = 'RIFF_CHUNK';
  def __init__(self, stream, offset, max_size, parent, name, valid_chunks):
    import C;
    from RIFF_Block import RIFF_Block;
    from RIFF_ACON_anih import RIFF_ACON_anih;
    from RIFF_ACON_fram_icon import RIFF_ACON_fram_icon;
    from RIFF_ACON_rate import RIFF_ACON_rate;
    from RIFF_ACON_seq import RIFF_ACON_seq;
    from RIFF_WAVE_fmt import RIFF_WAVE_fmt;
    from RIFF_WAVE_fact import RIFF_WAVE_fact;
    from RIFF_WAVE_cue import RIFF_WAVE_cue;
    from RIFF_WAVE_PEAK import RIFF_WAVE_PEAK;
    from RIFF_WAVE_DISP import RIFF_WAVE_DISP;
    from RIFF_WAVE_adtl_labl import RIFF_WAVE_adtl_labl;
    from RIFF_WAVE_adtl_note import RIFF_WAVE_adtl_note;
    from RIFF_WAVE_adtl_ltxt import RIFF_WAVE_adtl_ltxt;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._name = self.Member(C.STRING, 'name', 4);
    
    valid_blocks = None;
    if valid_chunks is not None:
      valid_chunk_names = valid_chunks.keys();
      if self._name.value not in valid_chunk_names:
        if len(valid_chunks) == 1:
          valid_chunk_names_string = valid_chunk_names[0];
        else:
          valid_chunk_names_string = \
            '", "'.join(valid_chunk_names[:-1]) + '" or "' + \
            valid_chunk_names[-1];
        self._name.warnings.append( \
            'expected value to be "%s"' % valid_chunk_names_string);
      else:
        valid_blocks = valid_chunks[self._name.value];
    else:
      self._name.notes.append('unknown/unexpected');

    self._size = self.Member(C.DWORD, 'size');

    padding_bytes = self._size.value % 2;
    if padding_bytes:
      self._size.notes.append('+1 byte padding');

    max_data_size = self._size.value;
    self.expected_end_offset = \
        self.current_offset + self._size.value + padding_bytes;
    self._size.notes.append(
        'end offset: %X' % self.expected_end_offset);
    original_max_size = self.current_max_size;
    if self.current_max_size > max_data_size:
      size_reduction = self.current_max_size - max_data_size;
      self.current_max_size = max_data_size;
    else:
      size_reduction = 0;

    if self._name.value in ['RIFF', 'LIST']:
      self._blocks = [];
      self._named_blocks = {};
      while self.DataAvailable():
        block = self.Member(RIFF_Block, 'block_%d' % (len(self._blocks) + 1), \
            valid_blocks);
        self._blocks.append(block);
        if block._name.value not in self._named_blocks:
          self._named_blocks[block._name.value] = [block];
        else:
          self._named_blocks[block._name.value].append(block);
      self.notes.append('0x%X|%d blocks' % \
          (len(self._blocks), len(self._blocks)));

      blocks_format_details = {};
      for block in self._blocks:
        if block.format_details not in blocks_format_details:
          blocks_format_details[block.format_details] = 1;
        else:
          blocks_format_details[block.format_details] += 1;
      keys = blocks_format_details.keys();
      keys.sort();
      details = [];
      for key in keys:
        if blocks_format_details[key] == 1:
          details.append(key);
        else:
          details.append('%d * %s' % (blocks_format_details[key], key));
      self.format_details = '%s(%s)' % \
          (self._name.value, ', '.join(details));
  
    elif self._name.value == 'INAM':
      self._data = self.Member(C.STRING, 'Title/name', max_data_size);
      self.format_details = self._name.value;
    elif self._name.value == 'IART':
      self._data = self.Member(C.STRING, 'Author/artist', max_data_size);
      self.format_details = self._name.value;
    elif self._name.value == 'ICRD':
      self._data = self.Member(C.STRING, 'Creation data', max_data_size);
      self.format_details = self._name.value;
    elif self._name.value == 'ISFT':
      self._data = self.Member(C.STRING, 'Software', max_data_size);
      self.format_details = self._name.value;
    elif self._name.value == 'ICMT':
      self._data = self.Member(C.STRING, 'Comment', max_data_size);
      self.format_details = self._name.value;
    elif self._name.value == 'anih' and parent._name.value == 'ACON':
      self._data = self.Member(RIFF_ACON_anih, 'data');
      self.format_details = self._data.format_details;
    elif self._name.value == 'rate' and parent._name.value == 'ACON':
      self._data = self.Member(RIFF_ACON_rate, 'data');
      self.format_details = self._data.format_details;
    elif self._name.value == 'seq ' and parent._name.value == 'ACON':
      self._data = self.Member(RIFF_ACON_seq, 'data');
      self.format_details = self._data.format_details;
    elif self._name.value == 'icon' and parent._name.value == 'fram':
      self._data = self.Member(RIFF_ACON_fram_icon, 'data');
      self.format_details = self._data.format_details;
    elif self._name.value == 'fmt ' and parent._name.value == 'WAVE':
      self._data = self.Member(RIFF_WAVE_fmt, 'data');
      self.format_details = self._data.format_details;
    elif self._name.value == 'fact' and parent._name.value == 'WAVE':
      self._data = self.Member(RIFF_WAVE_fact, 'data');
      self.format_details = self._data.format_details;
    elif self._name.value == 'data' and parent._name.value == 'WAVE':
      self._data = self.Member(C.STRING, 'data', max_data_size);
      self.format_details = self._name.value;
    elif self._name.value == 'cue ' and parent._name.value == 'WAVE':
      self._data = self.Member(RIFF_WAVE_cue, 'data');
      self.format_details = self._data.format_details;
    elif self._name.value == 'PEAK' and parent._name.value == 'WAVE':
      self._data = self.Member(RIFF_WAVE_PEAK, 'data');
      self.format_details = self._data.format_details;
    elif self._name.value in ['JUNK', 'PAD '] and parent._name.value == 'WAVE':
      self._data = self.Member(C.STRING, 'data', max_data_size);
      self._data.notes.append('ignored');
      self.format_details = self._name.value;
    elif self._name.value == 'DISP' and parent._name.value == 'WAVE':
      self._data = self.Member(RIFF_WAVE_DISP, 'data');
      self.format_details = self._data.format_details;
    elif self._name.value == 'PEAK' and parent._name.value == 'WAVE':
      self._data = self.Member(RIFF_WAVE_PEAK, 'data');
      self.format_details = self._data.format_details;
    elif self._name.value == 'labl' and parent._name.value == 'adtl':
      self._data = self.Member(RIFF_WAVE_adtl_labl, 'data');
      self.format_details = self._data.format_details;
    elif self._name.value == 'note' and parent._name.value == 'adtl':
      self._data = self.Member(RIFF_WAVE_adtl_note, 'data');
      self.format_details = self._data.format_details;
    elif self._name.value == 'ltxt' and parent._name.value == 'adtl':
      self._data = self.Member(RIFF_WAVE_adtl_ltxt, 'data');
      self.format_details = self._data.format_details;
    else:
      self._name.warnings.append('unknown type of chunk');
      self._data = self.Member(C.STRING, 'data', max_data_size);
      self.format_details = self._name.value.strip();

    assert padding_bytes in [0,1], \
        'Expected 0 or 1 padding bytes, found %s!?' % padding_bytes;
    if padding_bytes == 1:
      if size_reduction > 0 and self.current_max_size == 0:
        self.current_max_size += 1;
      assert self.current_max_size > 0, '%d' % self.current_max_size;
      self._padding = self.Member(C.BYTE, 'padding');
      if self._padding.value != 0:
        self._padding.warnings.append('expected value to be 0');

    self.Unused();
