from Structure import Structure

class RIFF_Chunk(Structure):
  type_name = 'RIFF_CHUNK';
  def __init__(self, stream, offset, max_size, parent, name, valid_chunk_names):
    import C;
    from RIFF_Block import RIFF_Block;
    from RIFF_anih import RIFF_anih;
    from RIFF_icon import RIFF_icon;
    from RIFF_fmt import RIFF_fmt;
    from RIFF_rate import RIFF_rate;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._name = self.Member(C.STRING, 'name', 4);
    
    if valid_chunk_names is not None:
      if self._name.value not in valid_chunk_names:
        if len(valid_chunk_names) == 1:
          valid_chunk_names_string = valid_chunk_names.keys()[0];
        else:
          valid_chunk_names_string = \
            '", "'.join(valid_chunk_names.keys()[:-1]) + '" or "' + \
            valid_chunk_names.keys()[-1];
        self._name.warnings.append( \
            'expected value to be "%s"' % valid_chunk_names_string);
        valid_block_names = None;
      else:
        valid_block_names = valid_chunk_names[self._name.value];
    else:
      self._name.notes.append('unknown/unexpected');

    self._size = self.Member(C.DWORD, 'size');

    max_data_size = self._size.value;
    original_max_size = self.current_max_size;
    if self.current_max_size > max_data_size:
      self.current_max_size = max_data_size;
      unused_data_size = max_data_size % 2;
    else:
      unused_data_size = 0;

    if self._name.value in ['RIFF', 'LIST']:
      self._blocks = [];
      self._named_blocks = {};
      while self.DataAvailable():
        block = self.Member(RIFF_Block, 'block_%d' % (len(self._blocks) + 1), \
            valid_block_names);
        self._blocks.append(block);
        if block._name.value not in self._named_blocks:
          self._named_blocks[block._name.value] = [block];
        else:
          self._named_blocks[block._name.value].append(block);
      self.notes.append('0x%X|%d blocks' % \
          (len(self._blocks), len(self._blocks)));
    elif self._name.value == 'INAM':
      self._data = self.Member(C.STRING, 'Title/name');
    elif self._name.value == 'IART':
      self._data = self.Member(C.STRING, 'Author/artist');
    elif self._name.value == 'anih':
      self._data = self.Member(RIFF_anih, 'data');
    elif self._name.value == 'rate':
      self._data = self.Member(RIFF_rate, 'data');
    elif self._name.value == 'icon':
      self._data = self.Member(RIFF_icon, 'data');
    elif self._name.value == 'fmt ':
      self._data = self.Member(RIFF_fmt, 'data');
    else:
      self._data = self.Member(C.STRING, 'data', max_data_size);
    if unused_data_size > 0:
      self.current_max_size += unused_data_size;
      self.Unused();
    self.current_max_size = original_max_size;
