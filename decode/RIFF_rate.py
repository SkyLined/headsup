from Structure import Structure;

class RIFF_rate(Structure):
  type_name = 'RIFF_rate';
  def __init__(self, stream, offset, max_size, parent, name):
    import math;
    import C;
    Structure.__init__(self, stream, offset, max_size, parent, name);
    self.dump_simplified = True;

    number_of_rates = int(math.floor(max_size / 4.0));
    self._rates = self.Member(C.ARRAY, 'rates', number_of_rates, C.DWORD);

    self.Unused();

  def SimplifiedValue(self, header = None):
    value = repr(self.value);
    if len(value) > 50:
      value = value[:50] + '...' + value[-1];
    return 'string(0x%X|%d bytes): %s' % \
        (self.size, self.size, value);
