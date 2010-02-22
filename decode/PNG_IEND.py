from Structure import Structure;

class PNG_IEND(Structure):
  type_name = 'PNG_IEND';
  def __init__(self, stream, offset, max_size, parent, name):
    import C;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self.Unused();
