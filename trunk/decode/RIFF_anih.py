from Structure import Structure;

class RIFF_anih(Structure):
  type_name = 'RIFF_anih';
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    from struct_ANIHEADER import struct_ANIHEADER;
    Structure.__init__(self, stream, offset, max_size, parent, name);
    
    self._anih = self.Member(struct_ANIHEADER, 'anih_data');

    self.Unused();
