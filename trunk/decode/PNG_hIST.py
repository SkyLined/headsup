from Structure import Structure;

# http://www.w3.org/TR/PNG/#11hIST
class PNG_hIST(Structure):
  type_name = 'PNG_hIST';
  def __init__(self, stream, offset, max_size, parent, name, palette_entries):
    import math;
    import C;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._number_of_entries = int(math.floor(max_size / 2.0));
    self._entries = self.Member(C.ARRAY, 'frequencies', \
        self._number_of_entries, C.WORD, little_endian = True);
    self._entries.dump_simplified = True;

    if palette_entries is None:
      self.warnings.append('expected only when a PLTE chunk is present');
    elif palette_entries != self._number_of_entries:
      self.warnings.append('expected %d entries' % palette_entries);

    self.Unused();
