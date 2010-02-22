from Structure import Structure;

# http://www.w3.org/TR/PNG/#11PLTE
class PNG_PLTE(Structure):
  type_name = 'PNG_PLTE';
  def __init__(self, stream, offset, max_size, parent, name):
    import math;
    import C;
    from struct_RGBTRIPPLE import struct_RGBTRIPPLE;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    if max_size % 3 != 0:
      self.warnings.append('pallete size should be divisible by 3');

    self._number_of_rgb_tripples = math.floor(max_size / 3.0);
    self._rgb_tripples = self.Member(C.ARRAY, 'rgb_tripples', \
        self._number_of_rgb_tripples, struct_RGBTRIPPLE);
    self._rgb_tripples.dump_simplified = True;

    self.Unused();
