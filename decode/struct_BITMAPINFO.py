from Structure import Structure;

# http://msdn.microsoft.com/en-us/library/aa921550.aspx
class struct_BITMAPINFO(Structure):
  type_name = 'struct BITMAPINFO';
  def __init__(self, stream, offset, max_size, parent, name, \
      height_div_2 = False):
    import C;
    from struct_BITMAPINFOHEADER import struct_BITMAPINFOHEADER;
    from struct_RGBQUAD import struct_RGBQUAD;
    Structure.__init__(self, stream, offset, max_size, parent, name);

    self._header = self.Member(struct_BITMAPINFOHEADER, \
        'header', height_div_2);

    bit_count = self._header._BitCount.value;
    compression = self._header._Compression.value;
    number_of_colors = 2 ** bit_count;
    used_colors = self._header._ClrUsed.value;
    # http://msdn.microsoft.com/en-us/library/aa930622.aspx

    if used_colors:
      number_of_rgb_quads = used_colors;
    else:
      number_of_rgb_quads = 2 ** bit_count;

    if bit_count in [16, 24, 32]:
      number_of_rgb_quads = 0;
    if compression == 3: # bitfields:
      number_of_rgb_quads = 3;

    if number_of_rgb_quads > 0:
      self._color_table = self.Member(C.ARRAY, 'color_table', \
          number_of_rgb_quads, struct_RGBQUAD);
      self._color_table.dump_simplified = True;
    else:
      self._color_table = None;
