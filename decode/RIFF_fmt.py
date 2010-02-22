from Structure import Structure;

class RIFF_fmt():
  type_name = 'RIFF_fmt'
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    from struct_FMT import struct_FMT;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._fmt = self.Member(struct_FMT, 'fmt_data');
    self.Unused();
