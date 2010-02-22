from Structure import Structure;

# http://www.w3.org/TR/PNG/#11gAMA
class PNG_gAMA(Structure):
  type_name = 'PNG_gAMA';
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    Structure.__init__(self, stream, offset, max_size, parent, name);
    self._gamma = self.Member(C.DWORD, 'gamma', little_endian = False);
    gamma = 100000.0 / self._gamma.value;
    self._gamma.notes.append('= 1/%f;' % gamma);
    self.Unused();

