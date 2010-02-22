from Structure import Structure;

# http://www.w3.org/Graphics/GIF/spec-gif89a.txt
class GIF_BLOCK(Structure):
  type_name = 'GIF_BLOCK';
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._subblocks = [];
    self.ContainStream('', 0);
    while self.DataAvailable():
      subblock = self.Member(GIF_SUBBLOCK, \
          'subblock_%d' % (len(self._subblocks) + 1));
      self._subblocks.append(subblock);
      self.ContainStream( \
          subblock.contained_stream, subblock.contained_max_size);
      if subblock._is_terminator:
        break;
    else:
      self.warnings.append('block is not terminated');

#    for i in range(len(self._subblocks) - 2):
#      if self._subblocks[i].size < 0xFF:
#        self._subblocks[i].warnings.append( \
#            'expect size to be 0xFF|255 or 0x100|256');

    self.notes.append('%X|%d subblocks' % \
        (len(self._subblocks), len(self._subblocks)));

class GIF_SUBBLOCK(Structure):
  type_name = 'GIF_SUBBLOCK';
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._size = self.Member(C.BYTE, 'size');

    if self._size.value == 0:
      self._is_terminator = True;
      self.notes.append('block terminator');
      self.ContainStream('', 0);
    else:
      self._is_terminator = False;
      self._data = self.Member(C.STRING, 'data', self._size.value);
      self.ContainStream(self._data.value, self._data.size);

  def dump(self, header = None):
    if header is None:
      header = 18;
    else:
      header += 2;
    if self.notes:
      notes = ' // ' + ', '.join(self.notes);
    else:
      notes = '';

    print ('%08X+%08X ' % (self.offset, self.size)).ljust(header) + \
        '%s = %s (%d bytes)' % (self.name, self.type_name, self.size) + notes;

    for warning in self.warnings:
      print ' ' * header + '  // *** Warning: ' + warning;
