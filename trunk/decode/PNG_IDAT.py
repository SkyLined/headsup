from Structure import Structure;

class PNG_IDAT(Structure):
  type_name = 'PNG_IDAT';
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._compressed_pixel_data = self.Member( \
        C.STRING, 'compressed_pixel_data', max_size);

    self.Unused();
