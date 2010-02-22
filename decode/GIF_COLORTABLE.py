from Structure import Structure;

class GIF_COLORTABLE(Structure):
  type_name = 'GIF_COLORTABLE';
  def __init__(self, stream, offset, max_size, parent, name, count, ordered):
    import C;
    from struct_RGBTRIPPLE import struct_RGBTRIPPLE;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    if ordered:
      self.notes.append('ordered by decreasing importance');
    else:
      self.notes.append('not ordered');

    self._rgb_tripples = self.Member(C.ARRAY, 'rgb_tripples', \
        count, struct_RGBTRIPPLE);
    self._rgb_tripples.dump_simplified = True;
